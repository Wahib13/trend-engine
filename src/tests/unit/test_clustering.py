from inference.main import run_clustering
from tests.conftest import FakeTopicModel


def test_basic_clustering(
        populated_db_session,
        db_session
):
    model = FakeTopicModel()
    run_clustering(db_session, model)
