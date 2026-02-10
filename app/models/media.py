from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel


class Media(BaseModel):
    __tablename__ = "media"

    url: Mapped[str] = mapped_column(String(500), nullable=False)

    post_media: Mapped[list["PostMedia"]] = relationship(
        "PostMedia", back_populates="media"
    )
