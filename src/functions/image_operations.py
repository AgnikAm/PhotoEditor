import flet as ft
import numpy as np
import cv2
import math
from PIL import Image, ImageFilter
from functions.files_operations import update_image, add_to_history
from typing import Callable, Optional


def rotate(image_arr: ft.Ref[np.ndarray], values: Optional[list]) -> None:
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


def flip(image_arr: ft.Ref[np.ndarray], values: list[float]) -> None:
    if image_arr.value is None:
        return
    
    flipped_image = cv2.flip(image_arr.value, int(values[0]))
    image_arr.value = flipped_image


def resize(image_arr: ft.Ref[np.ndarray], values: list[float]) -> None:
    if image_arr.value is None or values is None:
        return
    
    new_width = int(values[0])
    new_height = int(values[1])
    
    image_arr.value = cv2.resize(image_arr.value, (new_width, new_height), interpolation=cv2.INTER_LINEAR)


def blur(image_arr: ft.Ref[np.ndarray], blur_factor: list[float]) -> None:
    if image_arr.value is None or blur_factor is None:
        return
    
    pil_image = Image.fromarray(image_arr.value)
    blurred_image = pil_image.filter(ImageFilter.GaussianBlur(blur_factor[0]))
    image_arr.value = np.array(blurred_image)


def sharpen(image_arr: ft.Ref[np.ndarray], sharpen_factor: list[float]) -> None:
    if image_arr.value is None or sharpen_factor is None:
        return
    
    sharpened_channels = []
    for channel in cv2.split(image_arr.value):
        blurred_channel = cv2.GaussianBlur(channel, (0, 0), sharpen_factor[0])
        unsharp_mask = cv2.addWeighted(channel, 1.0 + sharpen_factor[0], blurred_channel, -sharpen_factor[0], 0)
        sharpened_channels.append(unsharp_mask)
    
    sharpened_image = cv2.merge(sharpened_channels)
    
    image_arr.value = sharpened_image


def noise(image_arr: ft.Ref[np.ndarray], noise_intensity: list[float]) -> None:
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


def color_adjustments(image_arr: ft.Ref[np.ndarray], colors: list[float]) -> None:
    if image_arr.value is None or image_arr.value.shape[2] < 3 or colors is None:
        return
    
    image = image_arr.value.astype(np.float32)
    image[:, :, 0] *= colors[0]
    image[:, :, 1] *= colors[1]
    image[:, :, 2] *= colors[2]

    image = np.clip(image, 0, 255).astype(np.uint8)
    image_arr.value = image


def hue(image_arr: ft.Ref[np.ndarray], hue_factor: list[float]) -> None:
    if image_arr.value is None or image_arr.value.shape[2] < 3 or hue_factor is None:
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


def brightness(image_arr: ft.Ref[np.ndarray], brightness_factor: list[float]):
    if image_arr.value is None or brightness_factor is None:
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


def saturation(image_arr: ft.Ref[np.ndarray], saturation_factor: list[float]) -> None:
    if image_arr.value is None or saturation_factor is None :
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


def contrast(image_arr: ft.Ref[np.ndarray], contrast_factor: list[float]) -> None:
    if image_arr.value is None or contrast_factor is None:
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


def generate_gradient(
        width: int, 
        height: int, 
        direction: str, 
        color_start: tuple[int, int, int], 
        color_end: tuple[int, int, int]
    ) -> np.ndarray:
    
    gradient = np.zeros((height, width, 3), dtype=np.uint8)

    if direction == 'horizontal':
        for x in range(width):
            gradient[:, x, 0] = np.interp(x, (0, width - 1), (color_start[0], color_end[0]))
            gradient[:, x, 1] = np.interp(x, (0, width - 1), (color_start[1], color_end[1]))
            gradient[:, x, 2] = np.interp(x, (0, width - 1), (color_start[2], color_end[2]))
            
    elif direction == 'vertical':
        for y in range(height):
            gradient[y, :, 0] = np.interp(y, (0, height - 1), (color_start[0], color_end[0]))
            gradient[y, :, 1] = np.interp(y, (0, height - 1), (color_start[1], color_end[1]))
            gradient[y, :, 2] = np.interp(y, (0, height - 1), (color_start[2], color_end[2]))
            
    elif direction == 'diagonal':
        for y in range(height):
            for x in range(width):
                t = min(x / width, y / height)
                gradient[y, x, 0] = int(color_start[0] + t * (color_end[0] - color_start[0]))
                gradient[y, x, 1] = int(color_start[1] + t * (color_end[1] - color_start[1]))
                gradient[y, x, 2] = int(color_start[2] + t * (color_end[2] - color_start[2]))
    
    elif direction == 'radial':
        center_x = width / 2
        center_y = height / 2
        max_distance = np.sqrt(center_x ** 2 + center_y ** 2)
        for y in range(height):
            for x in range(width):
                distance = np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
                t = min(distance / max_distance, 1)
                gradient[y, x, 0] = int(color_start[0] + t * (color_end[0] - color_start[0]))
                gradient[y, x, 1] = int(color_start[1] + t * (color_end[1] - color_start[1]))
                gradient[y, x, 2] = int(color_start[2] + t * (color_end[2] - color_start[2]))

    return gradient


def apply_gradient(image: np.ndarray, gradient: np.ndarray, opacity: float) -> np.ndarray:
    if len(image.shape) == 3 and image.shape[2] == 4:
        bgr_image = image[:, :, :3]
        alpha_channel = image[:, :, 3]

        non_transparent_pixels = np.where(alpha_channel > 0, True, False)

        blended_bgr = cv2.addWeighted(bgr_image, 1 - opacity, gradient, opacity, 0)
        
        alpha_mask = np.zeros_like(alpha_channel)
        alpha_mask[non_transparent_pixels] = 255

        blended_image = np.dstack((blended_bgr, alpha_mask))
    else:
        blended_image = cv2.addWeighted(image, 1 - opacity, gradient, opacity, 0)

    return blended_image


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    hex_color = hex_color.lstrip('#')
    
    red = int(hex_color[0:2], 16)
    green = int(hex_color[2:4], 16)
    blue = int(hex_color[4:6], 16)
    
    return red, green, blue


def gradient_overlay(image_arr: ft.Ref[np.ndarray], values: list) -> None:
    if values is None or image_arr.value is None:
        return 
    
    direction = values[0]
    first_color = values[1]
    second_color = values[2]
    opacity = values[3]

    gradient = generate_gradient(
        image_arr.value.shape[1],
        image_arr.value.shape[0],
        direction=direction,
        color_start=hex_to_rgb(first_color),
        color_end=hex_to_rgb(second_color)
    )

    image_arr.value = apply_gradient(image_arr.value, gradient, opacity)


def solid_overlay(image_arr: ft.Ref[np.ndarray], values: list) -> None:
    if values is None or image_arr.value is None:
        return 
    
    color = hex_to_rgb(values[0])
    opacity = values[1]
    height, width = image_arr.value.shape[:2]

    solid_color = np.full((height, width, 3), color, dtype=np.uint8)
    blended_image = cv2.addWeighted(image_arr.value, 1 - opacity, solid_color, opacity, 0)

    image_arr.value = blended_image
        

def noise(image_arr: ft.Ref[np.ndarray], noise_intensity: list[float]) -> None:
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


def vignette(image_arr: ft.Ref[np.ndarray], vignette_intensity: list[float]) -> None:
    if image_arr.value is None or vignette_intensity is None:
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


def inversion(image_arr: ft.Ref[np.ndarray], values: Optional[list]) -> None:
    if image_arr.value is None:
        return
    
    if image_arr.value.shape[2] == 3:
        inverted_image = 255 - image_arr.value
        image_arr.value = inverted_image

    elif image_arr.value.shape[2] == 4:
        bgr_image = image_arr.value[:, :, :3]
        alpha_channel = image_arr.value[:, :, 3]

        inverted_image = 255 - bgr_image
        image_arr.value = np.dstack((inverted_image, alpha_channel))


def grayscale(image_arr: ft.Ref[np.ndarray], values: Optional[list]) -> None:
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


def sepia(image_arr: ft.Ref[np.ndarray], values: Optional[list]=None) -> None:
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


def vintage(image_arr: ft.Ref[np.ndarray], strenght: list[float]) -> None:
    if image_arr.value is None or strenght is None:
        return
    
    blur(image_arr, [0.3])
    noise(image_arr, [max(0.4, strenght[0] * 0.5)])
    vignette(image_arr, [max(0.3, strenght[0] * 0.7)])
    sepia(image_arr)
    saturation(image_arr, [1.2])
    vignette(image_arr, [0.2])
    brightness(image_arr, [min(-6, strenght[0] * -16)])


def retro(image_arr: ft.Ref[np.ndarray], strenght: list[float]) -> None:
    if image_arr.value is None or strenght is None:
        return
    
    color_adjustments(image_arr, [0.9, 0.95, 1.1])
    saturation(image_arr, [max(1.1, strenght[0] * 1.3)])
    contrast(image_arr, [max(1.1, strenght[0] * 1.3)])
    brightness(image_arr, [min(-12.0, strenght[0] * -30.0)])
    blur(image_arr, [0.5])
    sharpen(image_arr, [0.7])
    brightness(image_arr, [max(8.0, strenght[0] * 15.0)])
    contrast(image_arr, [1.3])
    brightness(image_arr, [min(-12.0, strenght[0] * -30.0)])
    gradient = generate_gradient(
        image_arr.value.shape[1], 
        image_arr.value.shape[0], 
        direction='vertical', 
        color_start=(122, 141, 173), 
        color_end=(178, 138, 122)
    )
    image_arr.value = apply_gradient(image_arr.value, gradient, strenght[0] * 0.4)
    sharpen(image_arr, [1.3])


def mojave(image_arr: ft.Ref[np.ndarray], strenght: list[float]) -> None:
    if image_arr.value is None or strenght is None:
        return
    
    saturation(image_arr, [0.8])
    gradient = generate_gradient(
        image_arr.value.shape[1], 
        image_arr.value.shape[0], 
        direction='vertical', 
        color_start=(182, 118, 13), 
        color_end=(67, 54, 54)
    )
    image_arr.value = apply_gradient(image_arr.value, gradient, strenght[0] * 0.5)
    blur(image_arr, [0.7])
    brightness(image_arr, [strenght[0] * 15])
    contrast(image_arr, [1.3])


def nostalgia(image_arr: ft.Ref[np.ndarray], strenght: list[float]) -> None:
    if image_arr.value is None or strenght is None:
        return
    
    saturation(image_arr, [0.8])
    gradient = generate_gradient(
        image_arr.value.shape[1], 
        image_arr.value.shape[0], 
        direction='vertical', 
        color_start=(247, 176, 141), 
        color_end=(128, 84, 4)
    )
    image_arr.value = apply_gradient(image_arr.value, gradient, strenght[0] * 0.3)
    blur(image_arr, [max(0.4, strenght[0] * 1)])
    brightness(image_arr, [strenght[0] * 10])
    contrast(image_arr, [0.9])
    sharpen(image_arr, [0.7])


def clean(image_arr: ft.Ref[np.ndarray], strenght: list[float]) -> None:
    if image_arr.value is None or strenght is None:
        return
    
    contrast(image_arr, [max(1, strenght[0] * 1.2)])
    saturation(image_arr, [max(1, strenght[0] * 1.3)])
    sharpen(image_arr, [0.6])

    gradient = generate_gradient(
        image_arr.value.shape[1], 
        image_arr.value.shape[0], 
        direction='diagonal', 
        color_start=(154, 203, 245), 
        color_end=(250, 210, 175)
    )
    
    image_arr.value = apply_gradient(image_arr.value, gradient, strenght[0] * 0.5)
    saturation(image_arr, [max(1, strenght[0] * 1.3)])

def neon(image_arr: ft.Ref[np.ndarray], strenght: list[float]) -> None:
    if image_arr.value is None or strenght is None:
        return
    
    gradient = generate_gradient(
        image_arr.value.shape[1], 
        image_arr.value.shape[0], 
        direction='horizontal', 
        color_start=(148, 2, 201), 
        color_end=(0, 196, 193)
    )
    image_arr.value = apply_gradient(image_arr.value, gradient, strenght[0] * 0.5)
    contrast(image_arr, [max(strenght[0] * 2, 1.3)])
    saturation(image_arr, [1.3])
    sharpen(image_arr, [1.5])


def twilight(image_arr: ft.Ref[np.ndarray], strenght: list[float]) -> None:
    if image_arr.value is None or strenght is None:
        return

    saturation(image_arr, [0.8])
    color_adjustments(image_arr, [0.95, 1.25, 1.25])
    gradient = generate_gradient(
        image_arr.value.shape[1], 
        image_arr.value.shape[0], 
        direction='vertical', 
        color_start=(24, 64, 53), 
        color_end=(18, 42, 66)
    )
    image_arr.value = apply_gradient(image_arr.value, gradient, strenght[0] * 0.4)
    saturation(image_arr, [max(strenght[0] * 1.3, 1)])
    contrast(image_arr, [max(strenght[0] * 1.3, 1)])
    brightness(image_arr, [strenght[0] * -5])
    sharpen(image_arr, [strenght[0] * 0.8])
    vignette(image_arr, [0.8])


def add_image_operation(name: str, image_arr: ft.Ref[np.ndarray], image_flet: ft.Image, values: Optional[list] = None) -> Callable:
    def process_image(image_func: Callable, values: Optional[list] = None):
        image_func(image_arr, values)
        add_to_history(image_arr)
        update_image(image_arr, image_flet)

    image_processing_functions = {
        'rotate': rotate,
        'flip': flip,
        'resize': resize,
        'blur': blur,
        'sharpen': sharpen,
        'color adjustments': color_adjustments,
        'hue': hue,
        'brightness': brightness,
        'saturation': saturation,
        'contrast': contrast,
        'solid overlay': solid_overlay,
        'gradient overlay': gradient_overlay,
        'noise': noise,
        'vignette': vignette,
        'inversion': inversion,
        'black & white': grayscale,
        'sepia': sepia,
        'vintage': vintage,
        'retro': retro,
        'mojave': mojave,
        'nostalgia': nostalgia,
        'clean': clean,
        'neon': neon,
        'twilight': twilight
    }

    if name in image_processing_functions:
        process_image(image_processing_functions[name], values)

        