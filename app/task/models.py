from sqlalchemy.orm import Mapped, mapped_column

from app.models import db


class Tasks(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    done: Mapped[bool] = mapped_column(default=False)

    def __repr__(self):
        return self.title
