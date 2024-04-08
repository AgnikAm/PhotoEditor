import shutil
import os
from io import BytesIO
import flet as ft
import numpy as np
import base64
from PIL import Image

history = []
current_index = -1

def add_to_history(image: ft.Ref[np.ndarray]) -> None:
    global history, current_index

    current_index = current_index + 1
    clear_history_forward()
    history.append(image.value)


def read_from_history() -> np.ndarray:
    global history, current_index
    return history[current_index]


def clear_history_forward() -> None:
    global history, current_index
    history = history[:current_index]


def create_copy(file_path: str) -> str:
    file_name = os.path.basename(file_path)
    destination_dir = '../tmp/'

    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    destination = os.path.join(destination_dir, file_name)
    shutil.copyfile(file_path, destination)

    return destination


def pick_files_open(old_path: str, new_path: str, photo_flet: ft.Image, photo_arr: ft.Ref[np.ndarray], e: ft.FilePickerResultEvent) -> None:
    global history, current_index

    if e.files:
        history = []
        photo_flet.src_base64 = ""

        file_path = e.files[0].path.replace("\\", "/")
        old_path.value = file_path
        old_path.update()

        new_file_path = create_copy(file_path)
        new_path.value = new_file_path
        photo_flet.src = new_file_path
        photo_arr.value = np.asarray(open_image(new_file_path))

        add_to_history(photo_arr)
        current_index = 0

        photo_flet.update()


def pick_file_save( photo_flet: ft.Image, photo_arr: ft.Ref[np.ndarray], e: ft.FilePickerResultEvent) -> None:
    save_location = e.path
    if save_location:
        if '.' not in save_location:
            original_extension = os.path.splitext(photo_flet.src)[1]
            save_location += original_extension
            
        save_image(photo_arr, save_location)


def save_image(photo_arr: ft.Ref[np.ndarray], output_path: str) -> None:
    image_pil = Image.fromarray(photo_arr.value)
    image_pil.save(output_path)


def open_image(file_path: str) -> Image.Image:
    return Image.open(file_path)
     

def delete_all_files(folder_path: str) -> None:
    files = os.listdir(folder_path)
    
    for file in files:
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)


def update_image(photo_arr: ft.Ref[np.ndarray], photo_flet: ft.Image) -> None:
    global history

    image_pil = Image.fromarray(photo_arr.value)
    buff = BytesIO()
    image_pil.save(buff, format='PNG')
    src_base64 = base64.b64encode(buff.getvalue()).decode("utf-8")

    photo_flet.src_base64 = src_base64
    photo_flet.update()


def undo_command(photo_arr: ft.Ref[np.ndarray], photo_flet: ft.Image):
    global history, current_index

    if current_index > 0:
        current_index = current_index - 1
        photo_arr.value = read_from_history()
        
        image_pil = Image.fromarray(photo_arr.value)
        buff = BytesIO()
        image_pil.save(buff, format='PNG')
        src_base64 = base64.b64encode(buff.getvalue()).decode("utf-8")

        photo_flet.src_base64 = src_base64
        photo_flet.update()


def redo_command(photo_arr: ft.Ref[np.ndarray], photo_flet: ft.Image):
    global history, current_index

    if len(history) - 1 > current_index:
        current_index = current_index + 1
        photo_arr.value = read_from_history()
        
        image_pil = Image.fromarray(photo_arr.value)
        buff = BytesIO()
        image_pil.save(buff, format='PNG')
        src_base64 = base64.b64encode(buff.getvalue()).decode("utf-8")

        photo_flet.src_base64 = src_base64
        photo_flet.update()