import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import Base, get_db

# Import all models so Base.metadata knows about them
from app.users.model import User
from app.student_profiles.model import StudentProfile
from app.subjects.model import Subject
from app.study_plans.model import StudyPlan
from app.study_plan_subjects.model import StudyPlanSubject
from app.study_sessions.model import StudySession
from app.core.security import hash_password, create_access_token

from sqlalchemy.pool import StaticPool

# Use SQLite in memory for speed
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function", autouse=True)
def setup_db():
    # Setup: creates all tables
    Base.metadata.create_all(bind=engine)
    yield
    # Teardown: drops all tables
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    # Provide a new session per test
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def override_get_db(db_session):
    def _override_get_db():
        yield db_session
    return _override_get_db

@pytest.fixture
def client(override_get_db):
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
        
    app.dependency_overrides.clear()

@pytest.fixture
def user_a(db_session):
    user = db_session.query(User).filter_by(email="usera@test.com").first()
    if not user:
        user = User(name="User A", email="usera@test.com", password_hash=hash_password("senha123"))
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
    return user

@pytest.fixture
def user_b(db_session):
    user = db_session.query(User).filter_by(email="userb@test.com").first()
    if not user:
        user = User(name="User B", email="userb@test.com", password_hash=hash_password("senha123"))
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
    return user

@pytest.fixture
def token_a(user_a):
    return create_access_token({"sub": str(user_a.id)})

@pytest.fixture
def token_b(user_b):
    return create_access_token({"sub": str(user_b.id)})

@pytest.fixture
def headers_a(token_a):
    return {"Authorization": f"Bearer {token_a}"}

@pytest.fixture
def headers_b(token_b):
    return {"Authorization": f"Bearer {token_b}"}

@pytest.fixture
def subject_1(db_session):
    subject = db_session.query(Subject).filter_by(name="Matemática").first()
    if not subject:
        subject = Subject(name="Matemática", description="Matemática Básica")
        db_session.add(subject)
        db_session.commit()
        db_session.refresh(subject)
    return subject
