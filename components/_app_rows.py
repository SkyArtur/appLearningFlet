from flet import Row, MainAxisAlignment


def form_row(*args):
    return Row(
        controls=[*args],
        alignment=MainAxisAlignment.CENTER,
        wrap=True,
        expand=True,
    )