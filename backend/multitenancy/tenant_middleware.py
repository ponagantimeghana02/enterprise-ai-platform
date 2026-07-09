from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from .tenant_manager import TenantManager


class TenantMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        tenant_id = request.headers.get("X-Tenant-ID")

        if not tenant_id:
            from fastapi.responses import JSONResponse

            return JSONResponse(
                status_code=400,
                content={
                    "message": "Tenant ID Missing"
                }
            )

        request.state.tenant = TenantManager.get_tenant(
            tenant_id
        )

        response = await call_next(request)

        return response