import logging

import pytest
from jcp_plus_pulp_client import PULPMonitorClient
from jcp_plus_pulp_server.server import AWFlask

logging.basicConfig(level=logging.WARN)


@pytest.fixture(scope="session")
def app():
    return AWFlask("127.0.0.1", testing=True)


@pytest.fixture(scope="session")
def flask_client(app):
    yield app.test_client()


@pytest.fixture(scope="session")
def jcp_plus_pulp_client():
    # TODO: Could it be possible to write a sisterclass of PULPMonitorClient
    # which calls jcp_plus_pulp_server.api directly? Would it be of use? Would add another
    # layer of integration tests that are actually more like unit tests.
    c = PULPMonitorClient("jcp-plus-pulp-client-test", testing=True)
    yield c

    # Delete test buckets after all tests needing the fixture have been run
    buckets = c.get_buckets()
    for bucket_id in buckets:
        if bucket_id.startswith("test-"):
            c.delete_bucket(bucket_id)
