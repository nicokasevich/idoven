from datetime import datetime

from factory import (
    LazyFunction,
    RelatedFactoryList,
    Sequence,
    SubFactory,
    post_generation,
)
from factory.alchemy import SQLAlchemyModelFactory

from app.models.ecg import Ecg
from tests.factories.insight import InsightFactory


class EcgFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Ecg
        sqlalchemy_session_persistence = "commit"

    id = Sequence(lambda n: n + 1)
    created_at = LazyFunction(datetime.now)

    user = SubFactory("tests.factories.user.UserFactory")

    leads = RelatedFactoryList(
        "tests.factories.lead.LeadFactory", size=12, factory_related_name="ecg"
    )

    @post_generation
    def insight(self, *args, **kwargs):
        InsightFactory(ecg=self)
