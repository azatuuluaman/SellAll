from django.core.management.base import BaseCommand
from argparse import RawTextHelpFormatter

from advertisement.management.parser.house_kg import main_house


class Command(BaseCommand):
    help = 'Start Parsing'

    def handle(self, *args, **options):
        main_house()

    def add_arguments(self, parser):
        parser.add_argument(
            '-s',
            '--short',
            action='store_true',
            default=False,
            help='Вывод короткого сообщения'
        )
        parser.add_argument(
            '-p',
            '--parser',
            action='store_true',
            default=False,
            help='Вывод короткого сообщения'
        )

    def create_parser(self, prog_name, subcommand, **kwargs):
        parser = super(Command, self).create_parser(prog_name, subcommand)
        parser.formatter_class = RawTextHelpFormatter
        return parser
