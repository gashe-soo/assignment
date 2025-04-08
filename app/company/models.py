from datetime import datetime, timezone

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.enums import Locale
from app.tag.models import Tag


class Company(Base):
    __tablename__ = "company"

    id: Mapped[int] = mapped_column(primary_key=True)
    default_locale: Mapped[str] = mapped_column(
        String(10), nullable=False, default=Locale.KO
    )
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    translations: Mapped[list["CompanyTranslation"]] = relationship(
        back_populates="company", cascade="all, delete-orphan"
    )

    tags: Mapped[list["CompanyTag"]] = relationship(
        back_populates="company", cascade="all, delete-orphan"
    )


class CompanyTranslation(Base):
    __tablename__ = "company_translation"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("company.id", ondelete="CASCADE"), nullable=False
    )
    locale: Mapped[str] = mapped_column(String(10), nullable=False, index=True)
    name: Mapped[str] = mapped_column(nullable=False, index=True)

    company: Mapped["Company"] = relationship(back_populates="translations")

    __table_args__ = (
        UniqueConstraint("company_id", "locale", name="uq_company_locale"),
    )


class CompanyTag(Base):
    __tablename__ = "company_tag"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("company.id", ondelete="CASCADE"), nullable=False
    )
    tag_id: Mapped[int] = mapped_column(
        ForeignKey("tag.id", ondelete="CASCADE"), nullable=False
    )

    company: Mapped["Company"] = relationship(back_populates="tags")
    tag: Mapped[Tag] = relationship()

    __table_args__ = (
        UniqueConstraint("company_id", "tag_id", name="uq_company_tag"),
    )
