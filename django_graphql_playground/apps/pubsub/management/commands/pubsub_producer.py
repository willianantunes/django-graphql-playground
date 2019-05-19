import logging
import uuid

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from django_graphql_playground.apps.core.models import Category
from django_graphql_playground.apps.pubsub.apps import PubsubConfig
from django_graphql_playground.apps.pubsub.services import producer
from django_graphql_playground.settings import STOMP_SERVER_HOST
from django_graphql_playground.settings import STOMP_SERVER_PORT
from django_graphql_playground.settings import TARGET_DESTINATION

logger = logging.getLogger(__name__)

connection_params = {"host": STOMP_SERVER_HOST, "port": STOMP_SERVER_PORT, "client_id": PubsubConfig.name}
capitol_publisher = producer.build_publisher(TARGET_DESTINATION, **connection_params)


class Command(BaseCommand):
    help = "Start App producer"

    def handle(self, *args, **options):
        logger.info("Getting all categories to publish them...")
        categories = Category.objects.filter(end_at__lt=timezone.now(), distributed_at__isnull=True).values()

        logger.info(f"There are {categories.count()} categories to be sent")

        correlation_id = uuid.uuid4()
        logger.info(f"Correlation ID created: {correlation_id}")
        standard_header = {"correlation-id": correlation_id}

        with transaction.atomic():
            with producer.do_inside_transaction(capitol_publisher):
                for category in categories:
                    capitol_publisher.send(category, standard_header)
                categories.update(distributed_at=timezone.now())
