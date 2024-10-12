from re import search
from datetime import date
from typing import Literal


def validate_date(date_string: str, __format: Literal['BR', 'US', 'ISO'] = 'BR') -> date | bool:
    try:
        valid = [int(d) for d in search(r'^([0-9]{2,4})[/-]?([0-9]{2})[/-]?([0-9]{2,4})$', date_string).groups()]
        match __format:
            case 'BR':
                return date(day=valid[0], month=valid[1], year=valid[2])
            case 'US':
                return date(day=valid[1], month=valid[0], year=valid[2])
            case 'ISO':
                return date(day=valid[2], month=valid[1], year=valid[0])
            case _:
                raise ValueError
    except (TypeError, ValueError, AttributeError):
        return False
