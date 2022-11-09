import enum

from django.db.models import Q


class FilterQueryEnum(enum.Enum):
    filter_and = "and"
    filter_or = "or"


class FilterOrmCommon:
    @staticmethod
    def set_value_search_determinate(
            value,
            filter_list: tuple = (),
            filter_query_enum: FilterQueryEnum = FilterQueryEnum.filter_and,
            query_create: Q = None,
            default=None
    ):
        for filter_value in filter_list:

            if value:
                query_create.children.append((filter_value, value))
                continue

            if default is None:
                continue

            query_create.children.append((filter_value, default))

    @staticmethod
    def get_query_connector_tuple():
        query_OR_1 = Q()
        query_OR_1.connector = 'OR'
        query_AND_1 = Q()
        query_AND_1.connector = 'AND'
        return query_AND_1, query_OR_1
