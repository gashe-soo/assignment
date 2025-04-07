from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Tag(Base):
    __tablename__ = "tag"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(
        String, unique=True, nullable=False, index=True
    )

    translations: Mapped[list["TagTranslation"]] = relationship(
        back_populates="tag", cascade="all, delete-orphan"
    )


class TagTranslation(Base):
    __tablename__ = "tag_translation"

    id: Mapped[int] = mapped_column(primary_key=True)
    tag_id: Mapped[int] = mapped_column(
        ForeignKey("tag.id", ondelete="CASCADE"), nullable=False
    )
    locale: Mapped[str] = mapped_column(String(10), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False, index=True)

    tag: Mapped["Tag"] = relationship(back_populates="translations")

    __table_args__ = (
        UniqueConstraint("tag_id", "locale", name="uq_tag_locale"),
    )
