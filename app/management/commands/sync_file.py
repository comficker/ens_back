import datetime

from django.core.management.base import BaseCommand
from app.models import Asset, Contract, Transaction, Report
from django.utils import timezone


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
        file = open('/Users/hoanganhlam/WebstormProjects/crawl-nft/data_fixed/{}.txt'.format(options['q']), 'r')
        lines = file.readlines()
        count = 0
        start = True
        for line in lines:
            count = count + 1
            text = line.strip()
            arr = text.split("|")
            timestamp = datetime.datetime.fromtimestamp(int(arr[0]), timezone.timezone.utc)
            blockNumber = arr[1]
            transactionHash = arr[2]
            transactionIndex = arr[3]
            name = arr[4]
            label = arr[5]
            owner = arr[6]
            cost = arr[7]
            expires = arr[8]
            item_id = int(label, 16)
            if not start and name == "777⁄777":
                start = True
                continue
            if not start:
                continue
            if len(name) > 500:
                print(transactionHash)
                name = name[:32]
            a, is_created = Asset.objects.get_or_create(
                contract=contract,
                name=name.replace("\x00", ""),
                item_id=item_id,
                defaults={
                    "tx_hashes": [transactionHash],
                    "mint_date": timestamp
                }
            )
            if expires:
                a.expired_date = datetime.datetime.fromtimestamp(int(expires), timezone.timezone.utc)
            a.current_price = cost
            a.owner = owner
            if transactionHash not in a.tx_hashes:
                a.tx_hashes.append(transactionHash)
            tx, tx_created = Transaction.objects.get_or_create(
                tx_hash=transactionHash,
                defaults={
                    "event_name": "minted",
                    "asset": a,
                    "fr": "0x0000000000000000000000000000000000000000",
                    "to": owner,
                    "price": cost,
                    "timestamp": timestamp
                }
            )
            if tx_created:
                t, r_created = Report.objects.get_or_create(created=timestamp.date())
                t.minted = t.minted + 1
                t.save()
            a.save()
        print(count)
# 9456759|
# 0x4605808100386cfd319b663a80f92a0712f9ed34a8c0f5783a77632f68766981
# |22|
# 4play|
# 0x950b9c3f72c4a6b9bfde6e77cdf0d41a7599b7305dcd1e4f65116346f1f149da|
# 0xD53d5eA1C50CAe08bf29566bB9060b88146e7c40|
# 22335759995597450|
# 1612915685
