import csv
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User


class Command(BaseCommand):
    """
    management command for importing user data from csv file
    """
    help = 'To import user details'

    def add_arguments(self, parser):
        parser.add_argument('--file_path', type=str)

    def handle(self, *args, **options):
        """
        Function for recovering the user detail data from a csv file
        :param args:
        :param options:
        :return:
        """
        export_file = "user_data.csv"
        if export_file in options['file_path']:
            try:
                with open(export_file, mode="r") as user_file:
                    reader = csv.DictReader(user_file)
                    for row in reader:
                        User.objects.create_user(**row)
            except FileNotFoundError:
                raise CommandError('Use the correct file for importing')

        self.stdout.write(self.style.SUCCESS('Successfully recovered the user data from "user_data.csv"'))
