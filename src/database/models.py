from typing import List

from sqlalchemy import DateTime, func, BigInteger, String, Text, ForeignKey, Boolean, Integer, PickleType
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, relationship, DeclarativeBase, mapped_column


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(150), nullable=True)
    last_name: Mapped[str] = mapped_column(String(150), nullable=True)
    phone: Mapped[str] = mapped_column(String(13), nullable=True)
    is_blocked: Mapped[Boolean] = mapped_column(Boolean, default=False)
    reports: Mapped[List['Report']] = relationship('Report', back_populates='user')
    sectors = relationship('UserSector', secondary='user_sector_associated', back_populates='users')


class UserSectorAssociated(Base):
    __tablename__ = 'user_sector_associated'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    sector_id: Mapped[int] = mapped_column(ForeignKey('user_sector.id', ondelete='CASCADE'), nullable=False)


class UserSector(Base):
    __tablename__ = 'user_sector'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    file: Mapped[str] = mapped_column(String(150), nullable=True)
    users = relationship('User', secondary='user_sector_associated', back_populates='sectors')


class Report(Base):
    __tablename__ = 'report'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    type_id: Mapped[int] = mapped_column(ForeignKey('type_report.id', ondelete='CASCADE'), nullable=False)
    device_id: Mapped[int] = mapped_column(ForeignKey('device.id', ondelete='CASCADE'), nullable=True)
    place_id: Mapped[int] = mapped_column(ForeignKey('place.id', ondelete='CASCADE'), nullable=True)
    date: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    image: Mapped[List[str]] = mapped_column(JSONB, nullable=False)
    user: Mapped['User'] = relationship('User', back_populates='reports')
    type: Mapped['TypeReport'] = relationship('TypeReport', back_populates='reports')
    devices: Mapped['Device'] = relationship('Device', back_populates='reports')
    place: Mapped['Place'] = relationship('Place', back_populates='reports')


class TypeReport(Base):
    __tablename__ = 'type_report'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=True)
    on_complex: Mapped[bool] = mapped_column(Boolean, nullable=False)
    on_place: Mapped[bool] = mapped_column(Boolean, nullable=False)
    count_images: Mapped[int] = mapped_column(Integer, nullable=False)
    reports: Mapped['Report'] = relationship('Report', back_populates='type')


class Place(Base):
    __tablename__ = 'place'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), unique=True)
    reports: Mapped['Report'] = relationship('Report', back_populates='place')


class Device(Base):
    __tablename__ = 'device'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type_id: Mapped[int] = mapped_column(ForeignKey('device_type.id', ondelete='CASCADE'), nullable=False)
    number: Mapped[str] = mapped_column(String(15), unique=True)
    type: Mapped['DeviceType'] = relationship('DeviceType', back_populates='devices')
    reports: Mapped['Report'] = relationship('Report', back_populates='devices')


class DeviceType(Base):
    __tablename__ = 'device_type'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), unique=True)
    description: Mapped[str] = mapped_column(String(150), nullable=True)
    devices: Mapped['Device'] = relationship('Device', back_populates='type')


class Banner(Base):
    __tablename__ = 'banner'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(25), unique=True)
    image: Mapped[str] = mapped_column(String(150), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
