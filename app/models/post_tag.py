from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel


class PostTag(BaseModel):
    __tablename__ = "post_tag"

    post_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("post.id", ondelete="CASCADE"), nullable=False
    )
    tag_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("tag.id", ondelete="CASCADE"), nullable=False
    )

    post: Mapped["Post"] = relationship("Post", back_populates="tags")
    tag: Mapped["Tag"] = relationship("Tag", back_populates="posts")
