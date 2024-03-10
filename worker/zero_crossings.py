import numpy as np

from app.core.database import SessionLocal
from app.models.ecg import Ecg
from app.models.insight import Insight
from app.repositories.ecg import EcgRepository


def calculate_zero_crossings(ecg_id: int) -> Ecg:
    db = SessionLocal()
    ecg_repository = EcgRepository(db)
    ecg = ecg_repository.get(ecg_id)

    zero_crossings = []
    for lead in ecg.leads:
        signal = np.array(lead.signal) > 0
        count = len((signal[:-1] ^ signal[1:]).nonzero()[0])
        zero_crossings.append({"count": count, "channel": lead.name})
        ecg.insights.append(Insight(ecg_id=ecg.id, zero_crossings=zero_crossings))

    return ecg_repository.update(ecg)
