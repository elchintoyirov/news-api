from datetime import datetime

from sqlalchemy import BigInteger, Integer, Boolean, Text, ForeignKey, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel, Base


class Comment(BaseModel):
    __tablename__ = "comment"

    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), primary_key=True)
    media_id: Mapped[int] = mapped_column(ForeignKey('media.id'), primary_key=True)

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("user.id", ondelete="CASCADE"), nullable=True
    )
    post_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("post.id", ondelete="CASCADE"), nullable=False
    )

    text: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    author: Mapped["User"] = relationship("User", back_populates="comments")
    post: Mapped["Post"] = relationship("Post", back_populates="comments")

class UserSearch(Base):
    __tablename__ = "user_searches"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    term: Mapped[int] = mapped_column(String(50), nullable=False)
    count: Mapped[int] = mapped_column(Integer, default=0)

    def __repr__(self):
        return f"UserSearch({self.term})"
    
class Devices(BaseModel):
    __tablename__ = "devices"

    user_agent: Mapped[str] = mapped_column(String(255), nullable=False)
    last_active: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    def __repr__(self):
        return f"Device({self.user_agent})"
    
class Like(Base):
    __tablename__ = "likes"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    post_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("post.id"))
    device_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("devices.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )

    def __repr__(self):
        return f"Like({self.post_id})"