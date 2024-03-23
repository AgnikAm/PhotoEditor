import flet as ft
import numpy as np
from buttons import MyButton
from functions.image_operations import add_image_operation


def build_resize(name: str, photo_arr, photo_flet):
    width = ft.TextField(
        label="width",
        border_color='#d9e3ff',
        input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9]", replacement_string=""),
        height=40,
        text_style=ft.TextStyle(size=12),
    )

    height = ft.TextField(
        label="height",
        border_color='#d9e3ff',
        input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9]", replacement_string=""),
        height=40,
        text_style=ft.TextStyle(size=12),
    )

    apply_button = MyButton('apply')
    apply_button.define_onclick(lambda _: add_image_operation(name, photo_arr, photo_flet, [width.value, height.value]))
    apply_button = apply_button.build_file()

    return ft.Container(
        content=ft.Column(
            controls=[width, height, ft.Container(content=apply_button, alignment=ft.alignment.center)],
        ),
        padding=20,
    )


def build_slider(name, photo_arr, photo_flet, min, max, division, label):
    slider = ft.Slider(min=min, max=max, divisions=division, label=label, round=1)

    apply_button = MyButton('apply')
    apply_button.define_onclick(lambda _: add_image_operation(name, photo_arr, photo_flet, [slider.value]))
    apply_button = apply_button.build_file()
    
    return ft.Container(
        content=ft.Column(
            controls=[slider, ft.Container(content=apply_button, alignment=ft.alignment.center)],
        ),
        margin=ft.margin.only(top=40, left=5, right=5)
    )


def build_content(name: str, photo_arr, photo_flet):
    match name:
        case 'resize':
            return build_resize(name, photo_arr, photo_flet)
        case 'blur':
            return build_slider(name, photo_arr, photo_flet, 0, 10, 40, "{value}")
        case 'sharpen':
            return build_slider(name, photo_arr, photo_flet, 0, 10, 21, "{value}")
        case 'brightness':
            return build_slider(name, photo_arr, photo_flet, -50, 50, 20, "{value}")
        case 'saturation':
            return build_slider(name, photo_arr, photo_flet, 0, 2, 40, "{value}")

    