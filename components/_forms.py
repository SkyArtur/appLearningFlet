from typing import Callable
from flet import Page, Text, ElevatedButton
from ._fields import custom_text_field, custom_password_field
from ._rows import form_row
from functions import *


def form_register_new_user(page: Page):
    def save_new_user(event):
        _fields = [first_name, last_name, birth_date, username, email, password, confirm_password]
        if not validate_fields(page, *_fields): return
        elif not (_first_name := validate_names(_fields[0], page)): return
        elif not (_last_name := validate_names(_fields[1], page)): return
        elif not (_birth_date := validate_date(_fields[2], page)): return
        elif not (_username := validate_username(_fields[3], page)): return
        elif not (_email := validate_email(_fields[4], page)): return
        elif not (_password := validate_password(_fields[5], _fields[6], page)): return
        else:
            save_user(page, _first_name, _last_name, _birth_date.isoformat(), _username, _email, _password)
        for field in _fields:
            field.value = None
        page.update()

    first_name = custom_text_field('Nome', width=250)
    last_name = custom_text_field(label='Sobrenome', width=350)
    birth_date = custom_text_field(label='Nascimento', width=150)
    username = custom_text_field(label='username', width=300)
    email = custom_text_field(label='E-mail', width=460)
    password = custom_password_field(label='Password', width=380)
    confirm_password = custom_password_field(label='Confirme a senha', width=380)
    btn_save = ElevatedButton(text='Salvar', width=500, height=45, on_click=save_new_user)

    page.add(
        form_row(Text('Cadastrar Usuário', size=30)),
        form_row(first_name, last_name, birth_date),
        form_row(username, email),
        form_row(password, confirm_password),
        form_row(btn_save)
    )


def form_login(page: Page, function: Callable):
    def _login(event):
        _fields = [username, password]
        if not validate_fields(page, *_fields): return
        elif not check_login_data(page, *_fields): return
        else:
            function(page)
        for field in _fields:
            field.value = None
        page.update()

    username = custom_text_field('username', width=400)
    password = custom_password_field('password', width=400)
    btn_login = ElevatedButton(text='Login', width=300, height=45, on_click=_login)
    page.add(
        form_row(Text('Login', size=30)),
        form_row(username, password),
        form_row(btn_login),
    )