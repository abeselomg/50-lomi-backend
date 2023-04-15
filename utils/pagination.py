from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    # Returns 10 elements per page, and the page query param is named "page"
    page_size = 10
    page_query_param = 'page'