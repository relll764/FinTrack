from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, String, Numeric
from app.db.base import Base


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    subscription: Mapped[bool] = mapped_column(nullable=False, default=False)
    balance: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    theme: Mapped[str] = mapped_column(String(40), nullable=False)