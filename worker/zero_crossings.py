import numpy as np

from app.core.database import SessionLocal
from app.models.ecg import Ecg
from app.models.insight import Insight
from app.repositories.ecg import EcgRepository


def count_zero_crossings(sequence: list) -> int:
    """Counts the number of zero crossings in a sequence."""

    signal = np.array(sequence) > 0
    return len((signal[:-1] ^ signal[1:]).nonzero()[0])


def generate_zero_crossings(ecg_id: int) -> Ecg:
    """Appends zero crossings to the ecg insights. And returns the updated ecg."""

    db = SessionLocal()
    ecg_repository = EcgRepository(db)
    ecg = ecg_repository.get(ecg_id)

    zero_crossings = []
    for lead in ecg.leads:
        count = count_zero_crossings(lead.signal)
        zero_crossings.append({"count": count, "channel": lead.name})

    if not ecg.insight:
        ecg.insight = Insight(ecg_id=ecg.id, zero_crossings=zero_crossings)

    return ecg_repository.update(ecg)
