import flet as ft
from components import *


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
    register_new_user(page)
    page.update()

if __name__ == '__main__':
    ft.app(main)