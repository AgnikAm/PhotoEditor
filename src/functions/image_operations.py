import flet as ft
import numpy as np
import cv2
import math
from PIL import Image, ImageFilter
from functions.files_operations import update_image, add_to_history
from typing import Callable, Optional


def rotate(image_arr: ft.Ref[np.ndarray], image_flet: ft.Image) -> None:
    if image_arr.value is None:
        return
    
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


def flip(image_arr: ft.Ref[np.ndarray], image_flet: ft.Image, values: list[float]) -> None:
    if image_arr.value is None:
        return
    
    flipped_image = cv2.flip(image_arr.value, int(values[0]))
    image_arr.value = flipped_image

    add_to_history(image_arr)
    update_image(image_arr, image_flet)


def resize(image_arr: ft.Ref[np.ndarray], image_flet: ft.Image, values: list[float]) -> None:
    if values is None or image_arr.value is None:
        return
    
    new_width = int(values[0])
    new_height = int(values[1])
    
    image_arr.value = cv2.resize(image_arr.value, (new_width, new_height), interpolation=cv2.INTER_LINEAR)

    add_to_history(image_arr)
    update_image(image_arr, image_flet)


def blur(image_arr: ft.Ref[np.ndarray], image_flet: ft.Image, blur_factor: list[float]) -> None:
    if blur_factor is None or image_arr.value is None:
        return
    
    pil_image = Image.fromarray(image_arr.value)
    blurred_image = pil_image.filter(ImageFilter.GaussianBlur(blur_factor[0]))
    image_arr.value = np.array(blurred_image)

    add_to_history(image_arr)
    update_image(image_arr, image_flet)


def sharpen(image_arr: ft.Ref[np.ndarray], image_flet: ft.Image, kernel_size: list[float]) -> None:
    if kernel_size is None or image_arr.value is None:
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


def noise(image_arr: ft.Ref[np.ndarray], image_flet: ft.Image, noise_intensity: list[float]) -> None:
    if image_arr.value is None:
        return
    
    noise = np.random.normal(scale=noise_intensity[0], size=image_arr.value.shape).astype(np.uint8)
    noisy_image = cv2.add(image_arr.value, noise)
    
    if image_arr.value.shape[2] == 3:
        image_arr.value = noisy_image

    elif image_arr.value.shape[2] == 4:
        alpha_channel = image_arr.value[:, :, 3]
        transparent_pixels = np.where(alpha_channel == 0, True, False)
        noisy_image[transparent_pixels] = image_arr.value[transparent_pixels]
        
        image_arr.value = noisy_image

    add_to_history(image_arr)
    update_image(image_arr, image_flet)


def color_adjustments(image_arr: ft.Ref[np.ndarray], image_flet: ft.Image, colors: list[float]) -> None:
    if colors is None or image_arr.value is None or len(image_arr.value.shape) != 3 or image_arr.value.shape[2] < 3:
        return
    
    image = image_arr.value.astype(np.float32)
    image[:, :, 0] *= colors[0]
    image[:, :, 1] *= colors[1]
    image[:, :, 2] *= colors[2]

    image = np.clip(image, 0, 255).astype(np.uint8)
    image_arr.value = image

    add_to_history(image_arr)
    update_image(image_arr, image_flet)


def hue(image_arr: ft.Ref[np.ndarray], image_flet: ft.Image, hue_factor: list[float]) -> None:
    if hue_factor is None or image_arr.value is None or len(image_arr.value.shape) != 3 or image_arr.value.shape[2] < 3:
        return
    
    if image_arr.value.shape[2] == 3:
        bgr_image = image_arr.value
        hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_RGB2HSV)

        hsv_image[:, :, 0] = (hsv_image[:, :, 0] + hue_factor[0]) % 180
        adjusted_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2RGB)

        image_arr.value = adjusted_image

    elif image_arr.value.shape[2] == 4:
        bgr_image = image_arr.value[:, :, :3]
        alpha_channel = image_arr.value[:, :, 3]

        hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)
        hsv_image[:, :, 0] = (hsv_image[:, :, 0] + hue_factor[0]) % 180
        bgr_adjusted_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

        adjusted_image = np.dstack((bgr_adjusted_image, alpha_channel))

        image_arr.value = adjusted_image

    add_to_history(image_arr)
    update_image(image_arr, image_flet)


def brightness(image_arr: ft.Ref[np.ndarray], image_flet: ft.Image, brightness_factor: list[float]):
    if brightness_factor is None or image_arr.value is None:
        return
    
    if image_arr.value.shape[2] == 3: # RGB no alpha
        bgr_image = image_arr.value

        hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)
        hsv_image[:, :, 2] = np.clip(hsv_image[:, :, 2] + brightness_factor[0], 0, 255)
        bgr_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

        image_arr.value = bgr_image

    elif image_arr.value.shape[2] == 4: # RGB alpha
        bgr_image = image_arr.value[:, :, :3]
        alpha_channel = image_arr.value[:, :, 3]

        hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)
        hsv_image[:, :, 2] = np.clip(hsv_image[:, :, 2] + brightness_factor[0], 0, 255)
        bgr_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

        image_arr.value = np.dstack((bgr_image, alpha_channel))

    add_to_history(image_arr)
    update_image(image_arr, image_flet)


def saturation(image_arr: ft.Ref[np.ndarray], image_flet: ft.Image, saturation_factor: list[float]) -> None:
    if saturation_factor is None or image_arr.value is None:
        return

    if image_arr.value.shape[2] == 3:
        bgr_image = image_arr.value

        hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)
        hsv_image[:, :, 1] = np.clip(hsv_image[:, :, 1] * saturation_factor[0], 0, 255)
        bgr_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

        image_arr.value = bgr_image

    elif image_arr.value.shape[2] == 4:
        bgr_image = image_arr.value[:, :, :3]
        alpha_channel = image_arr.value[:, :, 3]

        hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)
        hsv_image[:, :, 1] = np.clip(hsv_image[:, :, 1] * saturation_factor[0], 0, 255)
        bgr_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

        image_arr.value = np.dstack((bgr_image, alpha_channel))

    add_to_history(image_arr)
    update_image(image_arr, image_flet)


def contrast(image_arr: ft.Ref[np.ndarray], image_flet: ft.Image, contrast_factor: list[float]) -> None:
    if contrast_factor is None or image_arr.value is None:
        return
    
    if len(image_arr.value.shape) == 3 and image_arr.value.shape[2] == 4:
            bgr_image = image_arr.value[:, :, :3]
            alpha_channel = image_arr.value[:, :, 3]

            contrast = contrast_factor[0]
            brightness = int(round(255 * (1 - contrast) / 2))
            adjusted = cv2.addWeighted(bgr_image, contrast, bgr_image, 0, brightness)

            adjusted_with_alpha = np.dstack((adjusted, alpha_channel))

            image_arr.value = adjusted_with_alpha
    else:
        contrast = contrast_factor[0]
        brightness = int(round(255 * (1 - contrast) / 2))
        adjusted = cv2.addWeighted(image_arr.value, contrast, image_arr.value, 0, brightness)

        image_arr.value = adjusted
        

    add_to_history(image_arr)
    update_image(image_arr, image_flet)


def grayscale(image_arr: ft.Ref[np.ndarray], image_flet: ft.Image) -> None:
    if image_arr.value is None:
        return
    
    if image_arr.value.shape[2] == 4:
        bgr_image = image_arr.value[:, :, :3]
        alpha_channel = image_arr.value[:, :, 3]

        grayscale_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
        grayscale_with_alpha = np.dstack((grayscale_image, grayscale_image, grayscale_image, alpha_channel))

        image_arr.value = grayscale_with_alpha

    else:
        grayscale_image = cv2.cvtColor(image_arr.value, cv2.COLOR_BGR2GRAY)

        rgb_image = np.dstack((grayscale_image, grayscale_image, grayscale_image))

        image_arr.value = rgb_image

    add_to_history(image_arr)
    update_image(image_arr, image_flet)


def sepia(image_arr: ft.Ref[np.ndarray], image_flet: ft.Image) -> None:
    if image_arr.value is None:
        return

    sepia_matrix = np.array(
        [
            [0.6, 0.769, 0.189],
            [0.5, 0.686, 0.168],
            [0.4, 0.534, 0.131]
        ]
    )

    if image_arr.value.shape[2] == 3:
        bgr_image = image_arr.value

        sepia_image = np.dot(bgr_image, sepia_matrix.T)
        sepia_image = np.clip(sepia_image, 0, 255).astype(np.uint8)

        image_arr.value = sepia_image

    elif image_arr.value.shape[2] == 4:
        bgr_image = image_arr.value[:, :, :3]
        alpha_channel = image_arr.value[:, :, 3]

        sepia_image = np.dot(bgr_image, sepia_matrix.T)
        sepia_image = np.clip(sepia_image, 0, 255).astype(np.uint8)

        image_arr.value = np.dstack((sepia_image, alpha_channel))

    add_to_history(image_arr)
    update_image(image_arr, image_flet)


import numpy as np
import cv2
import math

def vignette(image_arr: ft.Ref[np.ndarray], image_flet: ft.Image, vignette_intensity: list[float]) -> None:
    if image_arr.value is None:
        return
    
    height, width = image_arr.value.shape[:2]
    y, x = np.ogrid[:height, :width]

    center_x = width / 2
    center_y = height / 2
    distance = np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
    
    max_distance = math.sqrt(center_x ** 2 + center_y ** 2)
    distance_normalized = distance / max_distance
    
    vignette_mask = 1 - vignette_intensity * distance_normalized
    vignette_mask = np.clip(vignette_mask, 0, 1)
    
    if len(image_arr.value.shape) == 3:
        image = image_arr.value.copy()
        for i in range(3):
            image[:, :, i] = image[:, :, i] * vignette_mask

        image_arr.value = image

    elif len(image_arr.value.shape) == 4:
        bgr_image = image_arr.value[:, :, :3].copy()
        alpha_channel = image_arr.value[:, :, 3]
        for i in range(3):
            bgr_image[:, :, i] = bgr_image[:, :, i] * vignette_mask
            
        image_arr.value = np.dstack((bgr_image, alpha_channel))

    add_to_history(image_arr)
    update_image(image_arr, image_flet)


def add_image_operation(name: str, image_arr: ft.Ref[np.ndarray], image_flet: ft.Image, values: Optional[list] = None) -> Callable:
    match name:
        case 'rotate':
            return rotate(image_arr, image_flet)
        case 'flip':
            return flip(image_arr, image_flet, values)
        case 'resize':
            return resize(image_arr, image_flet, values)
        case 'blur':
            return blur(image_arr, image_flet, values)
        case 'sharpen':
            return sharpen(image_arr, image_flet, values)
        case 'noise':
            return noise(image_arr, image_flet, values)
        case 'color adjustments':
            return color_adjustments(image_arr, image_flet, values)
        case 'hue':
            return hue(image_arr, image_flet, values)
        case 'brightness':
            return brightness(image_arr, image_flet, values)
        case 'saturation':
            return saturation(image_arr, image_flet, values)
        case 'contrast':
            return contrast(image_arr, image_flet, values)
        case 'black & white':
            return grayscale(image_arr, image_flet)
        case 'sepia':
            return sepia(image_arr, image_flet)
        case 'vignette':
            return vignette(image_arr, image_flet, values)
        