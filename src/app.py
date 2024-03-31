import flet as ft
import numpy as np
from PIL import Image
from components.buttons import MyButton
from components.main_components import build_navbar, build_edit_options, undo_redo_buttons, build_sidebar, build_canvas, build_background, build_workspace
from functions.files_operations import pick_files_open, pick_file_save


def main(page: ft.Page) -> None:
    page.title = 'PhotoEditor'
    page.bgcolor = '#16171d'
    page.window_height = 1080
    page.window_width = 1920
    page.padding = 0

    original_path = ft.Ref[ft.Text]()
    current_path = ft.Ref[ft.Text]()
    photo_flet = ft.Ref[ft.Image]()
    photo_arr = ft.Ref[np.ndarray]()
    photo_arr.value = None
    
    open_photo_pick = ft.FilePicker(on_result=lambda e: pick_files_open(original_path, current_path, photo_flet, photo_arr, e))
    save_photo_pick = ft.FilePicker(on_result=lambda e: pick_file_save(photo_arr, photo_flet, e))
    page.overlay.append(open_photo_pick)
    page.overlay.append(save_photo_pick)
    
    open_photo = MyButton('Open photo')
    open_photo.define_onclick(lambda _: open_photo_pick.pick_files(
        allow_multiple=False,
        allowed_extensions=['png', 'jpg', 'jpeg']
        )
    )
    
    save_photo = MyButton('Save photo')
    save_photo.define_onclick(lambda _: save_photo_pick.save_file(
        allowed_extensions=['png', 'jpg', 'jpeg']
    ))

    original_path = ft.Text(ref=original_path, value='No opened photo')
    current_path = ft.Text(ref=current_path, value='No opened photo')

    navbar = build_navbar(page, open_photo, save_photo, original_path)
    photo_flet = ft.Image(src=current_path.value)

    edit_options = build_edit_options(photo_arr, photo_flet)
    command_buttons = ft.Container(undo_redo_buttons(photo_arr, photo_flet), margin=ft.margin.only(left=60))

    static_sidebar = build_sidebar(60, command_buttons)
    dynamic_sidebar = build_sidebar(page.window_height - static_sidebar.height, edit_options)

    sidebar = ft.Column(
        controls=[
            static_sidebar,
            ft.Container(
                content=dynamic_sidebar,
                margin=ft.margin.only(top=-10)
            )
        ]
    )

    canvas = build_canvas(photo_flet)
    background = build_background(canvas)
    workspace = build_workspace([sidebar, background])

    page.add(navbar)
    page.add(workspace)
    page.update()