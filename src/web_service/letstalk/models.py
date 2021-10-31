import enum
import logging

from sqlalchemy import Column, Integer, String, \
    create_engine, ForeignKey, DateTime
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from pydantic import BaseModel, Field
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from sqlalchemy.dialects.postgresql import ENUM as pgsql_ENUM

from config import CONFIG

from .utils.model_modifier import skip_primary_keys_in_model, \
    skip_fields_in_pydantic_model
from .utils.extended_model import ExtendedModelMixin

LOGGER = logging.getLogger(__name__)

# ===================================
#    CREATE POSTGRESQL CONNECTION
# ===================================
SQLALCHEMY_DATABASE_URL = f"postgresql://{CONFIG.PGSQL_USER}:" \
                          f"{CONFIG.PGSQL_PASS}@" \
                          f"{CONFIG.PGSQL_HOST}:" \
                          f"{CONFIG.PGSQL_PORT}/" \
                          f"{CONFIG.PGSQL_DATABASE}"

# TODO: DB connection management needs overhaul
engine = create_engine(SQLALCHEMY_DATABASE_URL)
db_session = scoped_session(sessionmaker(bind=engine))


# ===================================
#          DATABASE MODELS
# ===================================
Base = declarative_base()


class Doctor(Base, ExtendedModelMixin):
    """Table defining doctor"""
    __tablename__ = "doctor"

    # Primary key
    id: int = Column(Integer, primary_key=True)

    # Data specific columns
    name: str = Column(String, nullable=False)
    specialism: str = Column(String, nullable=False)

    # Back-references
    conditions = relationship("Condition")


class Condition(Base, ExtendedModelMixin):
    """Table for patient condition"""
    __tablename__ = "condition"

    # Primary key
    id = Column(Integer, primary_key=True)

    # Data specific columns
    name = Column(String, nullable=False)
    duration = Column(String, nullable=False)
    details = Column(String)

    # Foreign key to Doctor
    doctor_id = Column(Integer,
                       ForeignKey('doctor.id',
                                  ondelete="CASCADE"),
                       nullable=False)
    doctor = relationship('Doctor',
                          back_populates="conditions")

    # Back-references
    expectations = relationship("Expectation")

    concerns = relationship("Concern")

    appointments = relationship("Appointment")


class ConcernCreatorEnum(enum.Enum):
    """Enumerates who can create concern"""
    patient = "patient"
    doctor = "doctor"


class Concern(Base, ExtendedModelMixin):
    """Concerns related to patient health"""
    __tablename__ = "concern"

    # Primary key
    id = Column(Integer, primary_key=True)

    # Data specific columns
    creator = Column(pgsql_ENUM(ConcernCreatorEnum), nullable=False)
    details = Column(String)
    symptoms = Column(String, nullable=False)
    level = Column(Integer, nullable=False)

    # Foreign key to Condition
    condition_id = Column(Integer,
                          ForeignKey('condition.id',
                                     ondelete="CASCADE"),
                          nullable=False)
    condition = relationship('Condition',
                             back_populates="concerns")


class Expectation(Base, ExtendedModelMixin):
    """Expected progression of diagnosis"""
    __tablename__ = "expectation"

    # Primary key
    id = Column(Integer, primary_key=True)

    # Data specific columns
    name = Column(String, nullable=False)
    details = Column(String)

    # Foreign key to Condition
    condition_id = Column(Integer,
                          ForeignKey('condition.id',
                                     ondelete="CASCADE"),
                          nullable=False)
    condition = relationship('Condition',
                             back_populates="expectations")


class Appointment(Base, ExtendedModelMixin):
    """Appointment to address a condition."""
    __tablename__ = "appointment"

    # Primary key
    id = Column(Integer, primary_key=True)

    # Data specific columns
    details = Column(String)
    date_and_time = Column(DateTime,  # When to set appointment
                           nullable=False)

    # Foreign key to Condition
    condition_id = Column(Integer,
                          ForeignKey('condition.id',
                                     ondelete="CASCADE"),
                          nullable=False)
    condition = relationship('Condition',
                             back_populates="appointments")


# ===================================
#  MIGRATE CHANGES INTO THE DATABASE
# ===================================
Base.metadata.create_all(engine)

# ===================================
#    PYDANTIC MODELS (SERIALIZERS)
# ===================================
# Full serializers
DoctorSerializer = sqlalchemy_to_pydantic(Doctor)
ConditionSerializer = sqlalchemy_to_pydantic(Condition)
class ConcernSerializer(sqlalchemy_to_pydantic(Concern)):
    """Modify default concern serializer to restrict level"""
    level: int = Field(gt=0, lt=6) # level is the integer in [1, 5]


ExpectationSerializer = sqlalchemy_to_pydantic(Expectation)
AppointmentSerializer = sqlalchemy_to_pydantic(Appointment)

# Serializers for create and modify operations
DoctorModifySerializer = skip_primary_keys_in_model(
    DoctorSerializer, "DoctorModifySerializer"
)
ConditionModifySerializer = skip_primary_keys_in_model(
    ConditionSerializer, "ConditionModifySerializer"
)
ConcernModifySerializer = skip_primary_keys_in_model(
    ConcernSerializer, "ConcernModifySerializer"
)
ExpectationModifySerializer = skip_primary_keys_in_model(
    ExpectationSerializer, "ExpectationModifySerializer"
)
AppointmentModifySerializer = skip_primary_keys_in_model(
    AppointmentSerializer, "AppointmentModifySerializer"
)


# Join serializers for Condition and Doctor
class ConditionAndDoctorModifySerializer(BaseModel):
    condition: skip_fields_in_pydantic_model(
        ConditionModifySerializer,
        "ConditionModifyNoNameSerializer",
        {"doctor_id"}  # This one is skipped
    )
    doctor: DoctorModifySerializer


class ConditionAndDoctorSerializer(BaseModel):
    condition: skip_fields_in_pydantic_model(
        ConditionSerializer,
        "ConditionNoNameSerializer",
        {"doctor_id"}  # This one is skipped
    )
    doctor: DoctorSerializer


class ConditionDoctorNestedSerializer(
    skip_fields_in_pydantic_model(
        ConditionSerializer,
        "ConditionNoNameSerializer",
        {"doctor_id"}  # This one is skipped
    )
):
    doctor: DoctorSerializer


class ConcernWithConditionSerializer(skip_fields_in_pydantic_model(
        ConcernSerializer,
        "ConcernNoNameSerializer",
        {"condition_id"}  # This one is skipped
    )):
    condition: ConditionSerializer


class ExpectationWithConditionSerializer(
    skip_fields_in_pydantic_model(
        ExpectationSerializer,
        "ExpectationNoNameSerializer",
        {"condition_id"}  # This one is skipped
    )):
    condition: ConditionSerializer


class AppointmentWithConditionSerializer(
    skip_fields_in_pydantic_model(
        AppointmentSerializer,
        "AppointmentNoNameSerializer",
        {"condition_id"}  # This one is skipped
    )):
    condition: ConditionSerializer

# TODO: serializers also need to validate existence of IDs
