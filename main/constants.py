from enum import Enum


class UserStatus(str, Enum):
    active = "active"
    inactive = "inactive"


class ContactStatus(str, Enum):
    active = "active"
    inactive = "inactive"


class CourseStatus(str, Enum):
    active = "active"
    inactive = "inactive"


class TeacherStatus(str, Enum):
    active = "active"
    inactive = "inactive"


class ResultStatus(str, Enum):
    active = "active"
    inactive = "inactive"


class AdvantageStatus(str, Enum):
    active = "active"
    inactive = "inactive"


class AboutStatus(str, Enum):
    active = "active"
    inactive = "inactive"
