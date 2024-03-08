from tests.factories.ecg import EcgFactory
from tests.factories.insight import InsightFactory
from tests.factories.lead import LeadFactory
from tests.factories.user import UserFactory

sqlalchemy_factories: list = [UserFactory, EcgFactory, LeadFactory, InsightFactory]


__all__ = ["UserFactory", "EcgFactory", "LeadFactory", "InsightFactory"]
