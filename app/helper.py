import datetime
from app.models import Asset, Transaction, Report
from django.utils import timezone


def save_line(line, contract):
    text = line.strip()
    arr = text.split("|")
    if len(arr) < 7:
        return
    timestamp = datetime.datetime.fromtimestamp(int(arr[0]), timezone.timezone.utc) if arr[0] != '' else None
    transactionHash = arr[2]
    name = arr[4]
    label = arr[5]
    owner = arr[6]
    cost = arr[7]
    expires = arr[8]
    item_id = int(label, 16)
    if len(name) > 500:
        print(transactionHash)
        name = name[:32]
    a, is_created = Asset.objects.get_or_create(
        item_id=item_id,
        defaults={
            "contract": contract,
            "name": name.replace("\x00", ""),
            "tx_hashes": [transactionHash],
            "mint_date": timestamp
        }
    )
    if expires:
        a.expired_date = datetime.datetime.fromtimestamp(int(expires), timezone.timezone.utc)
    a.last_block = int(arr[1])
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
    if tx_created and timestamp:
        t, r_created = Report.objects.get_or_create(created=timestamp.date())
        t.minted = t.minted + 1
        t.save()
    a.save()
