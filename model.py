from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass

class Odd(Base):
    __tablename__ = "odds"

    id: Mapped[int] = mapped_column(primary_key=True)
    # match_time: Mapped[datetime] = mapped_column(DateTime)
    match_time: Mapped[str] = mapped_column(String(30))
    home_team: Mapped[str] = mapped_column(String(30))
    away_team: Mapped[str] = mapped_column(String(30))
    home_odds: Mapped[float]
    draw_odds: Mapped[float]
    away_odds: Mapped[float]
    roi: Mapped[float | None] = mapped_column(Float)
    arbitrage_opportunity: Mapped[bool | None] = mapped_column(Boolean)

    def __repr__(self) -> str:
        return f"Odd({self.home_team!r} vs {self.away_team!r}, roi={self.roi*100:.2f}%)"

engine = create_engine("sqlite:///db.sqlite", echo=True)

Base.metadata.create_all(engine)