import logging

from django.core.management.base import BaseCommand

from django_graphql_playground.apps.core.models import Category
from django_graphql_playground.apps.core.models import Ingredient
from django_graphql_playground.apps.pubsub.apps import PubsubConfig
from django_graphql_playground.apps.pubsub.exceps import CorrelationIdMustBeSetException
from django_graphql_playground.apps.pubsub.exceps import FormatNotValidaException
from django_graphql_playground.apps.pubsub.services import consumer
from django_graphql_playground.apps.pubsub.services.consumer import Payload
from django_graphql_playground.settings import MY_DESTINATION
from django_graphql_playground.settings import STOMP_SERVER_HOST
from django_graphql_playground.settings import STOMP_SERVER_PORT
from django_graphql_playground.support.django_helpers import make_sure_database_is_usable
from django_graphql_playground.support.log import do_log_with_correlation_id

logger = logging.getLogger(__name__)


def _listener_callback(payload: Payload):
    make_sure_database_is_usable()

    correlation_id = payload.headers.get("correlation-id")

    if not correlation_id:
        raise CorrelationIdMustBeSetException

    logger.info("A message arrived! Initializing logic...")

    with do_log_with_correlation_id(correlation_id):
        try:
            body = payload.body

            if body.get("categories"):
                logger.info("Persisting categories...")
                for category in body["categories"]:
                    Category.objects.create(**category)
            elif body.get("ingredients"):
                logger.info("Persisting ingredients...")
                for ingredient in body["ingredients"]:
                    Ingredient.objects.create(**ingredient)
            else:
                raise FormatNotValidaException

            payload.ack()
        except:
            logger.exception(f"The following payload could not be consumed: {payload}")
            payload.nack()


connection_params = {"host": STOMP_SERVER_HOST, "port": STOMP_SERVER_PORT, "client_id": PubsubConfig.name}
listener = consumer.build_listener(MY_DESTINATION, _listener_callback, **connection_params)


class Command(BaseCommand):
    help = "Start App consumer"

    def handle(self, *args, **options):
        try:
            logger.info(f"Starting listener...")
            listener.start()
        except BaseException as e:
            logger.exception(f"A exception of type {type(e)} was captured during listener logic")
        finally:
            logger.info(f"Trying to close listener...")
            listener.close()
