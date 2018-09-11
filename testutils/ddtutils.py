
class NamedList(list):
    """Custom list with __name__ attribute, which is added by prepare()"""
    pass


def prepare(test_data):
    """Generator used to prepare data for DDT

    :param test_data: dict with test data

    :return: named list with test data
    """
    for td in test_data:
        named_list = NamedList(test_data[td])
        setattr(named_list, '__name__', td)
        yield named_list
