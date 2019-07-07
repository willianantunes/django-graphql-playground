from io import StringIO

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.management import CommandError
from django.core.management import call_command
from django_graphql_playground.apps.core.models import Category
from django_graphql_playground.apps.core.models import Ingredient


@pytest.mark.django_db
def test_should_seed_db_without_super_user():
    out = StringIO()

    call_command("seed_db", stdout=out)

    assert out.getvalue() == "Creating categories\nCreating ingredients\n"
    assert Category.objects.all().count() == 2
    assert Ingredient.objects.all().count() == 4


@pytest.mark.django_db
def test_should_seed_db_with_super_user_given_extra_option():
    out = StringIO()

    call_command("seed_db", "--create-super-user", stdout=out)

    assert (
        out.getvalue()
        == "Creating ADMIN username admin and password Asd123!.\nCreating categories\nCreating ingredients\n"
    )
    assert User.objects.filter(username="admin").count() == 1
    assert Category.objects.all().count() == 2
    assert Ingredient.objects.all().count() == 4


@pytest.mark.django_db
def test_should_seed_db_with_super_user_hidding_password_given_extra_option():
    out = StringIO()

    call_command("seed_db", "--create-super-user", "--hide-super-user-password", stdout=out)

    assert out.getvalue() == "Creating ADMIN username admin\nCreating categories\nCreating ingredients\n"
    assert User.objects.filter(username="admin").count() == 1
    assert Category.objects.all().count() == 2
    assert Ingredient.objects.all().count() == 4


@pytest.mark.django_db
def test_should_seed_db_with_custom_super_user_given_extra_options():
    out = StringIO()
    custom_username = "xpto"

    call_command("seed_db", "--create-super-user", f"-u {custom_username}", stdout=out)

    assert (
        out.getvalue() == f"Creating ADMIN username {custom_username} and password Asd123!.\n"
        f"Creating categories\n"
        f"Creating ingredients\n"
    )
    assert User.objects.filter(username=custom_username).count() == 1
    assert Category.objects.all().count() == 2
    assert Ingredient.objects.all().count() == 4


@pytest.mark.django_db
def test_should_inform_if_super_user_exists():
    out = StringIO()
    custom_username = "xpto"
    get_user_model().objects.create_superuser(custom_username, None, "fake-password")

    call_command("seed_db", "--create-super-user", f"-u {custom_username}", stdout=out)

    assert out.getvalue() == "Super user already exists\nCreating categories\nCreating ingredients\n"


@pytest.mark.django_db
def test_should_only_create_super_user_given_extra_options():
    out = StringIO()

    call_command("seed_db", "--create-super-user", "--only-super-user", stdout=out)

    assert out.getvalue() == "Creating ADMIN username admin and password Asd123!.\n"
    assert User.objects.filter(username="admin").count() == 1
    assert Category.objects.all().count() == 0
    assert Ingredient.objects.all().count() == 0
