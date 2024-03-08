from factory import Faker, Sequence, SubFactory
from factory.alchemy import SQLAlchemyModelFactory

from app.models.lead import Lead


class LeadFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Lead
        sqlalchemy_session_persistence = "commit"

    id = Sequence(lambda n: n + 1)

    name = Faker("word")
    number_of_samples = Faker("random_int", min=10, max=10)
    signal = Faker("pylist", value_types=[int], nb_elements=number_of_samples)

    ecg = SubFactory("tests.factories.ecg.EcgFactory")
