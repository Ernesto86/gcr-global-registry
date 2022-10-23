
import datetime
from django.db.models import Q

class ListViewFilter(object):
    query_filter = {}
    def filter_date(self, date_key):
        if 'start_date' in self.request.GET:
            start_date = self.request.GET.get('start_date', '')
            end_date = self.request.GET.get('final', '')
            if start_date and end_date:
                try:
                    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
                    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
                    date_range = (
                        datetime.datetime.combine(start_date, datetime.datetime.min.time()),
                        datetime.datetime.combine(end_date, datetime.datetime.max.time())
                    )
                    self.query_filter[f'{date_key}__range'] = date_range
                except:
                    pass

    def queries(self):
        return [Q(**{k: v}) for k, v in self.query_filter.items() if v]
