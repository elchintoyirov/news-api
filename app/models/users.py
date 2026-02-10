from sqlalchemy import BigInteger, Boolean, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel


class User(BaseModel):
    __tablename__ = "user"

    first_name: Mapped[str] = mapped_column(String(25), nullable=False)
    last_name: Mapped[str] = mapped_column(String(25), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    bio: Mapped[str] = mapped_column(String(250), default="")

    profession_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("profession.id", ondelete="SET NULL"), nullable=True
    )

    posts_count: Mapped[int] = mapped_column(BigInteger, default=0)
    posts_read_count: Mapped[int] = mapped_column(BigInteger, default=0)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_staff: Mapped[bool] = mapped_column(Boolean, default=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    deleted_email: Mapped[str] = mapped_column(String(50), nullable=True)

    profession: Mapped["Profession"] = relationship(
        "Profession", back_populates="users"
    )
    posts: Mapped[list["Post"]] = relationship("Post", back_populates="author")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="author")
