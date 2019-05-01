import logging

from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.signals import user_logged_out
from django.contrib.auth.signals import user_login_failed
from django.dispatch import receiver

from django_graphql_playground.support.utils import retrieve_ip_address

logger = logging.getLogger(__name__)


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    ip_address = retrieve_ip_address(request)
    logger.info(f"The following user has logged from address {ip_address}: {user.username}")


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    logger.info(f"The following user has logged out: {user.username}")


@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, request, **kwargs):
    logger.info(f"Someone attempt to login with: {credentials['username']}")
