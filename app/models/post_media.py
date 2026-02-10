from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel


class PostMedia(BaseModel):
    __tablename__ = "post_media"

    post_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("post.id", ondelete="CASCADE"), nullable=False
    )
    media_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("media.id", ondelete="CASCADE"), nullable=False
    )

    post: Mapped["Post"] = relationship("Post", back_populates="media")
    media: Mapped["Media"] = relationship("Media", back_populates="post_media")
