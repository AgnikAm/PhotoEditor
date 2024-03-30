import flet as ft
import numpy as np
from buttons import MyButton
from contex_menu import build_content
from functions.image_operations import add_image_operation
from functions.files_operations import undo_command, redo_command


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


def build_operation_btn(operation: str, container: ft.Container, photo_arr: ft.Ref[np.ndarray], photo_flet: ft.Image) -> ft.FilledButton:
    operation_btn = MyButton(operation)
    if operation not in ['rotate', 'black & white', 'sepia', 'inversion']:
        operation_btn.define_onclick(lambda _: option_animate(operation, container))
    else:
        operation_btn.define_onclick(lambda _: add_image_operation(operation, photo_arr, photo_flet))

    operation_btn = operation_btn.build_operation()

    return operation_btn


def build_operation_options(operation: str, photo_arr: ft.Ref[np.ndarray], photo_flet: ft.Image) -> ft.Container:
    return ft.Container(
        width=300,
        height=3,
        bgcolor='#1d3678',
        margin=ft.margin.only(top=-5),
        border_radius=ft.border_radius.only(bottom_left=5, bottom_right=5),
        animate=ft.animation.Animation(500, "ease"),
        content=build_content(operation, photo_arr, photo_flet)
    )


def option_animate(operation: str, cont: ft.Container) -> None:
    match operation:
        case 'rotate':
            pass
        case 'grayscale':
            pass
        case 'flip':
            cont.height = 100 if cont.height == 3 else 3
        case 'resize':
            cont.height = 165 if cont.height == 3 else 3
        case 'color adjustments':
            cont.height = 240 if cont.height == 3 else 3
        case _:
            cont.height = 140 if cont.height == 3 else 3
            
    cont.bgcolor = '#1d3678' if cont.bgcolor == '#374362' else '#374362'
    cont.update()


def type_divider(text: str) -> ft.Column:
    return ft.Column(
        controls=[
            ft.Text(text),
            ft.Divider()
        ]
    )


def undo_redo_buttons(photo_arr: ft.Ref[np.ndarray], photo_flet: ft.Image) -> ft.Row:
    undo_icon = ft.Icon(ft.icons.UNDO_ROUNDED, color=ft.colors.WHITE, size=20)
    redo_icon = ft.Icon(ft.icons.REDO_ROUNDED, color=ft.colors.WHITE, size=20)

    undo = MyButton()
    undo.define_onclick(lambda _: undo_command(photo_arr, photo_flet))

    redo = MyButton()
    redo.define_onclick(lambda _: redo_command(photo_arr, photo_flet))

    undo = undo.build_command(undo_icon)
    redo = redo.build_command(redo_icon)

    return ft.Row(controls=[undo, redo])


def build_edit_options(photo_arr: ft.Ref[np.ndarray], image_flet: ft.Image) -> ft.Container:
    list_view = ft.ListView(spacing=20, padding=20)
    elements = [
        type_divider('Shape'), 
        'rotate',
        'flip',
        'resize',
        type_divider('Sharpness'), 
        'blur',
        'sharpen',
        type_divider('Colors'), 
        'color adjustments',
        'hue',
        'brightness', 
        'saturation',
        'contrast',
        type_divider('Miscellaneous'),
        'noise',
        'vignette',
        'inversion',
        type_divider('Filters'),
        'black & white',
        'sepia',
        'mojave',
        'nostalgia',
        'neon',
        'twilight'
    ]

    for element in elements:
        if not isinstance(element, str):
            list_view.controls.append(element)
        else:
            operation_btn_container = build_operation_options(element, photo_arr, image_flet)
            operation_btn = build_operation_btn(element, operation_btn_container, photo_arr, image_flet)
            list_view.controls.append(ft.Column([operation_btn, operation_btn_container]))

    return ft.Container(content=list_view, margin=ft.margin.only(bottom=140))


def build_sidebar(height: int, content: ft.Control) -> ft.Container:
    return ft.Container(
            width=275,
            height=height,
            bgcolor='#202230',
            content=content
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


def build_background(content: ft.Control) -> ft.Container:
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