from django.core.management.base import BaseCommand,CommandError
import csv
from students.models import TestAttempt


class Command(BaseCommand):
    """
    management command for exporting test attempt data and user data to csv file
    """
    help = 'storing the test attempt data as csv'

    def add_arguments(self, parser):
        parser.add_argument('--file_path', type=str)

    def handle(self, *args, **options):
        """
        Function for writing test attempt detail data into a csv file
        :param args:
        :param options:
        :return:
        """
        test_attempt_data = TestAttempt.objects.all()
        # Writing the test attempt data into a csv file
        export_file = options['file_path']
        if not export_file:
            export_file = "test_attempt_data.csv"
        with open(export_file, mode="w") as file:
            fieldnames = ['full_name', 'test_name', 'marks']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for attempt in test_attempt_data:
                data_dictionary = {'full_name': attempt.user.get_full_name(),
                                   'test_name': attempt.test.test_name,
                                   'marks': attempt.marks}
                writer.writerow(data_dictionary)

        self.stdout.write(self.style.SUCCESS('Successfully saved the test attempt data in "%s"' % export_file))
