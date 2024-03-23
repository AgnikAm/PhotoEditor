import flet as ft
import numpy as np
from buttons import MyButton
from content import build_content


def build_navbar(page: ft.Page, button1: MyButton, button2: MyButton, path: ft.Text) -> ft.Container:
    return ft.Container(
        width=page.window_max_width,
        height=70,
        bgcolor='#323445',
        content=ft.Row(
            controls=[
                ft.Container(
                    ft.Text(value='Photo Editor', size=25),
                    margin=ft.margin.only(left=50)
                ),
                ft.Container(
                      ft.Icon(ft.icons.ENHANCE_PHOTO_TRANSLATE_ROUNDED),
                      margin=ft.margin.only(right=30)
                ),
                ft.VerticalDivider(width=20, thickness=2),
                button1.build_file(),
                button2.build_file(),
                path
            ],   
        ),
    )


def build_operation_btn(operation: str, container: ft.Container) -> ft.FilledButton:
    operation_btn = MyButton(operation)
    operation_btn.define_onclick(lambda _: option_animate(operation, container))
    operation_btn = operation_btn.build_operation()

    return operation_btn


def build_operation_options(operation: str) -> ft.Container:
    return ft.Container(
        width=300,
        height=3,
        bgcolor='#1d3678',
        margin=ft.margin.only(top=-5),
        border_radius=ft.border_radius.only(bottom_left=5, bottom_right=5),
        animate=ft.animation.Animation(500, "ease"),
        content=build_content(operation)
    )


def option_animate(operation, cont: ft.Container):
    match operation:
        case 'resize':
            cont.height = 160 if cont.height == 3 else 3
        case _:
            cont.height = 140 if cont.height == 3 else 3
            
    cont.bgcolor = '#1d3678' if cont.bgcolor == '#374362' else '#374362'
    cont.update()


def build_edit_options(photo_arr: ft.Ref[np.ndarray], image_flet: ft.Image) -> ft.ListView:
    list_view = ft.ListView(expand=True, spacing=20, padding=20)
    operations = ['rotate', 'resize', 'blur', 'sharpen', 'saturation', 'lighten', 'darken']

    for operation in operations:
        operation_btn_container = build_operation_options(operation)
        operation_btn = build_operation_btn(operation, operation_btn_container)
        list_view.controls.append(ft.Column([operation_btn, operation_btn_container]))

    return list_view


def build_sidebar(page: ft.Page, content) -> ft.Container:
    return ft.Container(
        width=275,
        height=page.window_height,
        bgcolor='#202230',
        content=content,
    )


def build_canvas(image: ft.Image) -> ft.Container:
    return ft.Container(
        width=1400,
        height=780,
        bgcolor=ft.colors.TRANSPARENT,
        border=ft.border.all(width=0.2, color='white'),
        padding=10,
        content=image
    )


def build_background(content) -> ft.Container:
    return ft.Container(
            width=1650,
            height=1050,
            content=content,
            alignment=ft.alignment.Alignment(0, -0.4)
    )


def build_workspace(controls: list[ft.Container, ft.Container]) -> ft.Container:
    return ft.Container(
        ft.Row(controls=controls),
         margin=ft.margin.symmetric(vertical=-10)
    )