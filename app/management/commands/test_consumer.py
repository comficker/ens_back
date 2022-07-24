import web3
import pytz
from web3 import Web3
from django.core.management.base import BaseCommand

tz = pytz.UTC
w3 = Web3(Web3.HTTPProvider("https://main-rpc.linkpool.io/"))


class Command(BaseCommand):
    def handle(self, *args, **options):
        x = w3.eth.getTransactionReceipt("0x4328cc31c585d4311e915f26bb0b26dace9b18d24d209f70905c356900f398be")
        print(x)