from django.core.management.base import BaseCommand
from argparse import RawTextHelpFormatter

from advertisement.tasks import parse_house_kg, parse_doska, parse_salexy


class Command(BaseCommand):
    help = 'Start Parsing'

    def handle(self, *args, **options):
        site = options.get('site')
        start = options.get('start_page')
        end = options.get('end_page')

        parsers = {
            'house_kg': parse_house_kg.delay,
            'doska': parse_doska.delay,
            'salexy': parse_salexy.delay
        }

        if site in parsers:
            parsers[site](start, end)

    def add_arguments(self, parser):
        parser.add_argument(
            '-s',
            '--sites',
            type=str,
        )
        parser.add_argument(
            '-sp',
            '--start_page',
            type=int,
            default=1
        )
        parser.add_argument(
            '-ep',
            '--end_page',
            type=int,
            default=10
        )

    def create_parser(self, prog_name, subcommand, **kwargs):
        parser = super(Command, self).create_parser(prog_name, subcommand)
        parser.formatter_class = RawTextHelpFormatter
        return parser
