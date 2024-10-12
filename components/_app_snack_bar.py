from typing import Callable
from flet import SnackBar, Text, TextSpan, Page, TextStyle, FontWeight, colors

def custom_snack_bar(function: Callable, message: str, page: Page) -> None:
    page.overlay.append(
        SnackBar(
            content=Text(
                spans=[
                    TextSpan(text=f'ERROR <function: {function.__name__}>: ', style=TextStyle(color=colors.RED_400)),
                    TextSpan(text=message.upper(), style=TextStyle(weight=FontWeight.BOLD))
                ],
                color=colors.BLACK,
            ),
            bgcolor=colors.AMBER_50,
            show_close_icon=True,
            close_icon_color=colors.BLACK,
            open=True
        )
    )
    page.update()


