class FilterQueryCommon:

    @staticmethod
    def get_param_validate(value: str or None):
        if value in ('undefined', 'null', None):
            return None

        if value == 'true':
            return True

        if value == 'false':
            return False

        return value

    @staticmethod
    def get_persist_list(dictionary_get: dict, dictionary_query_persist_list: tuple, exclude: tuple = ()):
        query_list = []

        for dictionary_query_persist in dictionary_query_persist_list:

            for k, v in dictionary_query_persist.items():

                if v in exclude:
                    continue

                parameter = FilterQueryCommon.get_param_validate(dictionary_get.get(v))

                if parameter:
                    query_list.append(f'{v}={parameter}')

        return query_list
