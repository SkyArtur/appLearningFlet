from re import search
from datetime import date
from typing import Literal
from database import dbSQLite
from flet import Page, TextField
from passlib.hash import pbkdf2_sha256 as pbkdf2
from components import custom_snack_bar

#-----------------------------------------------------------------------------------------------------------------------
#   VALIDAÇÃO DOS CAMPOS DE FORMULÁRIOS
#-----------------------------------------------------------------------------------------------------------------------
def validate_fields(page: Page, *args: TextField) -> None | bool:
    """
    Checks the form field values. Returns True if the form field values are filled in.
    :param page: Flet library Page object
    :param args: Form TextFields.
    """
    try:
        for item in args:
            if item.value is None or item.value == '':
                raise ValueError(f'Field "{item.label}" cannot be null')
        return True
    except ValueError as error:
        custom_snack_bar(validate_fields, f'{error}.', page)

#-----------------------------------------------------------------------------------------------------------------------
#   VALIDAÇÃO DO CAMPO NOME E SOBRENOME
#-----------------------------------------------------------------------------------------------------------------------
def validate_names(names: TextField, page: Page) -> None | str:
    try:
        if not isinstance(names.value, str) or not names.value.replace(' ', '').isalpha():
            raise ValueError(f'Value entered in the {names.label} field is not valid')
        return names.value
    except (ValueError, TypeError) as error:
        custom_snack_bar(validate_names, error, page)

#-----------------------------------------------------------------------------------------------------------------------
#   VALIDAÇÃO DO CAMPO DE DATAS
#-----------------------------------------------------------------------------------------------------------------------
def validate_date(date_field: TextField, page: Page, __format: Literal['BR', 'US', 'ISO'] = 'BR') -> date | None:
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

#-----------------------------------------------------------------------------------------------------------------------
#   VALIDAÇÃO DO CAMPO DE E-MAIL
#-----------------------------------------------------------------------------------------------------------------------
def validate_email(email_field: TextField, page: Page) -> str | None:
    try:
        valid_email = search(r'^[a-z0-9_]{1,100}@[a-z0-9]{1,100}\.[a-z]{2,3}[.]?[a-z]{2}?$', email_field.value).string
        if dbSQLite.fetchone('select id from users where email = ?;', valid_email):
            raise ValueError('Email already registered!')
        return valid_email
    except (TypeError, ValueError, AttributeError) as error:
        custom_snack_bar(validate_email, f'{error}.', page)

#-----------------------------------------------------------------------------------------------------------------------
#   VALIDAÇÃO DOS CAMPOS DE SENHAS
#-----------------------------------------------------------------------------------------------------------------------
def validate_password(password: TextField, confirm: TextField, page: Page) -> None | str:
    try:
        if len(password.value) < 6:
            raise ValueError("Password must be at least 6 characters long")
        elif password.value != confirm.value:
            raise ValueError(f"Password value does not match confirm")
        else:
            return pbkdf2.hash(password.value)
    except ValueError as error:
        custom_snack_bar(validate_password, f'{error}.', page)
