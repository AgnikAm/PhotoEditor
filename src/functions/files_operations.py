import shutil
import os
from io import BytesIO
import flet as ft
import numpy as np
import base64
from PIL import Image

def create_copy(file_path: str) -> str:
    file_name = os.path.basename(file_path)
    destination_dir = '../tmp/'

    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    destination = os.path.join(destination_dir, file_name)
    shutil.copyfile(file_path, destination)

    return destination


def pick_files_open(old_path, new_path, photo_flet, photo_arr, e: ft.FilePickerResultEvent) -> None:
    if e.files:
        file_path = e.files[0].path.replace("\\", "/")
        photo_flet.src_base64 = ""
        old_path.value = file_path
        old_path.update()

        new_file_path = create_copy(file_path)
        new_path.value = new_file_path
        photo_flet.src = new_file_path
        photo_arr.value = np.asarray(open_image(new_file_path))

        photo_flet.update()


def pick_file_save(photo_arr: np.ndarray, e: ft.FilePickerResultEvent) -> None:
    save_location = e.path
    if save_location:
        save_image(photo_arr, save_location)


def save_image(photo_arr: np.ndarray, output_path: str) -> None:
    image_pil = Image.fromarray(photo_arr.value)
    image_pil.save(output_path)


def open_image(file_path: str) -> Image.Image:
    return Image.open(file_path)
     

def delete_all_files(folder_path) -> None:
    files = os.listdir(folder_path)
    
    for file in files:
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)


def update_image(photo_arr: np.ndarray, photo_flet: ft.Ref[ft.Image]) -> None:
    image_pil = Image.fromarray(photo_arr.value)
    buff = BytesIO()
    image_pil.save(buff, format='PNG')
    src_base64 = base64.b64encode(buff.getvalue()).decode("utf-8")

    photo_flet.src_base64 = src_base64
    photo_flet.update()
