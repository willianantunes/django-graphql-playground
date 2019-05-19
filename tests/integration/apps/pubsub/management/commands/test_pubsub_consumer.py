import time
import uuid

import pytest

from django_graphql_playground.apps.core.models import Category
from django_graphql_playground.apps.pubsub.management.commands import pubsub_consumer
from django_graphql_playground.apps.pubsub.services import producer
from django_graphql_playground.settings import MY_DESTINATION
from django_graphql_playground.settings import STOMP_SERVER_HOST
from django_graphql_playground.settings import STOMP_SERVER_PORT


@pytest.fixture
def configured_publisher():
    connection_params = {"host": STOMP_SERVER_HOST, "port": STOMP_SERVER_PORT}
    testing_publisher = producer.build_publisher(MY_DESTINATION, **connection_params)

    testing_publisher.start()

    yield testing_publisher

    testing_publisher.close()


@pytest.mark.django_db(transaction=True)
def test_should_persist_category_when_valid_payload_is_received(configured_publisher):
    configured_listener = pubsub_consumer.listener

    assert Category.objects.all().count() == 0

    sample_body = {"categories": [{"name": "Mortal Kombat"}, {"name": "Sal Paradise"}, {"name": "Jafar"}]}
    sample_header = {"correlation-id": uuid.uuid4()}

    configured_listener.start(block=False)
    configured_publisher.send(sample_body, sample_header)
    # TODO: Implement something like threading.Condition() looking at stomp.listener.TestListener
    time.sleep(2)
    configured_listener.close()

    assert Category.objects.all().count() == 3
    assert Category.objects.filter(name__exact="Mortal Kombat").count() == 1
    assert Category.objects.filter(name__exact="Sal Paradise").count() == 1
    assert Category.objects.filter(name__exact="Jafar").count() == 1
