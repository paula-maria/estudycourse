import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import Base, get_db
from app.core.security import get_current_user

# Import all models so Base.metadata knows about them
from app.users.model import User
from app.student_profiles.model import StudentProfile
from app.subjects.model import Subject
from app.study_plans.model import StudyPlan
from app.study_plan_subjects.model import StudyPlanSubject
from app.study_sessions.model import StudySession

from sqlalchemy.pool import StaticPool

# Use SQLite in memory for speed
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
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
def override_get_current_user():
    def _override_get_current_user():
        # Create a mock user for testing authentication
        return User(id=1, email="test@test.com", name="Test User")
    return _override_get_current_user

@pytest.fixture
def client(override_get_db, override_get_current_user):
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    
    with TestClient(app) as test_client:
        yield test_client
        
    app.dependency_overrides.clear()
