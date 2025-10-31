from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .enums.auth_provider import AuthProvider


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(75), unique=True)
    hashed_password: Mapped[str] = mapped_column(
        String(97),
        nullable=True
    )  # Size of current hash function beeing used
    role: Mapped[str] = mapped_column(String(15), nullable=True)
    google_id: Mapped[str] = mapped_column(String(100), nullable=True)
    auth_provider: Mapped[str] = mapped_column(default=AuthProvider.LOCAL, server_default=AuthProvider.LOCAL.value)

    sessions: Mapped[list["Session"]] = relationship( # type: ignore
        back_populates="user", cascade="all, delete-orphan"
    )
