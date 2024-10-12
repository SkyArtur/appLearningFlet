import flet as ft
from re import search
from datetime import date
from typing import Literal
from components import custom_snack_bar


def validate_date(date_field: ft.TextField, page: ft.Page, __format: Literal['BR', 'US', 'ISO'] = 'BR') -> date | None:
    try:
        valid = [int(d) for d in search(r'^([0-9]{2,4})[/-]?([0-9]{2})[/-]?([0-9]{2,4})$', date_field.value).groups()]
        match __format:
            case 'BR':
                return date(day=valid[0], month=valid[1], year=valid[2])
            case 'US':
                return date(day=valid[1], month=valid[0], year=valid[2])
            case 'ISO':
                return date(day=valid[2], month=valid[1], year=valid[0])
            case _:
                raise ValueError(' Format date not defined!')
    except (TypeError, ValueError, AttributeError) as error:
        if isinstance(error, AttributeError):
            error = 'Value is not valid for a date'
        custom_snack_bar(validate_date, f'{error}.', page)
