import time
import datetime
import logging
import jwt
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from backend.database.db import SessionLocal, AuditLog, User, Role
from backend.authentication.auth import decode_access_token

logger = logging.getLogger(__name__)

# List of public endpoints that bypass authentication & RBAC
PUBLIC_PATHS = [
    "/",
    "/health",
    "/login",
    "/logout",
    "/refresh-token",
    "/docs",
    "/redoc",
    "/openapi.json"
]

class AuditAndRBACMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 1. Initialize audit parameters
        path = request.url.path
        method = request.method
        ip = request.client.host if request.client else "unknown"
        user_id = None
        user_email = None
        user_role = None
        user_permissions = []
        
        # 2. Extract and decode Bearer Token if present
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                # Decode the access token (using settings.JWT_SECRET_KEY)
                # Note: We do this manually to avoid raising HTTPException directly 
                # inside middleware which might fail to yield a clean JSON response.
                from backend.settings.config import settings
                from backend.authentication.auth import ALGORITHM
                
                payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[ALGORITHM])
                user_email = payload.get("sub")
                
                # Fetch user details from database to get permissions
                db = SessionLocal()
                try:
                    user = db.query(User).filter(User.email == user_email).first()
                    if user:
                        user_id = user.id
                        user_role = user.role.name
                        user_permissions = [p.permission_name for p in user.role.permissions]
                        # Inject user state into request so routes can access it directly
                        request.state.user = user
                finally:
                    db.close()
            except jwt.ExpiredSignatureError:
                # If path is protected, we must block. Otherwise ignore.
                if path not in PUBLIC_PATHS:
                    return JSONResponse(
                        status_code=401,
                        content={"detail": "Access token has expired"}
                    )
            except jwt.InvalidTokenError:
                if path not in PUBLIC_PATHS:
                    return JSONResponse(
                        status_code=401,
                        content={"detail": "Invalid access token"}
                    )
            except Exception as e:
                logger.error(f"Error validating token in middleware: {e}")

        # 3. RBAC (Role-Based Access Control) Enforcement
        # Bypass for public endpoints
        is_public = any(path == p or path.startswith(p + "/") for p in PUBLIC_PATHS)
        
        if not is_public:
            # If path is protected and user is not authenticated
            if not user_email:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Authentication credentials were not provided."}
                )
            
            # Admin has full access, skip permission checks
            if user_role != "Admin":
                authorized = False
                
                # Check Leave Policies (HR / Manager / Admin)
                if "leave-policies" in path:
                    if "Leave Policies" in user_permissions:
                        authorized = True
                
                # Check Onboarding (HR / Manager / Admin)
                elif "onboarding" in path:
                    if "Onboarding" in user_permissions:
                        authorized = True
                
                # Check HR Documents (HR / Admin)
                elif "hr-documents" in path:
                    if "HR Documents" in user_permissions:
                        authorized = True
                
                # Check Payroll (Manager / Admin)
                elif "payroll" in path:
                    if "Payroll" in user_permissions:
                        authorized = True
                
                # Check Finance (Manager / Admin)
                elif "finance" in path:
                    if "Finance" in user_permissions:
                        authorized = True
                
                # Check Admin dashboard actions (users, roles, permissions, settings, audit)
                elif any(p in path for p in ["/users", "/roles", "/permissions", "/settings", "/audit"]):
                    # These endpoints are strictly restricted to Admin role
                    authorized = False
                
                # Check Chat (Employee / HR / Manager / Support / Admin)
                elif "chat" in path:
                    if "Chat" in user_permissions:
                        authorized = True
                
                # Check RAG (Employee / HR / Manager / Support / Admin)
                elif "rag" in path:
                    if "RAG" in user_permissions:
                        authorized = True
                
                # Check Agents (Employee / HR / Manager / Support / Admin)
                elif "agents" in path:
                    if "Agents" in user_permissions:
                        authorized = True
                
                else:
                    # Default: for any other route, if the user has role Employee they have limited access
                    # We will allow standard routes unless specifically blocked
                    authorized = True
                
                if not authorized:
                    # Log forbidden access attempt
                    db = SessionLocal()
                    try:
                        audit_log = AuditLog(
                            user_id=user_id,
                            user_email=user_email,
                            ip=ip,
                            endpoint=path,
                            action=method,
                            status=403
                        )
                        db.add(audit_log)
                        db.commit()
                    finally:
                        db.close()
                        
                    return JSONResponse(
                        status_code=403,
                        content={"detail": f"Access denied: Insufficient permissions for module."}
                    )

        # 4. Proceed to route handler
        status_code = 500
        try:
            response = await call_next(request)
            status_code = response.status_code
            return response
        except Exception as e:
            logger.error(f"Unhandled exception during request processing: {e}")
            raise e
        finally:
            # 5. Create Audit Log entry in DB
            db = SessionLocal()
            try:
                audit_log = AuditLog(
                    user_id=user_id,
                    user_email=user_email,
                    ip=ip,
                    endpoint=path,
                    action=method,
                    status=status_code
                )
                db.add(audit_log)
                db.commit()
            except Exception as db_err:
                logger.error(f"Failed to save audit log: {db_err}")
            finally:
                db.close()
