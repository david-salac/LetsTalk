import logging

from fastapi import FastAPI
from fastapi import status
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi.middleware.cors import CORSMiddleware

from config import CONFIG

from . import __title__, __version__, __author__
from . import models
from .utils.genericviewset import create_generic_viewset
from .utils.viewsetwithcondition import viewset_with_condition_detail

LOGGER = logging.getLogger(__file__)

# ===================================
#         Main web service
# ===================================
service = FastAPI()

# ===================================
#          CORS headers
# ===================================
service.add_middleware(
    CORSMiddleware,
    allow_origins=CONFIG.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===================================
#        Database connector
# ===================================
db_session = models.db_session()


# ===================================
#        Application routes
# ===================================
@service.get("/")
def display_root():
    """Default informative end-point running on root address"""
    return {
        "title": __title__,
        "version": __version__,
        "author": __author__
    }


router = InferringRouter()

# CRUD for model: Doctor
create_generic_viewset(router,
                       models.Doctor,
                       models.DoctorSerializer,
                       models.DoctorModifySerializer,
                       db_session,
                       r"/api/doctor")


# CRUD for model: Condition
@cbv(router)
class ConditionViewSet(
    create_generic_viewset(router,
                           models.Condition,
                           models.ConditionSerializer,
                           models.ConditionModifySerializer,
                           db_session,
                           r"/api/condition")
):
    @router.post(r"/api/condition-with-doctor",
                 response_model=models.ConditionDoctorNestedSerializer,
                 status_code=status.HTTP_201_CREATED)
    def create_doctor_and_condition(
            self,
            item: models.ConditionAndDoctorModifySerializer
    ):
        """Create both doctor and condition in one call"""
        # Create doctor:
        doctor = models.Doctor(
            **item.dict()['doctor']
        ).create(db_session)
        # Create condition
        new_condition = models.Condition(
            **item.dict()['condition'],
            doctor_id=doctor['id']
        ).create(db_session)

        # Construct nested object
        new_condition.pop('doctor_id')  # Remove doctor_id from root
        new_condition = new_condition | {'doctor': doctor}

        db_session.close()

        return new_condition

    @router.get(
        r"/api/condition-with-doctor",
        response_model=list[models.ConditionDoctorNestedSerializer],
        status_code=status.HTTP_200_OK
    )
    def list_doctor_and_condition(self):
        """Return nested dict without doctor_id but as nested
        dict for 'doctor' key (presenting the whole Doctor object).
        """
        all_conditions = models.Condition.all(db_session)
        _conditions = []
        for condition in all_conditions:
            # Remove 'doctor_id' field
            doctor_id = int(condition.pop("doctor_id"))
            # Add nested field for doctor
            condition['doctor'] = models.Doctor.get(db_session,
                                                    id=doctor_id)
            _conditions.append(condition)

        db_session.close()
        return _conditions

    @router.put(
        r"/api/condition-with-doctor",
        response_model=models.ConditionDoctorNestedSerializer,
        status_code=status.HTTP_200_OK
    )
    def update_doctor_and_condition(
            self, item: models.ConditionAndDoctorSerializer
    ):
        """Update both doctor and condition on one call.
        """
        # Construct standard Condition & Doctor data-sets
        request = item.dict()
        condition = request.pop('condition')
        doctor = request.pop('doctor')
        condition['doctor_id'] = doctor['id']
        # Update condition
        models.Condition.update(db_session,
                                {"id": condition['id']},
                                condition)
        # Update doctor
        models.Doctor.update(db_session,
                             {"id": doctor['id']},
                             doctor)
        db_session.close()
        # Return nested structure
        condition.pop('doctor_id')
        new_condition = condition | {'doctor': doctor}
        return new_condition

# CRUD for model: Expectation
viewset_with_condition_detail(
    router,
    models.Expectation,
    models.ExpectationSerializer,
    models.ExpectationModifySerializer,
    models.ExpectationWithConditionSerializer,
    db_session,
    r"/api/expectation"
)

# CRUD for model: Concern
viewset_with_condition_detail(
    router,
    models.Concern,
    models.ConcernSerializer,
    models.ConcernModifySerializer,
    models.ConcernWithConditionSerializer,
    db_session,
    r"/api/concern"
)

# CRUD for model: Appointment
viewset_with_condition_detail(
    router,
    models.Appointment,
    models.AppointmentSerializer,
    models.AppointmentModifySerializer,
    models.AppointmentWithConditionSerializer,
    db_session,
    r"/api/appointment"
)

# Register router
service.include_router(router)
