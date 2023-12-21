import json
import sqlalchemy
import enum
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from models.setup import db

class RoleTypeEnum(str, enum.Enum):
    superadmin = "superadmin"
    admin = "admin"
    staff = "staff"

    

class User(db.Model):
    id: Mapped[int] = mapped_column(sqlalchemy.Integer, primary_key=True)
    email: Mapped[str] = mapped_column(sqlalchemy.String(45), unique=True, nullable=False)
    phone_no: Mapped[str] = mapped_column(sqlalchemy.String(20), unique=True, nullable=True)
    password: Mapped[str] = mapped_column(sqlalchemy.String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(sqlalchemy.Boolean, nullable=False, server_default=sqlalchemy.sql.true())
    role_type: Mapped[str] = mapped_column(sqlalchemy.Enum(RoleTypeEnum), nullable=False)
    created_at: Mapped[datetime] = mapped_column(sqlalchemy.DateTime(timezone=True), server_default=sqlalchemy.sql.func.now())

    def __repr__(self) -> str:
        return f"User(id={self.id}, email={self.email}, phone_no={self.phone_no})"