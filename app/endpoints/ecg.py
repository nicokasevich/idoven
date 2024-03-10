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
    current_user: User = Depends(get_current_user),
    ecg_repository: EcgRepository = Depends(),
):
    if current_user.role != "user":
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return ecg_repository.all_by_user(current_user.id)


@router.get("/ecgs/{id}", response_model=EcgItem)
def get_ecg(
    id: int,
    current_user: User = Depends(get_current_user),
    ecg_repository: EcgRepository = Depends(),
):
    if current_user.role != "user":
        raise HTTPException(status_code=403, detail="Not enough permissions")

    ecg = ecg_repository.get(id)

    if current_user.id != ecg.user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    if not ecg:
        raise HTTPException(status_code=404, detail="Ecg not found")

    return ecg


@router.get("/ecgs/{ecg_id}/insights", response_model=Optional[InsightItem])
def get_ecg_insights(
    ecg_id: int,
    current_user: User = Depends(get_current_user),
    ecg_repository: EcgRepository = Depends(),
):
    if current_user.role != "user":
        raise HTTPException(status_code=403, detail="Not enough permissions")

    ecg = ecg_repository.get(ecg_id)

    if current_user.id != ecg.user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    if not ecg:
        raise HTTPException(status_code=404, detail="Ecg not found")

    return ecg.insight


@router.post("/ecgs", response_model=EcgItem)
def create_ecg(
    request: EcgCreate,
    current_user: User = Depends(get_current_user),
    ecg_repository: EcgRepository = Depends(),
):
    if current_user.role != "user":
        raise HTTPException(status_code=403, detail="Not enough permissions")

    ecg = ecg_repository.create(request, user_id=current_user.id)

    on_ecg_create.delay(ecg.id)

    return ecg
