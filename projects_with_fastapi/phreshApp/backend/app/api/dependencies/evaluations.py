from typing import List

from fastapi import HTTPException, Depends, Path, status

from app.models.user import UserInDB
from app.models.cleaning import CleaningInDB
from app.models.offer import OfferInDB
from app.models.evaluation import EvaluationInDB

from app.db.repositories.evaluations import EvaluationsRepository

from app.api.dependencies.database import get_repository
from app.api.dependencies.auth import get_current_active_user
from app.api.dependencies.users import get_user_by_username_from_path
from app.api.dependencies.cleanings import get_cleaning_by_id_from_path
from app.api.dependencies.offers import get_offer_for_cleaning_from_user_by_path


async def check_evaluation_create_permissions(current_user: UserInDB = Depends(get_current_active_user),
                                              cleaning: CleaningInDB = Depends(get_cleaning_by_id_from_path),
                                              cleaner: UserInDB = Depends(get_user_by_username_from_path),
                                              offer: OfferInDB = Depends(get_offer_for_cleaning_from_user_by_path),
                                              eval_repo: EvaluationsRepository = Depends(get_repository(EvaluationsRepository)),) -> None:
    # only onwners of a cleaning can leave evaluations for that cleaning job
    if cleaning.owner != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Users are unable to leave evaluations for cleaning jobs they don't own",)
    # check evals can only be made for jobs that they have accpeted
    if offer.status != "accepted":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Only users with accepted offer can be evalauted.",)
    # check that evals can be who's offer was accepted for that job
    if offer.user_id != cleaner.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="You are not authorized to leave an evaluation for this user",)


# async def list_evaluations_for_cleaner_from_path(cleaner: UserInDB = Depends(get_user_by_username_from_path),
#                                                  evals_repo: EvaluationsRepository = Depends(get_repository(EvaluationsRepository)),) -> List[EvaluationInDB]:
#     return await evals_repo.list_evaluations_for_cleaner(cleaner=cleaner)

async def list_evaluations_for_cleaner_from_path(cleaner: UserInDB = Depends(get_user_by_username_from_path),
                                                 evals_repo: EvaluationsRepository = Depends(get_repository(EvaluationsRepository)),) -> List[EvaluationInDB]:
    return await evals_repo.list_evaluations_for_cleaner(cleaner=cleaner)


async def get_cleaner_evaluation_for_cleaning_from_path(cleaning: CleaningInDB = Depends(get_cleaning_by_id_from_path),
                                                        cleaner: UserInDB = Depends(get_user_by_username_from_path),
                                                        evals_repo: EvaluationsRepository = Depends(get_repository(EvaluationsRepository)),) -> EvaluationInDB:
    evaluation = await evals_repo.get_cleaner_evaluation_for_cleaning(cleaning=cleaning, cleaner=cleaner)
    if not evaluation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No evaluation found for this cleaning.")
    return evaluation
