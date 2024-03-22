import flet as ft
from typing import Callable

class MyButton:
    text: ft.Text
    style: ft.ButtonStyle
    onclick: Callable

    def __init__(self, text: str) -> None:
        self.text = ft.Text(value=text)
        self.onclick = None

    def define_onclick(self, fun: Callable) -> None:
        self.onclick = fun

    def build_file(self) -> ft.OutlinedButton:
        self.style = ft.ButtonStyle(
            bgcolor={
                ft.MaterialState.DEFAULT: '#374362',
                ft.MaterialState.HOVERED: '#1d3678'
            },
        )

        return ft.OutlinedButton(
            content=self.text,
            style=self.style,
            on_click=self.onclick
        )
    
    def build_operation(self) -> ft.FilledButton:
        self.style = ft.ButtonStyle(
            color='white',
            bgcolor={
                ft.MaterialState.DEFAULT: '#374362',
                ft.MaterialState.HOVERED: '#1d3678'
            },
            shape=ft.RoundedRectangleBorder(radius=5)
        )

        return ft.FilledButton(
            content=self.text,
            width=300,
            style=self.style,
            on_click=self.onclick
        )