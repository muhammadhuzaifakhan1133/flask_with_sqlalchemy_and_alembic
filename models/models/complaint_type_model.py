from models.setup import db
import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

class ComplaintType(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sqlalchemy.String(45), nullable=False)
    created_at: Mapped[datetime] = mapped_column(sqlalchemy.DateTime(timezone=True), server_default=sqlalchemy.sql.func.now())

    def __repr__(self) -> str:
        return f"ComplaintType(id={self.id}, name={self.name})"