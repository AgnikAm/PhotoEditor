import flet as ft
from flet_contrib.color_picker import ColorPicker
import numpy as np
from typing import Optional

from components.buttons import MyButton
from functions.image_operations import add_image_operation


def build_resize(name: str, photo_arr: ft.Ref[np.ndarray], photo_flet: ft.Image) -> ft.Container:
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


def build_slider(
        name: str, 
        photo_arr: ft.Ref[np.ndarray], 
        photo_flet: ft.Image, 
        min: float, 
        max: float, 
        division: int, 
        label: str, 
        round: int, 
        value: Optional[float] = None
    ) -> ft.Container:

    slider = ft.Slider(min=min, max=max, divisions=division, label=label, round=round, value=value)

    apply_button = MyButton('apply')
    apply_button.define_onclick(lambda _: add_image_operation(name, photo_arr, photo_flet, [slider.value]))
    apply_button = apply_button.build_file()
    
    return ft.Container(
        content=ft.Column(
            controls=[
                slider, 
                ft.Container(content=apply_button, alignment=ft.alignment.center)
            ],
        ),
        margin=ft.margin.only(top=40, left=5, right=5)
    )


def build_color_sliders(name: str, photo_arr: ft.Ref[np.ndarray], photo_flet: ft.Image) -> ft.Container:
    red = ft.Slider(min=0, max=2, divisions=510, label="{value}", value=1, round=3, height=20)
    green = ft.Slider(min=0, max=2, divisions=510, label="{value}", value=1, round=3, height=20)
    blue = ft.Slider(min=0, max=2, divisions=510, label="{value}", value=1, round=3, height=20)

    apply_button = MyButton('apply')
    apply_button.define_onclick(lambda _: add_image_operation(name, photo_arr, photo_flet, [red.value, green.value, blue.value]))
    apply_button = apply_button.build_file()

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(ft.Text('Red'), margin=ft.margin.only(left=15)),
                red,
                ft.Container(ft.Text('Green'), margin=ft.margin.only(left=15)),
                green,
                ft.Container(ft.Text('Blue'), margin=ft.margin.only(left=15)),
                blue,
                ft.Container(content=apply_button, alignment=ft.alignment.center)
            ],
        ),
        margin=ft.margin.only(top=15, left=5, right=5)
    )


def build_radio(name: str, photo_arr: ft.Ref[np.ndarray], photo_flet: ft.Image) -> ft.Container:
    radio_group = ft.RadioGroup(
        content=ft.Row(
            controls=[
                ft.Radio(value=0, label='X axis'),
                ft.Radio(value=1, label='Y axis')
            ]
        )
    )

    apply_button = MyButton('apply')
    apply_button.define_onclick(lambda _: add_image_operation(name, photo_arr, photo_flet, [radio_group.value]))
    apply_button = apply_button.build_file()


    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(content=radio_group, margin=ft.margin.only(top=15, left=40)), 
                ft.Container(content=apply_button, alignment=ft.alignment.center)
            ]
        )
    )


def build_solid_pick(name: str, photo_arr: ft.Ref[np.ndarray], photo_flet: ft.Image) -> ft.Container:
    color_pick = ColorPicker(
        color='#000000',
        width=200
    )

    slider = ft.Slider(min=0, max=1, divisions=20, label='{value}', round=2, value=0.5)

    apply_button = MyButton('apply')
    apply_button.define_onclick(lambda _: add_image_operation(name, photo_arr, photo_flet, [color_pick.color, slider.value]))
    apply_button = apply_button.build_file()

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(content=ft.Text('color:'), margin=ft.margin.only(top=20, left=20)),
                ft.Container(content=color_pick, alignment=ft.alignment.center),
                ft.Container(content=ft.Text('opacity:'), margin=ft.margin.only(top=20, left=20)),
                ft.Container(content=slider, alignment=ft.alignment.center),
                ft.Container(content=apply_button, alignment=ft.alignment.center)
            ]
        )
    )

def build_gradient_pick(name: str, photo_arr: ft.Ref[np.ndarray], photo_flet: ft.Image) -> ft.Container:
    radio_group = ft.RadioGroup(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                    ft.Radio(value='horizontal', label='horizontal'),
                    ft.Radio(value='vertical', label='vertical'),
                    ]
                ),
                ft.Row(
                    controls=[
                    ft.Radio(value='diagonal', label='diagonal'),
                    ft.Container(ft.Radio(value='radial', label='radial'), margin=ft.margin.only(left=8)),
                    ]
                )
            ]
        ),
        value='horizontal'
    )

    first_color = ColorPicker(
        width=200
    )
    first_color.hex.visible = False

    second_color = ColorPicker(
        width=200
    )
    second_color.hex.visible = False

    slider = ft.Slider(min=0, max=1, divisions=20, label='{value}', round=2, value=0.5)

    apply_button = MyButton('apply')
    apply_button.define_onclick(lambda _: add_image_operation(name, photo_arr, photo_flet, [radio_group.value, first_color.color, second_color.color, slider.value]))
    apply_button = apply_button.build_file()

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(content=radio_group, margin=ft.margin.only(top=15, left=20)),
                ft.Container(content=ft.Text('first color:'), margin=ft.margin.only(top=20, left=20)),
                ft.Container(content=first_color, alignment=ft.alignment.center),
                ft.Container(content=ft.Text('second color:'), margin=ft.margin.only(top=20, left=20)),
                ft.Container(content=second_color, alignment=ft.alignment.center), 
                ft.Container(content=ft.Text('opacity:'), margin=ft.margin.only(top=20, left=20)),
                ft.Container(content=slider, alignment=ft.alignment.center),
                ft.Container(content=apply_button, alignment=ft.alignment.center)
            ]
        )
    )


def build_pick_file(name: str, photo_arr: ft.Ref[np.ndarray], photo_flet: ft.Image, page: ft.Page) -> ft.Container:
    img_path = ''

    def handle_file_selection(selected_file):
        nonlocal img_path
        if selected_file:
            img_path = selected_file.files[0].path.replace("\\", "/")

    file_picker = ft.FilePicker(on_result=lambda e: handle_file_selection(e))
    page.add(file_picker)

    pick_btn = MyButton('pick file')
    pick_btn.define_onclick(lambda _: file_picker.pick_files(allow_multiple=False, allowed_extensions=['png', 'jpg', 'jpeg']))
    pick_btn = pick_btn.build_file()
    pick_btn.width = 200

    slider = ft.Slider(min=0, max=1, divisions=20, label='{value}', round=2, value=0.5)

    apply_button = MyButton('apply')
    apply_button.define_onclick(lambda _: add_image_operation(name, photo_arr, photo_flet, [img_path, slider.value]))
    apply_button = apply_button.build_file()

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(content=pick_btn, alignment=ft.alignment.center, margin=ft.margin.only(top=20)),
                ft.Container(content=ft.Text('opacity:'), margin=ft.margin.only(top=20, left=20)),
                ft.Container(content=slider, alignment=ft.alignment.center),
                ft.Container(content=apply_button, alignment=ft.alignment.center)
            ]
        )
    )


def build_content(name: str, photo_arr: ft.Ref[np.ndarray], photo_flet: ft.Image) -> ft.Container:
    match name:
        case 'flip':
            return build_radio(name, photo_arr, photo_flet)
        case 'resize':
            return build_resize(name, photo_arr, photo_flet)
        case 'blur':
            return build_slider(name, photo_arr, photo_flet, 0, 2, 40, "{value}", 2, 0)
        case 'sharpen':
            return build_slider(name, photo_arr, photo_flet, 0, 3, 30, "{value}", 1, 1)
        case 'color adjustments':
            return build_color_sliders(name, photo_arr, photo_flet)
        case 'hue':
            return build_slider(name, photo_arr, photo_flet, 0, 179, 179, "{value}", 0, 1)
        case 'brightness':
            return build_slider(name, photo_arr, photo_flet, -60, 60, 60, "{value}", 1, 0)
        case 'saturation':
            return build_slider(name, photo_arr, photo_flet, 0, 2, 40, "{value}", 1, 1)
        case 'contrast':
            return build_slider(name, photo_arr, photo_flet, 0, 2, 40, "{value}", 1, 1)
        case 'gradient overlay':
            return build_gradient_pick(name, photo_arr, photo_flet)
        case 'solid overlay':
            return build_solid_pick(name, photo_arr, photo_flet)
        case _:
            return build_slider(name, photo_arr, photo_flet, 0, 1, 20, "{value}", 2, 0.5)

