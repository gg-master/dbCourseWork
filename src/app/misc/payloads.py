import json
from decimal import Decimal
from datetime import date, datetime
from functools import partial, singledispatch


@singledispatch
def convert(value):
    raise TypeError(f'Unserializable value: {value!r}')


@convert.register(object)
def convert_dataclass(value):
    try:
        return value.to_dict()
    except AttributeError:
        return value.__dict__


@convert.register(list)
def convert_dataclass_list(value: list):
    return list(map(convert_dataclass, value))


@convert.register(date)
def convert_date(value: date):
    return value.isoformat()


@convert.register(datetime)
def convert_datetime(value: datetime):
    return value.isoformat()


@convert.register(Decimal)
def convert_datetime(value: Decimal):
    return float(value)


dumps = partial(
    json.dumps,
    default=convert,
    ensure_ascii=False,
    sort_keys=True,
    indent=4,
    separators=(',', ': '),
)
