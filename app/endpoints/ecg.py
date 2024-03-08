from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.models.user import User
from app.repositories.ecg import EcgRepository
from app.schemas.ecg import EcgCreate, EcgItem

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


@router.post("/ecgs", response_model=EcgItem)
def create_ecg(
    request: EcgCreate,
    _: User = Depends(get_current_user),
    ecg_repository: EcgRepository = Depends(),
):
    return ecg_repository.create(request)
