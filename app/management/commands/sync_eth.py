import json
import pytz
from datetime import datetime
from web3 import Web3
from django.core.management.base import BaseCommand

tz = pytz.UTC
w3 = Web3(Web3.HTTPProvider("https://main-rpc.linkpool.io/"))

with open("abi/api.json") as f:
    ABI_NFT_721 = json.load(f)

START_BLOCK_ENV = 9380410
TOKEN_NFT = Web3.toChecksumAddress("0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85")

CONTRACT_NFT = w3.eth.contract(
    address=TOKEN_NFT,
    abi=ABI_NFT_721
)


def get_block_datetime(event):
    block = w3.eth.get_block(event['blockNumber'])
    timestamp = block.timestamp
    block_datetime = datetime.fromtimestamp(timestamp, tz)
    return block_datetime


def get_block_all_entries(block_filter):
    return block_filter.get_all_entries()


def get_tx_receipt(event):
    return w3.eth.waitForTransactionReceipt(event['transactionHash'])


def get_latest_block():
    return w3.eth.get_block('latest').get("number")


def sync_event_nft(block_filter):
    try:
        event_entries = get_block_all_entries(block_filter)
        event_entries = list({v['transactionHash'].hex(): v for v in event_entries}.values())
        for event in event_entries:
            tx_hash = event['transactionHash'].hex()
            receipt = get_tx_receipt(event)
            block_datetime = get_block_datetime(event=event)
            for res in CONTRACT_NFT.events.NameRegistered().processReceipt(receipt):
                print(json.loads(Web3.toJSON(res['args'])))
                print(tx_hash)
                print(block_datetime)
        return True
    except Exception as e:
        print(e)
        return False


class Command(BaseCommand):
    def handle(self, *args, **options):
        new_transaction_filter = w3.eth.filter('pending')
        new_transaction_filter.get_new_entries()