from datetime import datetime

from factory import LazyFunction, RelatedFactoryList, Sequence, post_generation
from factory.alchemy import SQLAlchemyModelFactory

from app.models.ecg import Ecg
from tests.factories.insight import InsightFactory


class EcgFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Ecg
        sqlalchemy_session_persistence = "commit"

    id = Sequence(lambda n: n + 1)
    created_at = LazyFunction(datetime.now)

    leads = RelatedFactoryList(
        "tests.factories.lead.LeadFactory", size=12, factory_related_name="ecg"
    )

    @post_generation
    def insight(self, *args, **kwargs):
        InsightFactory(ecg=self)
