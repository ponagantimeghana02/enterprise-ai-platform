import datetime
import logging
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from backend.settings.config import settings

# Setup logging
logger = logging.getLogger(__name__)

# Determine Database URL (Fallback to SQLite if PostgreSQL not configured)
db_url = settings.DATABASE_URL
if not db_url:
    db_url = "sqlite:///./backend.db"
    logger.warning("No DATABASE_URL configured. Falling back to local SQLite: backend.db")

# Create Engine
if db_url.startswith("sqlite"):
    engine = create_engine(db_url, connect_args={"check_same_thread": False})
else:
    engine = create_engine(db_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Many-to-Many Association Table for Roles and Permissions
role_permissions = Table(
    'role_permissions',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id', ondelete='CASCADE'), primary_key=True)
)

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    users = relationship("User", back_populates="role")
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    permission_name = Column(String(100), unique=True, nullable=False)
    module = Column(String(50), nullable=False)

    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="RESTRICT"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    role = relationship("Role", back_populates="users")
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user")

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(512), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="refresh_tokens")

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    user_email = Column(String(100), nullable=True)
    ip = Column(String(45), nullable=False)
    endpoint = Column(String(255), nullable=False)
    action = Column(String(50), nullable=False)
    status = Column(Integer, nullable=False)

    user = relationship("User", back_populates="audit_logs")


# Dependency to get db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Database initialization and seeding
def init_db():
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if roles are already seeded
        if db.query(Role).count() == 0:
            logger.info("Seeding database roles and permissions...")
            
            # Create Roles
            admin_role = Role(id=1, name="Admin")
            hr_role = Role(id=2, name="HR")
            manager_role = Role(id=3, name="Manager")
            employee_role = Role(id=4, name="Employee")
            support_role = Role(id=5, name="Support")
            
            db.add_all([admin_role, hr_role, manager_role, employee_role, support_role])
            db.commit()
            
            # Create Permissions
            permissions = [
                Permission(id=1, permission_name="Leave Policies", module="hr"),
                Permission(id=2, permission_name="Onboarding", module="hr"),
                Permission(id=3, permission_name="HR Documents", module="hr"),
                Permission(id=4, permission_name="Payroll", module="finance"),
                Permission(id=5, permission_name="Finance", module="finance"),
                Permission(id=6, permission_name="Chat", module="assistant"),
                Permission(id=7, permission_name="RAG", module="assistant"),
                Permission(id=8, permission_name="Agents", module="assistant"),
                Permission(id=9, permission_name="Users Dashboard", module="admin"),
                Permission(id=10, permission_name="Audit Logs", module="admin"),
                Permission(id=11, permission_name="Settings", module="admin"),
            ]
            db.add_all(permissions)
            db.commit()
            
            # Map Permissions to Roles
            # Admin gets all (1 to 11)
            admin_role.permissions.extend(permissions)
            
            # HR gets 1, 2, 3, 6, 7, 8
            hr_role.permissions.extend([permissions[0], permissions[1], permissions[2], permissions[5], permissions[6], permissions[7]])
            
            # Manager gets 1, 2, 4, 5, 6, 7, 8
            manager_role.permissions.extend([permissions[0], permissions[1], permissions[3], permissions[4], permissions[5], permissions[6], permissions[7]])
            
            # Employee gets 6, 7, 8
            employee_role.permissions.extend([permissions[5], permissions[6], permissions[7]])
            
            # Support gets 6, 7, 8
            support_role.permissions.extend([permissions[5], permissions[6], permissions[7]])
            
            db.commit()
            
            # Seed Default Admin User
            # password is 'adminpassword'
            # Hashed using bcrypt: $2b$12$7wA8q95D/d6V5vX0w9Tye.mG3X5iB/yX2rW4q2r9D5P8h7M1i1vSq
            admin_user = User(
                id=1,
                name="System Admin",
                email="admin@example.com",
                password_hash="$2b$12$NLvCSPmR6cGCJmrn9f/g0u8qZBL1PX6tQh.u7m.kxdk2IeIKERgHW",
                role_id=1
            )
            db.add(admin_user)
            db.commit()
            logger.info("Seeding completed successfully.")
    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()
