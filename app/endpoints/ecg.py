from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from app.core.security import get_current_user
from app.models.user import User
from app.repositories.ecg import EcgRepository
from app.schemas.ecg import EcgCreate, EcgItem
from app.schemas.insight import InsightItem
from worker.actions import on_ecg_create

router = APIRouter(tags=["ECG"])


@router.get("/ecgs", response_model=list[EcgItem])
def get_ecgs(
    _: User = Depends(get_current_user), ecg_repository: EcgRepository = Depends()
):
    return ecg_repository.all()


@router.get("/ecgs/{id}", response_model=EcgItem)
def get_ecg(
    id: int,
    _: User = Depends(get_current_user),
    ecg_repository: EcgRepository = Depends(),
):
    return ecg_repository.get(id)


@router.get("/ecgs/{ecg_id}/insights", response_model=Optional[InsightItem])
def get_ecg_insights(
    ecg_id: int,
    _: User = Depends(get_current_user),
    ecg_repository: EcgRepository = Depends(),
):
    ecg = ecg_repository.get(ecg_id)

    if not ecg:
        raise HTTPException(status_code=404, detail="Ecg not found")

    return ecg.insight


@router.post("/ecgs", response_model=EcgItem)
def create_ecg(
    request: EcgCreate,
    _: User = Depends(get_current_user),
    ecg_repository: EcgRepository = Depends(),
):
    ecg = ecg_repository.create(request)

    on_ecg_create.delay(ecg.id)

    return ecg
    return ecg
