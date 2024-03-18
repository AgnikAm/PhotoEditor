import flet as ft
from PIL import Image
from buttons import MyButton
from components import build_navbar, build_edit_options, build_sidebar, build_canvas, build_background, build_workspace
from functions.files_operations import pick_files_open, pick_file_save, open_image


def main(page: ft.Page) -> None:
    page.title = 'PhotoEditor'
    page.bgcolor = '#16171d'
    page.window_height = 1080
    page.window_width = 1920
    page.padding = 0

    original_path = ft.Ref[ft.Text]()
    current_path = ft.Ref[ft.Text]()
    photo_flet = ft.Ref[ft.Image]()
    photo_pil = ft.Ref[Image.Image]()
    
    open_photo_pick = ft.FilePicker(on_result=lambda e: pick_files_open(original_path, current_path, photo_flet, photo_pil, e))
    save_photo_pick = ft.FilePicker(on_result=lambda e: pick_file_save(photo_pil.value, e))
    page.overlay.append(open_photo_pick)
    page.overlay.append(save_photo_pick)
    
    open_photo = MyButton('Open photo')
    open_photo.define_onclick(lambda _: open_photo_pick.pick_files(
        allow_multiple=False,
        file_type=ft.FilePickerFileType.IMAGE
        )
    )
    
    save_photo = MyButton('Save photo')
    save_photo.define_onclick(lambda _: save_photo_pick.save_file())

    original_path = ft.Text(ref=original_path, value='No opened photo')
    current_path = ft.Text(ref=current_path, value='No opened photo')

    navbar = build_navbar(page, open_photo, save_photo, original_path)
    edit_options = build_edit_options()
    sidebar = build_sidebar(page, edit_options)
    photo_flet = ft.Image(src=original_path.value)
    canvas = build_canvas(photo_flet)
    background = build_background(canvas)
    workspace = build_workspace([sidebar, background])

    page.add(navbar)
    page.add(workspace)
    page.update()