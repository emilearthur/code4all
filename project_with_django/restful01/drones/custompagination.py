from rest_framework.pagination import LimitOffsetPagination


class LimitOffsetPaginationWithUpperBound(LimitOffsetPagination):
    # setting maximum limit values to 10
    max_limit = 8