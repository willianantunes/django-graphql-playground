from datetime import date

import pytest
from dateutil import relativedelta
from django.core.management import call_command
from django.utils import timezone

from django_graphql_playground.apps.core.models import Category
from django_graphql_playground.support.utils import get_first_day
from django_graphql_playground.support.utils import get_last_day

day_from_previous_month = date.today() + relativedelta.relativedelta(months=-1)
first_day_of_previous_month, last_day_of_previous_month = (
    get_first_day(day_from_previous_month),
    get_last_day(day_from_previous_month),
)


@pytest.mark.django_db
def test_should_send_expired_categories__given_they_werent_distributed_yet():
    Category.objects.create(
        name="Mortal Kombat", start_at=first_day_of_previous_month, end_at=last_day_of_previous_month
    )
    Category.objects.create(
        name="Sal Paradise",
        start_at=first_day_of_previous_month,
        end_at=last_day_of_previous_month,
        distributed_at=timezone.now(),
    )

    assert Category.objects.filter(distributed_at__isnull=False).count() == 1

    call_command("pubsub_producer")

    assert Category.objects.filter(distributed_at__isnull=False).count() == 2
