import flet as ft
from buttons import MyButton

def main(page: ft.Page) -> None:
    page.title = 'PhotoEditor'
    page.bgcolor = '#16171d'
    page.window_height = 1080
    page.window_width = 1920
    page.padding = 0

    options_names = ['blur', 'sharpen', 'saturation', 'lighten', 'darken']
    
    open_photo = MyButton('Open photo')
    save_photo = MyButton('Save photo')
    path = ft.Text('No opened photo')

    navbar = ft.Container(
        width=page.window_max_width,
        height=60,
        bgcolor='#323445',
        content=ft.Row(
            controls=[ft.Container(ft.Text(value='Photo Editor', size=25),
                                   margin=ft.margin.only(left=20)),
                      ft.Icon(ft.icons.ENHANCE_PHOTO_TRANSLATE_ROUNDED),
                      ft.VerticalDivider(width=20, thickness=2),
                      open_photo.build_file(),
                      save_photo.build_file(),
                      path
            ],   
        ),
    )

    edit_options = ft.ListView(expand=True, spacing=20, padding=20)
    for option in options_names:
        edit_options.controls.append(MyButton(option).build_option())

    sidebar = ft.Container(
        width=215,
        height=page.window_height,
        bgcolor='#202230',
        content=edit_options,
    )

    photo = ft.Container(
        width=1200,
        height=800,
        bgcolor=ft.colors.TRANSPARENT,
        border=ft.border.all(width=0.2, color='white'),
    )

    canvas = ft.Container(
        width=1720,
        height=1050,
        content=photo,
        alignment=ft.alignment.Alignment(0, -0.4)
    )

    workspace = ft.Container(
        ft.Row(controls=[sidebar, canvas]),
         margin=ft.margin.symmetric(vertical=-10)
    )

    page.add(navbar)
    page.add(workspace)