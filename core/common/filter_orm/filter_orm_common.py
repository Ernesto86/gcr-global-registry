import datetime
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
        query_AND_1 = Q()
        query_AND_1.connector = 'AND'
        query_OR_1 = Q()
        query_OR_1.connector = 'OR'
        return query_AND_1, query_OR_1

    @staticmethod
    def get_url_params(request_get):
        get_params = {k: v[0] for k, v in dict(request_get).items()}

        try:
            get_params.pop('page')
        except:
            pass
        return get_params

    @staticmethod
    def get_filter_date_range(request_get, date_key, query_create: Q = None, ):
        data = {}

        if 'date_init' in request_get:
            start_date = request_get.get('date_init', '')
            print("start_date___: ", start_date)
            end_date = request_get.get('date_end', '')
            if start_date and end_date:
                try:
                    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
                    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
                    date_range = (
                        datetime.datetime.combine(start_date, datetime.datetime.min.time()),
                        datetime.datetime.combine(end_date, datetime.datetime.max.time())
                    )
                    # data[f'{date_key}__range'] = date_range
                    query_create.children.append((f'{date_key}__range', date_range))
                except:
                    pass
