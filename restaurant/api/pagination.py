from rest_framework.pagination import PageNumberPagination as RestFrameworkPageNumberPagination


class PageNumberPagination(RestFrameworkPageNumberPagination):
    page_size = 100
