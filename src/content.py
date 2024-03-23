import flet as ft
import numpy as np
from buttons import MyButton


def build_resize():
    width_field = ft.TextField(
        label="width",
        border_color='#d9e3ff',
        input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9]", replacement_string=""),
        height=40,
        text_style=ft.TextStyle(size=12)
    )

    height_field = ft.TextField(
        label="height",
        border_color='#d9e3ff',
        input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9]", replacement_string=""),
        height=40,
        text_style=ft.TextStyle(size=12)
    )

    apply_button = ft.Container(content=MyButton('apply').build_file(), alignment=ft.alignment.center)
    return ft.Container(
        content=ft.Column(
            controls=[width_field, height_field, apply_button],
        ),
        padding=20,
    )


def build_degree_slider():
    slider = ft.Slider(min=0, max=360, divisions=36, label="{value}°")
    apply_button = ft.Container(content=MyButton('apply').build_file(), alignment=ft.alignment.center)
    return ft.Container(
        content=ft.Column(
            controls=[slider, apply_button],
        ),
        margin=ft.margin.only(top=40, left=5, right=5)
    )


def build_slider():
    slider = ft.Slider(min=0.0, max=1.0, divisions=10, label="{value}", round=1)
    apply_button = ft.Container(content=MyButton('apply').build_file(), alignment=ft.alignment.center)
    return ft.Container(
        content=ft.Column(
            controls=[slider, apply_button],
        ),
        margin=ft.margin.only(top=40, left=5, right=5)
    )


def build_content(name: str):
    match name:
        case 'rotate':
            return build_degree_slider()
        case 'resize':
            return build_resize()
        case _:
            return build_slider()
    