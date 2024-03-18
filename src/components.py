import flet as ft
from buttons import MyButton

def build_navbar(page: ft.Page, button1: MyButton, button2: MyButton, path: ft.Text) -> ft.Container:
    return ft.Container(
            width=page.window_max_width,
            height=60,
            bgcolor='#323445',
            content=ft.Row(
                controls=[ft.Container(ft.Text(value='Photo Editor', size=25),
                                    margin=ft.margin.only(left=20)),
                        ft.Icon(ft.icons.ENHANCE_PHOTO_TRANSLATE_ROUNDED),
                        ft.VerticalDivider(width=20, thickness=2),
                        button1.build_file(),
                        button2.build_file(),
                        path
                ],   
            ),
        )

def build_edit_options() -> ft.ListView:
    list_view = ft.ListView(expand=True, spacing=20, padding=20)
    options = ['rotate', 'zoom', 'blur', 'sharpen', 'saturation', 'lighten', 'darken']

    for option in options:
        list_view.controls.append(MyButton(option).build_option())

    return list_view

def build_sidebar(page: ft.Page, content) -> ft.Container:
    return ft.Container(
        width=215,
        height=page.window_height,
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

def build_background(content) -> ft.Container:
    return ft.Container(
            width=1720,
            height=1050,
            content=content,
            alignment=ft.alignment.Alignment(0, -0.4)
        )

def build_workspace(controls: list[ft.Container, ft.Container]) -> ft.Container:
    workspace = ft.Container(
        ft.Row(controls=controls),
         margin=ft.margin.symmetric(vertical=-10)
    )

    return workspace

