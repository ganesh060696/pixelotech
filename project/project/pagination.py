from rest_framework.response import Response
from rest_framework import pagination


class BasePagination(pagination.PageNumberPagination):
    """ Custom small set pagination for the new APIs"""
    page_size = 10

    def get_paginated_response(self, data):
        response = {
            'total_count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'next_page': self.page.next_page_number() if self.page.has_next() else None,
            'current_page': self.page.number,
            'previous_page': self.page.previous_page_number() if self.page.has_previous() else None,
            'page_size': self.page_size,
            'data': data
        }
        return Response(response)


class SmallSetPagination(BasePagination):
    """ Small set pagination for the new APIs"""
    page_size = 5
    max_page_size = 10


class DefaultSetPagination(BasePagination):
    """ Default set pagination for the new APIs"""
    page_size = 10


class LargeSetPagination(BasePagination):
    """ Large set pagination for the new APIs"""
    page_size = 20
    max_page_size = 20


class CustomSetPagination(BasePagination):
    """ Custom set pagination for the new APIs"""

    max_page_size = 10

    def __init__(self, page_size, *args, **kwargs):
        self.page_size = page_size
        super().__init__(*args, **kwargs)
