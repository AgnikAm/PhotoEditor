import flet as ft
import numpy as np
import cv2
from PIL import Image, ImageFilter, ImageChops
from functions.files_operations import update_image, add_to_history
from typing import Callable, Optional


def rotate(image_arr: ft.Ref[np.ndarray], image_flet: ft.Image) -> None:
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

    add_to_history(image_arr)
    update_image(image_arr, image_flet)


def resize(image_arr: ft.Ref[np.ndarray], image_flet: ft.Image, values: list[float]) -> None:
    if values is None:
        return
    
    
    new_width = int(values[0])
    new_height = int(values[1])
    
    image_arr.value = cv2.resize(image_arr.value, (new_width, new_height), interpolation=cv2.INTER_LINEAR)

    add_to_history(image_arr)
    update_image(image_arr, image_flet)


def blur(image_arr: ft.Ref[np.ndarray], image_flet: ft.Image, blur_factor: list[float]) -> None:
    if blur_factor is None:
        return
    

    pil_image = Image.fromarray(image_arr.value)
    blurred_image = pil_image.filter(ImageFilter.GaussianBlur(blur_factor[0]))
    image_arr.value = np.array(blurred_image)

    add_to_history(image_arr)
    update_image(image_arr, image_flet)


def sharpen(image_arr: ft.Ref[np.ndarray], image_flet: ft.Image, kernel_size: list[float]) -> None:
    if kernel_size is None:
        return
    
    mapping = {
        0: 1,
        1: 3,
        2: 5,
        3: 7,
        4: 9,
        5: 11,
        6: 13,
        7: 15,
        8: 17,
        9: 19,
        10: 21
    }

    kernel_size = mapping[kernel_size[0]]
    
    blurred = cv2.GaussianBlur(image_arr.value, (kernel_size, kernel_size), 1.0)
    sharpened = 2.0 * image_arr.value - float(1.0) * blurred
    
    sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
    sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
    sharpened = sharpened.round().astype(np.uint8)
    
    image_arr.value = np.array(sharpened)

    add_to_history(image_arr)
    update_image(image_arr, image_flet)


def brightness(image_arr: ft.Ref[np.ndarray], image_flet: ft.Image, brightness_factor: list[float]):
    if brightness_factor is None:
        return

    if image_arr.value.shape[2] == 4:
        bgr_image = image_arr.value[:, :, :3]
        alpha_channel = image_arr.value[:, :, 3]

        hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)
        hsv_image[:, :, 2] = np.clip(hsv_image[:, :, 2] + brightness_factor[0], 0, 255)
        bgr_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

        image_arr.value = np.dstack((bgr_image, alpha_channel))
    else:
        bgr_image = image_arr.value

        hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)
        hsv_image[:, :, 2] = np.clip(hsv_image[:, :, 2] + brightness_factor[0], 0, 255)
        bgr_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

        image_arr.value = bgr_image

    add_to_history(image_arr)
    update_image(image_arr, image_flet)


def saturation(image_arr: ft.Ref[np.ndarray], image_flet: ft.Image, saturation_factor: list[float]) -> None:
    if saturation_factor is None:
        return

    if image_arr.value.shape[2] == 4:
        bgr_image = image_arr.value[:, :, :3]
        alpha_channel = image_arr.value[:, :, 3]

        hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)
        hsv_image[:, :, 1] = np.clip(hsv_image[:, :, 1] * saturation_factor[0], 0, 255)
        bgr_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

        image_arr.value = np.dstack((bgr_image, alpha_channel))
    else:
        bgr_image = image_arr.value

        hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)
        hsv_image[:, :, 1] = np.clip(hsv_image[:, :, 1] * saturation_factor[0], 0, 255)
        bgr_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

        image_arr.value = bgr_image

    add_to_history(image_arr)
    update_image(image_arr, image_flet)
    

def add_image_operation(name: str, image_arr: ft.Ref[np.ndarray], image_flet: ft.Image, values: Optional[list] = None) -> Callable:
    match name:
        case 'rotate':
            return rotate(image_arr, image_flet)
        case 'resize':
            return resize(image_arr, image_flet, values)
        case 'blur':
            return blur(image_arr, image_flet, values)
        case 'sharpen':
            return sharpen(image_arr, image_flet, values)
        case 'brightness':
            return brightness(image_arr, image_flet, values)
        case 'saturation':
            return saturation(image_arr, image_flet, values)
        