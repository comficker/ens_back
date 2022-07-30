from django.db import models


# Create your models here.

class Contract(models.Model):
    chain_id = models.CharField(max_length=50, default="eth")
    address = models.CharField(max_length=50, null=True, blank=True)

    name = models.CharField(max_length=120)
    desc = models.CharField(max_length=500, null=True, blank=True)
    meta = models.JSONField(null=True, blank=True)

    token_schema = models.CharField(max_length=50, default="erc721")
    token_symbol = models.CharField(max_length=50, blank=True, null=True)
    total_supply = models.IntegerField(default=0)
    init_price = models.FloatField(default=0)
    payment_symbol = models.CharField(max_length=50, default="ETH")
    mint_date = models.DateTimeField(null=True, blank=True)
    links = models.JSONField(null=True, blank=True)


class Asset(models.Model):
    contract = models.ForeignKey(Contract, related_name="assets", on_delete=models.CASCADE)
    item_id = models.CharField(max_length=500, db_index=True)
    uri = models.CharField(max_length=500, null=True, blank=True)

    name = models.CharField(max_length=500)
    desc = models.CharField(max_length=500, null=True, blank=True)
    meta = models.JSONField(null=True, blank=True)

    traits = models.JSONField(null=True, blank=True)
    links = models.JSONField(null=True, blank=True)
    owner = models.CharField(max_length=50)
    mint_date = models.DateTimeField(null=True, blank=True)
    expired_date = models.DateTimeField(null=True, blank=True)
    tx_hashes = models.JSONField(null=True, blank=True)
    current_price = models.FloatField(default=0)


class Transaction(models.Model):
    timestamp = models.DateTimeField(null=True, blank=True)
    tx_hash = models.CharField(max_length=256, db_index=True)

    asset = models.ForeignKey(Asset, related_name="transactions", on_delete=models.CASCADE)
    event_name = models.CharField(max_length=50)
    fr = models.CharField(max_length=42)
    to = models.CharField(max_length=42)
    price = models.FloatField(default=0)


class SystemConfig(models.Model):
    key = models.CharField(max_length=50, unique=True)
    value = models.CharField(max_length=50)
    meta = models.JSONField(null=True, blank=True)


class Report(models.Model):
    created = models.DateField()
    minted = models.IntegerField(default=0)
    trade = models.IntegerField(default=0)
