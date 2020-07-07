# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint
from web.base.views import BaseResource
from exceptions import InternalServerError, ValidationError
from flask_restful import marshal
from mongoengine import Q
from web.charts.models import SpreadData, Pairs
from web.utility.utils import convert_time, current_time_range
from web.charts.serializers import chart_fields, pair_fields
from web.tasks.actions import crawl_market_data


class ChartResource(BaseResource):
    """Charts stats resource"""

    def get(self, pair_id):
        self.add_filter('start', required=True, type=str, location='args')
        self.add_filter('end', required=True, type=str, location='args')

        data_filters = self.get_filter()
        start = convert_time(data_filters['start'], timezone=2)
        end = convert_time(data_filters['end'], timezone=2)
        try:
            pair = Pairs.objects.get_or_404(pk=pair_id)
            reports = SpreadData.objects(pair=pair.name)
            reports = reports.filter((Q(timestamp__gte=start) & Q(timestamp__lte=end))).order_by('timestamp')
            return self.success(data={'results': marshal(list(reports), chart_fields)})
        except Exception as e:
            raise InternalServerError


class PairListResource(BaseResource):
    """Pair list resource """
    def get(self):
        pairs = Pairs.objects
        return self.success(data={'results': marshal(list(pairs), pair_fields)})

    def post(self):
        self.add_filter('pair_name', required=True, type=str, location='json')

        data = self.get_filter()
        pair_name = data['pair_name']
        if Pairs.objects(name=pair_name).count() > 0:
            raise ValidationError
        pair = Pairs(name=pair_name)
        pair.save()
        return self.success(data={'result': marshal(pair, pair_fields)})

    def put(self):
        self.add_filter('pair_id', required=True, type=str, location='json')

        data = self.get_filter()
        pair_id = data['pair_id']

        pair = Pairs.objects.get_or_404(pk=pair_id)
        pair.is_active = not pair.is_active
        pair.save()
        return self.success(data={'result': marshal(pair, pair_fields)})


class OrderHistoryResource(BaseResource):
    """data backfill resource"""
    def get(self, pair_id):
        self.add_filter('start', required=True, type=str, location='args')
        self.add_filter('end', required=True, type=str, location='args')
        data_filters = self.get_filter()
        start = data_filters['start']
        end = data_filters['end']
        pair = Pairs.objects.get_or_404(pk=pair_id)
        crawl_market_data.s(start, end, pair.name).apply_async()
        return self.success(data='ok')


class PopulateResource(BaseResource):
    """data population resource"""
    def get(self):
        list = ['BNB_USDSB-1AC', 'BTCB-1DE_BUSD-BD1']
        for e in list:
            pair = Pairs.objects(name=e)
            if len(pair) == 0:
                pair = Pairs(name=e)
                pair.save()
        return self.success(data='ok')