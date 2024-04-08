import flet as ft
import numpy as np
from components.gui_builder import GUIBuilder
from functions.files_operations import pick_files_open, pick_file_save


def main(page: ft.Page) -> None:
    page.title = 'Photo Editor'
    page.bgcolor = '#16171d'
    page.window_height = 1080
    page.window_width = 1920
    page.padding = 0

    original_path = ft.Text(value='No opened photo')
    current_path = ft.Text(value='No opened photo')
    image_arr = ft.Ref[np.ndarray]()
    image_arr.value = None

    gui = GUIBuilder(
        page, 
        original_path,
        current_path,
        image_arr
    )

    gui.build()
