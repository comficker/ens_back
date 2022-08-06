import json
import base64
import datetime
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.utils.urls import remove_query_param, replace_query_param
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from app import serializers
from app.models import Asset, Contract, Transaction, Report
from eth_account.messages import defunct_hash_message
from web3 import Web3
from collections import OrderedDict
from django.utils import timezone
from app.helper import save_line

class Pagination(PageNumberPagination):
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('most_rarity', self.most_rarity if hasattr(self, 'most_rarity') else None),
            ('most_expensive', self.most_expensive if hasattr(self, 'most_expensive') else None),
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))

    def get_next_link(self):
        if not self.page.has_next():
            return None
        page_number = self.page.next_page_number()
        return replace_query_param("", self.page_query_param, page_number)

    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        page_number = self.page.previous_page_number()
        if page_number == 1:
            return remove_query_param("", self.page_query_param)
        return replace_query_param("", self.page_query_param, page_number)


class AssetFilter(filters.FilterSet):
    start = filters.CharFilter(field_name="name", lookup_expr='startswith')

    class Meta:
        model = Asset
        fields = ['name']


class AssetViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    models = Asset
    queryset = models.objects.order_by('-id')
    serializer_class = serializers.AssetSerializer
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = AssetFilter
    ordering_fields = ['id', 'mint_date', 'expired_date', 'current_price']
    lookup_field = "id"
    search_fields = ['name']

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        tx = Transaction.objects.filter(asset=instance)
        out = {
            **serializer.data,
            "transactions": serializers.TransactionSerializer(tx, many=True).data
        }
        return Response(out)


class ContractViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    models = Contract
    queryset = models.objects.order_by('-id').distinct()
    serializer_class = serializers.ContractSerializer
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['assets__owner']
    lookup_field = "address"


class TransactionViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    models = Transaction
    queryset = models.objects.order_by('-timestamp').distinct()
    serializer_class = serializers.TransactionSerializer
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['asset']
    lookup_field = "pk"


class ReportFilter(filters.FilterSet):
    start = filters.CharFilter(field_name="created", lookup_expr='gte')
    end = filters.CharFilter(field_name="created", lookup_expr='lte')

    class Meta:
        model = Report
        fields = []


class ReportViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    models = Report
    queryset = models.objects.order_by('created').distinct()
    serializer_class = serializers.ReportSerializer
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReportFilter
    lookup_field = "pk"


@api_view(['POST'])
def update_trait(request):
    w3 = Web3(Web3.HTTPProvider(request.data.get("rpc")))
    sign_mess = request.data.get("message")
    signature = request.data.get("signature")
    message_hash = defunct_hash_message(text=sign_mess)
    address = w3.eth.account.recoverHash(message_hash, signature=signature)
    decoded = base64.b64decode(sign_mess)
    m_json = json.loads(decoded)
    if address == request.wallet.address and m_json.get("id"):
        return Response({}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def push_data(request):
    if "HOANGLAMBK57XYZ" == request.data.get("pwd"):
        contract, _ = Contract.objects.get_or_create(
            address="0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85",
            chain_id="ethereum",
            defaults={
                "name": "Ethereum Name Service"
            }
        )
        msg = request.data.get("message")
        lines = msg.split("\n")
        for line in lines:
            save_line(line, contract)
        return Response(status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_last_block(request):
    return Response({
        "last_block": Asset.objects.order_by('-last_block').first().last_block
    })
