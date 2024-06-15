from rest_framework import filters

class TagFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        tags = request.query_params.get('tags')
        if tags:
            queryset = queryset.filter(tags__name__iexact=tags)
        return queryset
