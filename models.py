from __future__ import annotations
from datetime import datetime, UTC
from sqlalchemy import String, Integer,Text,  ForeignKey, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class User(Base):
    __table__ = "users"
    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username:Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    image_file:Mapped[str | None] = mapped_column(String(150), nullable=True, default=None)
    @property
    def image_file(self):
        if self.image_file:
            return f"/static/profile_pics/{self.image_file}"

        return "/static/profile_pics/default.jpg"

    posts:Mapped[list[Post]] = relationship(back_populates="author")

class Post(Base):
    __table__ = "posts"
    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title:Mapped[str] = mapped_column(String(150), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    date_posted:Mapped[str] =  mapped_column(DateTime, default=lambda: datetime.now(UTC))
    user_id:Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    author:Mapped[User] = relationship(back_populates="posts")