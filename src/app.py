import flet as ft

def main(page: ft.Page) -> None:
    page.title = 'PhotoEditor'
    page.bgcolor = '#16171d'
    page.window_max_height=1080
    page.window_max_width=1920
    page.padding=0

    open_photo_btn = ft.OutlinedButton(
        content=ft.Text(value='Open photo'),
        style=ft.ButtonStyle(
            bgcolor={ft.MaterialState.DEFAULT: '#374362',
                     ft.MaterialState.HOVERED: '#1d3678'}
        )
    )

    save_photo_btn = ft.OutlinedButton(
        content=ft.Text(value='Save photo'),
        style=ft.ButtonStyle(
            bgcolor={ft.MaterialState.DEFAULT: '#374362',
                     ft.MaterialState.HOVERED: '#1d3678'}
        )
    )

    blur_btn = ft.FilledButton(
        content=ft.Text(value='Blur'),
        style=ft.ButtonStyle(
            color='white',
            bgcolor={ft.MaterialState.DEFAULT: '#374362',
                     ft.MaterialState.HOVERED: '#1d3678'},
            shape=ft.RoundedRectangleBorder(radius=5)
        )
    )

    sharpen_btn = ft.FilledButton(
        content=ft.Text(value='Sharpen'),
        style=ft.ButtonStyle(
            color='white',
            bgcolor={ft.MaterialState.DEFAULT: '#374362',
                     ft.MaterialState.HOVERED: '#1d3678'},
            shape=ft.RoundedRectangleBorder(radius=5)
        )
    )

    navbar = ft.Container(
        width=page.window_max_width,
        height=60,
        bgcolor='#323445',
        content=ft.Row(
            controls=[ft.Container(ft.Text(value='Photo Editor', size=25),
                                   margin=ft.margin.only(left=20)),
                      ft.Icon(ft.icons.ENHANCE_PHOTO_TRANSLATE_ROUNDED),
                      ft.VerticalDivider(width=20, thickness=2),
                      open_photo_btn,
                      save_photo_btn
            ],          
        ),
    )

    edit_options = ft.ListView(expand=True, spacing=20, padding=20, auto_scroll=True)
    edit_options.controls.append(blur_btn)
    edit_options.controls.append(sharpen_btn)

    sidebar_menu = ft.Container(
        width=215,
        height=page.window_max_height,
        bgcolor='#202230',
        content=edit_options
    )

    photo = ft.Container(
        width=1200,
        height=800,
        bgcolor=ft.colors.TRANSPARENT,
        border=ft.border.all(width=0.2, color='white'),
    )

    wrapper = ft.Container(
        width=1700,
        height=1050,
        content=photo,
        alignment=ft.alignment.Alignment(0, -0.4)
    )

    workspace = ft.Container(
        ft.Row(controls=[sidebar_menu, wrapper]),
        margin=ft.margin.symmetric(vertical=-10),
    )

    page.add(navbar)
    page.add(workspace)
    



