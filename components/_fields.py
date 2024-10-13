from flet import TextField, InputBorder

def custom_text_field(label: str, width: int = 100, hint_text: str = None, tooltip: str = None) -> TextField:
    return TextField(
        label=label,
        width=width,
        border=InputBorder.UNDERLINE,
        tooltip=tooltip,
        filled=True,
        hint_text=hint_text
    )

def custom_password_field(label: str, width: int = 100, hint_text: str = None, tooltip: str = None) -> TextField:
    return TextField(
        label=label,
        width=width,
        password=True,
        border=InputBorder.UNDERLINE,
        tooltip=tooltip,
        filled=True,
        hint_text=hint_text,
        can_reveal_password=True
    )