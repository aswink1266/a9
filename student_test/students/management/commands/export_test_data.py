from django.core.management.base import BaseCommand,CommandError
import csv
from django.contrib.auth.models import User


class Command(BaseCommand):
    """
    management command for exporting test attempt data and user data to csv file
    """
    help = 'storing the user detail data as csv'

    def add_arguments(self, parser):
        parser.add_argument('--file_path', type=str)

    def handle(self, *args, **options):
        """
        Function for writing the user detail data into a csv file
        :param args:
        :param options:
        :return:
        """
        user_data = User.objects.get(username='anjus')
        # Saving the user data into a csv file
        export_file = options['file_path']
        if not export_file:
            export_file = "test_user_data.csv"
        with open(export_file, mode="w") as file:
            fieldnames = ['first_name', 'last_name', 'username', 'email', 'password']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            data_dictionary = {'first_name': user_data.first_name,
                               'last_name': user_data.last_name,
                               'username': user_data.username,
                               'email': user_data.email,
                               'password': 'pass1234',
                               }
            writer.writerow(data_dictionary)
        self.stdout.write(self.style.SUCCESS('Successfully saved the user data in "%s"' % export_file))
