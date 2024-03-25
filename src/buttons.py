import flet as ft
from typing import Callable, Optional

class MyButton:
    text: ft.Text
    style: ft.ButtonStyle
    onclick: Callable

    def __init__(self, text: Optional[str] = None) -> None:
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
            shape=ft.RoundedRectangleBorder(radius=5),
        )

        return ft.FilledButton(
            content=ft.Text(value=self.text.value, size=16),
            width=300,
            height=40,
            style=self.style,
            on_click=self.onclick
        )
    
    def build_command(self, icon: ft.Icon) -> ft.FilledButton:
        self.style = ft.ButtonStyle(
            bgcolor={
                ft.MaterialState.DEFAULT: '#374362',
                ft.MaterialState.HOVERED: '#1d3678'
            },
            shape=ft.RoundedRectangleBorder(radius=3)
        )

        return ft.FilledButton(
            content=ft.Container(icon, alignment=ft.alignment.center),
            width=70,
            height=30,
            style=self.style,
            on_click=self.onclick
        )

