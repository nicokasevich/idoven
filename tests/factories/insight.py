from factory import Factory, Faker, RelatedFactoryList, Sequence, SubFactory
from factory.alchemy import SQLAlchemyModelFactory

from app.models.insight import Insight
from app.schemas.insight import ZeroCrossingItem


class ZeroCrossingFactory(Factory):
    class Meta:
        model = ZeroCrossingItem

    channel = Faker("word")
    count = Faker("random_int", min=1, max=10)


class InsightFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Insight
        sqlalchemy_session_persistence = "commit"

    id = Sequence(lambda n: n + 1)

    zero_crossings = RelatedFactoryList(
        "tests.factories.insight.ZeroCrossingFactory", "insight", size=5
    )

    ecg = SubFactory("tests.factories.ecg.EcgFactory")
