import flet as ft
from re import search
from database import dbSQLite
from components import custom_snack_bar


def validate_email(email_field: ft.TextField, page: ft.Page) -> str | None:
    try:
        valid_email = search(r'^[a-z0-9_]{1,100}@[a-z0-9]{1,100}\.[a-z]{2,3}[.]?[a-z]{2}?$', email_field.value).string
        if dbSQLite.fetchone('select id from users where email = ?;', valid_email):
            raise ValueError('Email already registered!')
        return valid_email
    except (TypeError, ValueError, AttributeError) as error:
        custom_snack_bar(validate_email, f'{error}.', page)

