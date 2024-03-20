import flet as ft
import numpy as np
import cv2
from functions.files_operations import update_image
from typing import Callable


def rotate(image_arr: np.ndarray, image_flet: ft.Image):
    angle = 90
    height, width = image_arr.value.shape[:2]
    center = (width // 2, height // 2)

    abs_cos, abs_sin = abs(np.cos(np.radians(angle))), abs(np.sin(np.radians(angle)))
    bound_w = int(height * abs_sin + width * abs_cos)
    bound_h = int(height * abs_cos + width * abs_sin)

    rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale=1.0)
    rotation_matrix[0, 2] += bound_w / 2 - center[0]
    rotation_matrix[1, 2] += bound_h / 2 - center[1]

    image_arr.value = cv2.warpAffine(image_arr.value, rotation_matrix, (bound_w, bound_h), flags=cv2.INTER_NEAREST)
    update_image(image_arr, image_flet)


def resize(image_arr: np.ndarray, image_flet: ft.Image):
    image_arr.value = cv2.resize(image_arr.value, (300, 300), interpolation=cv2.INTER_LINEAR)
    update_image(image_arr, image_flet)


def add_image_operation(name: str, image_arr: np.ndarray, image_flet: ft.Image) -> Callable:
    match name:
        case 'rotate':
            return rotate(image_arr, image_flet)
        case 'resize':
            return resize(image_arr, image_flet)
        