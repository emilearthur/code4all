import os
import warnings
import random

from typing import List, Callable

import pytest
from asgi_lifespan import LifespanManager

from fastapi import FastAPI
from httpx import AsyncClient
from databases import Database

import alembic
from alembic.config import Config

from app.models.user import UserCreate, UserInDB
from app.models.cleaning import CleaningCreate, CleaningInDB
from app.models.offer import OfferCreate, OfferUpdate
from app.models.evaluation import EvaluationCreate

from app.db.repositories.users import UsersRepository
from app.db.repositories.cleanings import CleaningsRepository
from app.db.repositories.offers import OffersRepository
from app.db.repositories.evaluations import EvaluationsRepository

from app.services import auth_service
from app.core.config import SECRET_KEY, JWT_TOKEN_PREFIX


# apply migrations at beginning and end of testing session
@pytest.fixture(scope="session")
def apply_migrations():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    os.environ["TESTING"] = "1"
    config = Config("alembic.ini")
    alembic.command.upgrade(config, "head")
    yield
    alembic.command.downgrade(config, "base")


# create a new application for testing
@pytest.fixture
def app(apply_migrations: None) -> FastAPI:
    from app.api.server import get_application
    return get_application()


# Grab a reference to our db  when needed
@pytest.fixture
def db(app: FastAPI) -> Database:
    return app.state._db


# make requests in our test
@pytest.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url="http://testserver",
            headers={"Content-Type": "application/json"}
        ) as client:
            yield client


@pytest.fixture
def new_cleaning():
    return CleaningCreate(
        name="test cleaning",
        description="test description",
        price=10.00,
        cleaning_type="spot_clean")


@pytest.fixture
async def test_cleanings_list(db: Database, test_user2: UserInDB) -> List[CleaningInDB]:
    cleaning_repo = CleaningsRepository(db)
    return [await cleaning_repo.create_cleaning(new_cleaning=CleaningCreate(name=f"test cleaning {i}",
                                                description="test description", price=20.00,
                                                cleaning_type="full_clean"), requesting_user=test_user2,) for i in range(5)]


@pytest.fixture
async def test_cleaning(db: Database, test_user: UserInDB) -> CleaningInDB:
    cleaning_repo = CleaningsRepository(db)
    new_cleaning = CleaningCreate(
        name="fake cleaning name",
        description="fake cleaning description",
        price=9.99,
        cleaning_type="spot_clean",
    )
    return await cleaning_repo.create_cleaning(new_cleaning=new_cleaning, requesting_user=test_user)


@pytest.fixture
async def test_user(db: Database) -> UserInDB:
    new_user = UserCreate(email="emilextrigxxp@gmail.com",
                          username="emilextrigxxp",
                          password="emilextrigxxp",)
    user_repo = UsersRepository(db)

    existing_user = await user_repo.get_user_by_email(email=new_user.email)
    if existing_user:
        return existing_user
    return await user_repo.register_new_user(new_user=new_user)


@pytest.fixture
async def test_user2(db: Database) -> UserInDB:
    new_user = UserCreate(
        email="gethost@gmail.com",
        username="gethost",
        password="gethost",
    )
    user_repo = UsersRepository(db)

    existing_user = await user_repo.get_user_by_email(email=new_user.email)
    if existing_user:
        return existing_user
    return await user_repo.register_new_user(new_user=new_user)


@pytest.fixture
def authorized_client(client: AsyncClient, test_user: UserInDB) -> AsyncClient:
    access_token = auth_service.create_access_token_for_user(user=test_user, secret_key=str(SECRET_KEY))
    client.headers = {
        **client.headers, "Authorization": f"{JWT_TOKEN_PREFIX} {access_token}"
    }
    return client


async def user_fixture_helper(*, db: Database, new_user: UserCreate) -> UserInDB:
    user_repo = UsersRepository(db)
    existing_user = await user_repo.get_user_by_email(email=new_user.email)
    if existing_user:
        return existing_user
    return await user_repo.register_new_user(new_user=new_user)


@pytest.fixture
async def test_user(db: Database) -> UserInDB:
    new_user = UserCreate(email="emilextrigxxp@gmail.com", username="emilextrigxxp",
                          password="emilextrigxxp",)
    return await user_fixture_helper(db=db, new_user=new_user)


@pytest.fixture
async def test_user2(db: Database) -> UserInDB:
    new_user = UserCreate(email="gethost@gmail.com", username="gethost", password="gethost",)
    return await user_fixture_helper(db=db, new_user=new_user)


@pytest.fixture
async def test_user3(db: Database) -> UserInDB:
    new_user = UserCreate(email="ato@gmail.com", username="atom", password="atomain",)
    return await user_fixture_helper(db=db, new_user=new_user)


@pytest.fixture
async def test_user4(db: Database) -> UserInDB:
    new_user = UserCreate(email="dan@gmail.com", username="dan", password="danmain")
    return await user_fixture_helper(db=db, new_user=new_user)


@pytest.fixture
async def test_user5(db: Database) -> UserInDB:
    new_user = UserCreate(email="pope@ux.io", username="pope", password="morepope")
    return await user_fixture_helper(db=db, new_user=new_user)


@pytest.fixture
async def test_user6(db: Database) -> UserInDB:
    new_user = UserCreate(email="shamsu@xxx.io", username="shamsu", password="shamsumain")
    return await user_fixture_helper(db=db, new_user=new_user)


@pytest.fixture
async def test_user_list(test_user3: UserInDB, test_user4: UserInDB,
                         test_user5: UserInDB, test_user6: UserInDB,) -> List[UserInDB]:
    return [test_user3, test_user4, test_user5, test_user6]


@pytest.fixture
def create_authorized_client(client: AsyncClient) -> Callable:
    def _create_authorized_client(*, user: UserInDB) -> AsyncClient:
        access_token = auth_service.create_access_token_for_user(user=user, secret_key=str(SECRET_KEY))
        client.headers = {**client.headers, "Authorization": f"{JWT_TOKEN_PREFIX} {access_token}", }
        return client
    return _create_authorized_client


@pytest.fixture
async def test_cleaning_with_offers(db: Database, test_user2: UserInDB, test_user_list: List[UserInDB]) -> CleaningInDB:
    cleaning_repo = CleaningsRepository(db)
    offers_repo = OffersRepository(db)
    new_cleaning = CleaningCreate(name="cleaning with offers", description="desc for cleaning",
                                  price=9.99, cleaning_type="full_clean",)

    created_cleaning = await cleaning_repo.create_cleaning(new_cleaning=new_cleaning, requesting_user=test_user2)
    for user in test_user_list:
        await offers_repo.create_offer_for_cleaning(new_offer=OfferCreate(cleaning_id=created_cleaning.id, user_id=user.id))
    return created_cleaning


@pytest.fixture
async def test_cleaning_with_accepted_offer(db: Database, test_user2: UserInDB,
                                            test_user3: UserInDB,
                                            test_user_list: List[UserInDB]) -> CleaningInDB:
    cleaning_repo = CleaningsRepository(db)
    offers_repo = OffersRepository(db)
    new_cleaning = CleaningCreate(name="cleaning with offers", description="desc for cleaning",
                                  price=2.99, cleaning_type="full_clean",)
    created_cleaning = await cleaning_repo.create_cleaning(new_cleaning=new_cleaning,
                                                           requesting_user=test_user2)
    offers = []
    for user in test_user_list:
        offers.append(await offers_repo.create_offer_for_cleaning(new_offer=OfferCreate(cleaning_id=created_cleaning.id, user_id=user.id)))
    await offers_repo.accept_offer(offer=[offer for offer in offers if offer.user_id == test_user3.id][0],
                                   offer_update=OfferUpdate(status="accepted"))
    return created_cleaning


async def create_cleaning_with_evaluation_offer_helper(db: Database, owner: UserInDB,
                                                       cleaner: UserInDB, cleaning_create: CleaningCreate,
                                                       evaluation_create: EvaluationCreate) -> CleaningInDB:
    cleaning_repo = CleaningsRepository(db)
    offers_repo = OffersRepository(db)
    evals_repo = EvaluationsRepository(db)

    created_cleaning = await cleaning_repo.create_cleaning(new_cleaning=cleaning_create, requesting_user=owner)
    offer = await offers_repo.create_offer_for_cleaning(new_offer=OfferCreate(cleaning_id=created_cleaning.id,
                                                        user_id=cleaner.id))
    await offers_repo.accept_offer(offer=offer, offer_update=OfferUpdate(status="accepted"))
    await evals_repo.create_evaluation_for_cleaner(evaluation_create=evaluation_create,
                                                   cleaning=created_cleaning,
                                                   cleaner=cleaner,)
    return created_cleaning


@pytest.fixture
async def test_list_of_cleanings_with_evaluated_offer(db: Database, test_user2: UserInDB,
                                                      test_user3: UserInDB,) -> List[CleaningInDB]:
    return [await create_cleaning_with_evaluation_offer_helper(db=db, owner=test_user2,
                                                               cleaner=test_user3,
                                                               cleaning_create=CleaningCreate(name=f"test cleaning - {i}",
                                                                                              description=f"test description - {i}",
                                                                                              price=float(f"{i}9.99"),
                                                                                              cleaning_type="full_clean",),
                                                               evaluation_create=EvaluationCreate(professionalism=random.randint(0, 5),
                                                                                                  completeness=random.randint(0, 5),
                                                                                                  efficiency=random.randint(0, 5),
                                                                                                  overall_rating=random.randint(0, 5),
                                                                                                  headline=f"test headline - {i}",
                                                                                                  comment=f"test comment - {i}",),)
            for i in range(5)]
