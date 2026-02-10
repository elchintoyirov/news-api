from sqlalchemy import BigInteger, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel


class Post(BaseModel):
    __tablename__ = "post"

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    category_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("category.id"), nullable=False
    )

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)

    views_count: Mapped[int] = mapped_column(BigInteger, default=0)
    comments_count: Mapped[int] = mapped_column(BigInteger, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    author: Mapped["User"] = relationship("User", back_populates="posts")
    category: Mapped["Category"] = relationship("Category", back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="post")
    media: Mapped[list["PostMedia"]] = relationship("PostMedia", back_populates="post")
    tags: Mapped[list["PostTag"]] = relationship("PostTag", back_populates="post")
