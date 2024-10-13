import flet as ft
from components import *


def app_learning(page: ft.Page):
    page.controls.clear()
    page.overlay.clear()
    page.window.width = 980
    page.window.height = 730
    page.add(ft.Text('aplicação principal'))


def login(page: ft.Page):
    def _register_new_user(event):
        register_new_user(page)
    page.controls.clear()
    page.overlay.clear()
    page.window.width = 500
    page.window.height = 600
    page.window.resizable = False
    page.window.maximizable = False
    page.window.minimizable = False
    page.window.always_on_top = True
    page.window.alignment = ft.alignment.center
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    btn_register_new_user = ft.TextButton(text='Cadastrar Novo Usuario', width=250, on_click=_register_new_user)
    form_login(page, app_learning)
    page.add(form_row(btn_register_new_user))
    page.update()


def register_new_user(page: ft.Page):
    page.controls.clear()
    page.overlay.clear()
    page.window.width = 850
    page.window.height = 500
    page.window.resizable = False
    page.window.maximizable = False
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    form_register_new_user(page)
    page.update()


def main(page: ft.Page):
    page.title = 'App Learning Flet'
    login(page)
    page.update()

if __name__ == '__main__':
    ft.app(main)