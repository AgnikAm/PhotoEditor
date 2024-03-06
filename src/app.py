import flet as ft
from buttons import MyButton

def main(page: ft.Page) -> None:
    page.title = 'PhotoEditor'
    page.bgcolor = '#16171d'
    page.window_height = 1080
    page.window_width = 1920
    page.padding = 0

    options = ['rotate', 'zoom', 'blur', 'sharpen', 'saturation', 'lighten', 'darken']

    def pick_files_result(e: ft.FilePickerResultEvent):
        if e.files:
            file_path = e.files[0].path.replace("\\", "/")
            path.value = file_path
            photo.src = file_path

            path.update()
            photo.update()
    

    open_photo_pick = ft.FilePicker(on_result=pick_files_result)
    page.overlay.append(open_photo_pick)
    
    open_photo = MyButton('Open photo')
    open_photo.define_onclick(lambda _: open_photo_pick.pick_files(
        allow_multiple=False,
        file_type=ft.FilePickerFileType.IMAGE
        )
    )
    
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
    for option in options:
        edit_options.controls.append(MyButton(option).build_option())

    sidebar = ft.Container(
        width=215,
        height=page.window_height,
        bgcolor='#202230',
        content=edit_options,
    )

    photo = ft.Image(src=path.value)

    canvas = ft.Container(
        width=1400,
        height=780,
        bgcolor=ft.colors.TRANSPARENT,
        border=ft.border.all(width=0.2, color='white'),
        padding=10,
        content=photo
    )

    background = ft.Container(
        width=1720,
        height=1050,
        content=canvas,
        alignment=ft.alignment.Alignment(0, -0.4)
    )

    workspace = ft.Container(
        ft.Row(controls=[sidebar, background]),
         margin=ft.margin.symmetric(vertical=-10)
    )

    page.add(navbar)
    page.add(workspace)
    page.update()