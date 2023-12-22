from models.setup import db
import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class Complaint(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(sqlalchemy.String(45), nullable=False)
    description: Mapped[str] = mapped_column(sqlalchemy.Text, nullable=False)
    complaint_type_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("complaint_type.id"))
    complaint_status_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("complaint_status.id"))
    assignee_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("user.id"), nullable=True)
    file_url: Mapped[str] = mapped_column(sqlalchemy.Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(sqlalchemy.DateTime(timezone=True), server_default=sqlalchemy.sql.func.now())

    def __repr__(self) -> str:
        return f"Complaint(id={self.id}, title={self.title})"
    
    @property
    def serialize(self):
       return {
           "id": self.id,
           "title": self.title,
           "description": self.description,
           "complaint_type_id": self.complaint_type_id,
           "complaint_status_id": self.complaint_status_id,
           "assignee_id": self.assignee_id,
           "file_url": self.file_url,
           "created_at": self.created_at,
       }