from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.core.management import CommandError

from django_graphql_playground.apps.core.models import Category
from django_graphql_playground.apps.core.models import Ingredient


class Command(BaseCommand):
    help = "Seed database with sample data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--create-super-user", action="store_true", dest="create_super_user", help="Create default super user"
        )
        parser.add_argument(
            "-u", dest="admin_username", type=str, default="admin", help="Super user username. Defaults to: admin "
        )
        parser.add_argument(
            "-p",
            dest="admin_password",
            type=str,
            default="Asd123!.",
            help="Super user password. Defaults to: Asd123!. ",
        )

    def handle(self, *args, **options):
        self.create_super_user = options["create_super_user"]
        self.admin_username = options["admin_username"].strip()
        self.admin_password = options["admin_password"].strip()

        if self.create_super_user == True:
            user_model = get_user_model()
            if user_model.objects.filter(username=self.admin_username).count() == 0:
                self.stdout.write(f"Creating with username {self.admin_username} and password {self.admin_password}")
                get_user_model().objects.create_superuser(self.admin_username, None, self.admin_password)
            else:
                raise CommandError(f"Super user {self.admin_username} already exists")

        if Category.objects.all().count() == 0 and Ingredient.objects.all().count() == 0:
            self.stdout.write(f"Creating categories")
            category_one = Category.objects.create(name="Category XPTO")
            category_two = Category.objects.create(name="Category QWERTY")
            self.stdout.write(f"Creating ingredients")
            Ingredient.objects.create(name="Salt", notes=None, category=category_one)
            Ingredient.objects.create(name="Oregano", notes=None, category=category_one)
            Ingredient.objects.create(name="Cumin", notes=None, category=category_one)
            Ingredient.objects.create(name="Chive", notes=None, category=category_two)
        else:
            self.stdout.write(f"There are categories and ingredients already")
