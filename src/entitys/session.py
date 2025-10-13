from datetime import datetime

from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .base import Base


class Session(Base):
    __tablename__ = "sessions"

    token: Mapped[str] = mapped_column(String(256))
    expires_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship(back_populates="sessions")