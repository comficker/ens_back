from django.core.management.base import BaseCommand
from app.models import Contract
from app.helper import save_line


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--q')

    def handle(self, *args, **options):
        contract, _ = Contract.objects.get_or_create(
            address="0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85",
            chain_id="ethereum",
            defaults={
                "name": "Ethereum Name Service"
            }
        )
        file = open(options['q'], 'r')
        lines = file.readlines()
        count = 0
        start = True
        for line in lines:
            count = count + 1
            text = line.strip()
            arr = text.split("|")
            name = arr[4]
            if not start and name == "777⁄777":
                start = True
                continue
            if not start:
                continue
            save_line(line, contract)
