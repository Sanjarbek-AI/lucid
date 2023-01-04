import sqlalchemy
from sqlalchemy import DateTime

from main.constants import *
from main.databases import metadata

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("full_name", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("location", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("language", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("telegram_id", sqlalchemy.BigInteger),
    sqlalchemy.Column("phone_number", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("status", sqlalchemy.Enum(UserStatus), nullable=True),
    sqlalchemy.Column('created_at', DateTime(timezone=True), nullable=True),
    sqlalchemy.Column('updated_at', DateTime(timezone=True), nullable=True)
)

contacts = sqlalchemy.Table(
    "contacts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("image_uz", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("image_en", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("image_ru", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("contact_uz", sqlalchemy.Text, nullable=True),
    sqlalchemy.Column("contact_en", sqlalchemy.Text, nullable=True),
    sqlalchemy.Column("contact_ru", sqlalchemy.Text, nullable=True),
    sqlalchemy.Column("status", sqlalchemy.Enum(ContactStatus), nullable=True),
    sqlalchemy.Column('created_at', DateTime(timezone=True), nullable=True),
    sqlalchemy.Column('updated_at', DateTime(timezone=True), nullable=True)
)

courses = sqlalchemy.Table(
    "courses",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("image_uz", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("image_en", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("image_ru", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("info_uz", sqlalchemy.Text, nullable=True),
    sqlalchemy.Column("info_ru", sqlalchemy.Text, nullable=True),
    sqlalchemy.Column("info_en", sqlalchemy.Text, nullable=True),
    sqlalchemy.Column("status", sqlalchemy.Enum(CourseStatus), nullable=True),
    sqlalchemy.Column('created_at', DateTime(timezone=True), nullable=True),
    sqlalchemy.Column('updated_at', DateTime(timezone=True), nullable=True)
)

registered_to_course = sqlalchemy.Table(
    "registered_to_course",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("course_id", sqlalchemy.Integer, nullable=True),
    sqlalchemy.Column("user_id", sqlalchemy.BigInteger, nullable=True),
    sqlalchemy.Column('created_at', DateTime(timezone=True), nullable=True),
    sqlalchemy.Column('updated_at', DateTime(timezone=True), nullable=True)
)

teachers = sqlalchemy.Table(
    "teachers",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("image_uz", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("image_en", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("image_ru", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("info_uz", sqlalchemy.Text, nullable=True),
    sqlalchemy.Column("info_ru", sqlalchemy.Text, nullable=True),
    sqlalchemy.Column("info_en", sqlalchemy.Text, nullable=True),
    sqlalchemy.Column("status", sqlalchemy.Enum(TeacherStatus), nullable=True),
    sqlalchemy.Column('created_at', DateTime(timezone=True), nullable=True),
    sqlalchemy.Column('updated_at', DateTime(timezone=True), nullable=True)
)


results = sqlalchemy.Table(
    "results",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("image_uz", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("image_en", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("image_ru", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("info_uz", sqlalchemy.Text, nullable=True),
    sqlalchemy.Column("info_ru", sqlalchemy.Text, nullable=True),
    sqlalchemy.Column("info_en", sqlalchemy.Text, nullable=True),
    sqlalchemy.Column("status", sqlalchemy.Enum(ResultStatus), nullable=True),
    sqlalchemy.Column('created_at', DateTime(timezone=True), nullable=True),
    sqlalchemy.Column('updated_at', DateTime(timezone=True), nullable=True)
)


about = sqlalchemy.Table(
    "about",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("image_uz", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("image_en", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("image_ru", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("info_uz", sqlalchemy.Text, nullable=True),
    sqlalchemy.Column("info_ru", sqlalchemy.Text, nullable=True),
    sqlalchemy.Column("info_en", sqlalchemy.Text, nullable=True),
    sqlalchemy.Column("status", sqlalchemy.Enum(AboutStatus), nullable=True),
    sqlalchemy.Column('created_at', DateTime(timezone=True), nullable=True),
    sqlalchemy.Column('updated_at', DateTime(timezone=True), nullable=True)
)

advantage = sqlalchemy.Table(
    "advantage",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("image_uz", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("image_en", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("image_ru", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("info_uz", sqlalchemy.Text, nullable=True),
    sqlalchemy.Column("info_ru", sqlalchemy.Text, nullable=True),
    sqlalchemy.Column("info_en", sqlalchemy.Text, nullable=True),
    sqlalchemy.Column("status", sqlalchemy.Enum(AdvantageStatus), nullable=True),
    sqlalchemy.Column('created_at', DateTime(timezone=True), nullable=True),
    sqlalchemy.Column('updated_at', DateTime(timezone=True), nullable=True)
)