import pytest
from _pytest.logging import LogCaptureFixture
from django.contrib.auth import get_user_model
from django.test import Client


@pytest.mark.django_db
def test_should_log_username_when_one_logged_in_and_logged_out(caplog: LogCaptureFixture):
    fake_admin_user = "fake-admin-user"
    fake_admin_user_password = "fake-admin-user-password"
    get_user_model().objects.create_superuser(fake_admin_user, None, fake_admin_user_password)

    client = Client()
    client.login(username=fake_admin_user, password=fake_admin_user_password)

    assert len(caplog.records) == 1
    assert caplog.records[0].message == f"The following user has logged from address 127.0.0.1: {fake_admin_user}"

    client.logout()

    assert len(caplog.records) == 2
    assert caplog.records[1].message == f"The following user has logged out: {fake_admin_user}"


@pytest.mark.django_db
def test_should_log_attempt_when_user_failed_to_login(caplog: LogCaptureFixture):
    client = Client()
    client.login(username="salt", password="foo")

    assert len(caplog.records) == 1
    assert caplog.records[0].message == f"Someone attempt to login with: salt"
