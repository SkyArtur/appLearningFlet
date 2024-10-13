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
    Validates the form field values. Returns True if all the form fields are filled.
    :param page: A Page object from the Flet library.
    :param args: One or more TextField objects from the form.
    :return: True if all fields are filled, otherwise raises a ValueError.
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
    """
    Validates the value entered in the name field. Returns the entered value if it is a valid string
    and contains no numeric characters.
    :param names: A TextField object representing the name field in the form.
    :param page: A Page object from the Flet library.
    :return: The value of the TextField if valid, otherwise raises a ValueError or TypeError.
    """
    try:
        if not isinstance(names.value, str) or not names.value.replace(' ', '').isalpha():
            raise ValueError(f'Value entered in the {names.label} field is not valid')
        return names.value
    except (ValueError, TypeError) as error:
        custom_snack_bar(validate_names, f'{error}.', page)

#-----------------------------------------------------------------------------------------------------------------------
#   VALIDAÇÃO DO CAMPO DE DATAS
#-----------------------------------------------------------------------------------------------------------------------
def validate_date(date_field: TextField, page: Page, __format: Literal['UK', 'US', 'ISO'] = 'UK') -> date | None:
    """
    Validates the value entered in the date field. Returns a `date` object if the value matches the expected format
    (UK, US, or ISO) based on the selected format.
    :param date_field: A TextField object representing the date field in the form.
    :param page: A Page object from the Flet library.
    :param __format: A string literal indicating the expected date format ('UK', 'US', or 'ISO'). Defaults to 'UK'.
    :return: A `date` object if valid, otherwise raises a ValueError or TypeError.
    """
    try:
        # Extract date components using regular expression
        valid = [int(d) for d in search(r'^([0-9]{2,4})[/-]?([0-9]{2})[/-]?([0-9]{2,4})$', date_field.value).groups()]
        # Match the format and return the corresponding date
        match __format:
            case 'UK': # Day-Month-Year
                return date(day=valid[0], month=valid[1], year=valid[2])
            case 'US': # Month-Day-Year
                return date(day=valid[1], month=valid[0], year=valid[2])
            case 'ISO': # Year-Month-Day
                return date(day=valid[2], month=valid[1], year=valid[0])
            case _:
                raise ValueError('Date format not defined!')
    except (TypeError, ValueError, AttributeError) as error:
        if isinstance(error, AttributeError):
            error = 'Value is not valid for a date'
        custom_snack_bar(validate_date, f'{error}.', page)

#-----------------------------------------------------------------------------------------------------------------------
#   VALIDAÇÃO DO CAMPO DE E-MAIL
#-----------------------------------------------------------------------------------------------------------------------
def validate_email(email_field: TextField, page: Page) -> str | None:
    """
    Validates the value entered in the email field. Returns the email string if it matches the defined pattern
    and is not already registered in the database.
    :param email_field: A TextField object representing the email field in the form.
    :param page: A Page object from the Flet library.
    :return: A valid email string if not already registered, otherwise raises a ValueError or TypeError.
    """
    try:
        # Validate email format using regular expression
        valid_email = search(r'^[a-z0-9_.+-]+@([a-z0-9-]+\.)+[a-z]{2,}$', email_field.value).string
        # Check if the email is already registered in the database
        if dbSQLite.fetchone('select id from users where email = ?;', valid_email):
            raise ValueError('Email already registered!')
        return valid_email
    except (TypeError, ValueError, AttributeError) as error:
        if isinstance(error, AttributeError):
            error = 'Value is not valid for a email'
        custom_snack_bar(validate_email, f'{error}.', page)

#-----------------------------------------------------------------------------------------------------------------------
#   VALIDAÇÃO DOS CAMPOS DE SENHAS
#-----------------------------------------------------------------------------------------------------------------------
def validate_password(password: TextField, confirm: TextField, page: Page) -> None | str:
    """
    Validates the password entered in the form. Ensures the password meets length requirements
    and matches the confirmation password. Returns a hashed password if valid.
    :param password: A TextField object representing the password input.
    :param confirm: A TextField object representing the confirmation password input.
    :param page: A Page object from the Flet library.
    :return: A hashed password string if valid, otherwise raises a ValueError.
    """
    try:
        # Check password length and match with confirmation
        if len(password.value) < 6:
            raise ValueError("Password must be at least 6 characters long")
        elif password.value != confirm.value:
            raise ValueError(f"Password value does not match confirm")
        else:
            return pbkdf2.hash(password.value)
    except ValueError as error:
        custom_snack_bar(validate_password, f'{error}.', page)
