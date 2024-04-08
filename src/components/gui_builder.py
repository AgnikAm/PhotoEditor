import flet as ft
import numpy as np
from components.buttons import MyButton
from components.contex_menu import build_content
from functions.image_operations import add_image_operation
from functions.files_operations import undo_command, redo_command, pick_files_open, pick_file_save


class GUIBuilder:
    
    def __init__(
            self, 
            page: ft.Page, 
            orig_path: ft.Text,
            curr_path: ft.Text,
            image_arr: ft.Ref[np.ndarray],
    ):
        self.page = page
        self.original_path = orig_path
        self.current_path = curr_path
        self.image_flet = ft.Image(src=self.original_path)
        self.image_arr = image_arr

        self.open_picker = ft.FilePicker(
            on_result=lambda e: pick_files_open(
                self.original_path, 
                self.current_path, 
                self.image_flet, 
                self.image_arr, 
                e
            )
        )
        self.save_picker = ft.FilePicker(
            on_result=lambda e: pick_file_save( 
                self.image_arr,
                self.image_flet, 
                e
            )
        )
        self.page.overlay.append(self.open_picker)
        self.page.overlay.append(self.save_picker)


    def open_btn(self) -> MyButton:
        open_btn = MyButton('Open photo')
        open_btn.define_onclick(
            lambda _: self.open_picker.pick_files(
                allow_multiple=False,
                allowed_extensions=['png', 'jpg', 'jpeg']
            )
        )

        return open_btn

    
    def save_btn(self) -> MyButton:
        save_btn = MyButton('Save photo')
        save_btn.define_onclick(
            lambda _: self.save_picker.save_file(
                allowed_extensions=['png', 'jpg', 'jpeg']
            )
        )

        return save_btn


    def navbar(self, button1: MyButton, button2: MyButton) -> ft.Container:
        return ft.Container(
            width=self.page.window_max_width,
            height=70,
            bgcolor='#323445',
            content=ft.Row(
                controls=[
                    ft.Container(
                        ft.Text(value='Photo Editor', size=25),
                        margin=ft.margin.only(left=50)
                    ),
                    ft.Container(
                          ft.Icon(ft.icons.ENHANCE_PHOTO_TRANSLATE_ROUNDED),
                          margin=ft.margin.only(right=30)
                    ),
                    ft.VerticalDivider(width=20, thickness=2),
                    button1.build_file(),
                    button2.build_file(),
                    self.original_path
                ],   
            ),
        )


    def operation_btn(self, operation: str, cont: ft.Container) -> ft.FilledButton:
        operation_btn = MyButton(operation)
        if operation not in ['rotate', 'black & white', 'sepia', 'inversion']:
            operation_btn.define_onclick(lambda _: self.option_animate(operation, cont))
        else:
            operation_btn.define_onclick(lambda _: add_image_operation(operation, self.image_arr, self.image_flet))

        operation_btn = operation_btn.build_operation()

        return operation_btn


    def operation_options(self, operation: str) -> ft.Container:
        return ft.Container(
            width=300,
            height=3,
            bgcolor='#1d3678',
            margin=ft.margin.only(top=-5),
            border_radius=ft.border_radius.only(bottom_left=5, bottom_right=5),
            animate=ft.animation.Animation(500, "ease"),
            content=build_content(operation, self.image_arr, self.image_flet)
        )


    def option_animate(self, operation: str, cont: ft.Container) -> None:
        match operation:
            case 'rotate':
                pass
            case 'grayscale':
                pass
            case 'flip':
                cont.height = 100 if cont.height == 3 else 3
            case 'resize':
                cont.height = 165 if cont.height == 3 else 3
            case 'color adjustments':
                cont.height = 240 if cont.height == 3 else 3
            case 'solid overlay':
                cont.height = 430 if cont.height == 3 else 3
            case 'gradient overlay':
                cont.height = 810 if cont.height == 3 else 3
            case 'image overlay':
                cont.height = 215 if cont.height == 3 else 3
            case _:
                cont.height = 140 if cont.height == 3 else 3
                
        cont.bgcolor = '#1d3678' if cont.bgcolor == '#374362' else '#374362'
        cont.update()


    def type_divider(self, text: str) -> ft.Column:
        return ft.Column(
            controls=[
                ft.Text(text),
                ft.Divider()
            ]
        )
    

    def edit_options(self) -> ft.Container:
        list_view = ft.ListView(spacing=20, padding=20)
        elements = [
            self.type_divider('Shape'), 
            'rotate',
            'flip',
            'resize',
            self.type_divider('Sharpness'), 
            'blur',
            'sharpen',
            self.type_divider('Colors'), 
            'color adjustments',
            'hue',
            'brightness', 
            'saturation',
            'contrast',
            self.type_divider('Overlays'),
            'solid overlay',
            'gradient overlay',
            self.type_divider('Miscellaneous'),
            'noise',
            'vignette',
            'inversion',
            self.type_divider('Filters'),
            'black & white',
            'sepia',
            'vintage',
            'retro',
            'mojave',
            'nostalgia',
            'clean',
            'neon',
            'twilight'
        ]

        for element in elements:
            if not isinstance(element, str):
                list_view.controls.append(element)
            else:
                operation_btn_container = self.operation_options(element)
                operation_btn = self.operation_btn(element, operation_btn_container)
                list_view.controls.append(ft.Column([operation_btn, operation_btn_container]))

        return ft.Container(content=list_view, margin=ft.margin.only(bottom=140))


    def undo_redo_buttons(self) -> ft.Row:
        undo_icon = ft.Icon(ft.icons.UNDO_ROUNDED, color=ft.colors.WHITE, size=20)
        redo_icon = ft.Icon(ft.icons.REDO_ROUNDED, color=ft.colors.WHITE, size=20)

        undo = MyButton()
        undo.define_onclick(lambda _: undo_command(self.image_arr, self.image_flet))

        redo = MyButton()
        redo.define_onclick(lambda _: redo_command(self.image_arr, self.image_flet))

        undo = undo.build_command(undo_icon)
        redo = redo.build_command(redo_icon)

        return ft.Row(controls=[undo, redo])
    

    def static_sidebar(self) -> ft.Container:
        return ft.Container(
                width=275,
                height=60,
                bgcolor='#202230',
                content=ft.Container(
                    content=self.undo_redo_buttons(),
                    margin=ft.margin.only(left=60)
                )
        )
    

    def dynamic_sidebar(self) -> ft.Container:
        return ft.Container(
                width=275,
                height=self.page.window_height - 60,
                bgcolor='#202230',
                content=self.edit_options()
        )


    def sidebar(self) -> ft.Column:
        return ft.Column(
            controls=[
                self.static_sidebar(),
                ft.Container(
                    content=self.dynamic_sidebar(),
                    margin=ft.margin.only(top=-10)
                )
            ]
        )


    def canvas(self) -> ft.Container:
        return ft.Container(
            width=1400,
            height=780,
            bgcolor=ft.colors.TRANSPARENT,
            border=ft.border.all(width=0.2, color='white'),
            padding=10,
            content=self.image_flet
        )


    def background(self) -> ft.Container:
        return ft.Container(
                width=1650,
                height=1050,
                content=self.canvas(),
                alignment=ft.alignment.Alignment(0, -0.4)
        )


    def workspace(self) -> ft.Container:
        return ft.Container(
            ft.Row(
                controls=[
                    self.sidebar(),
                    self.background()
                ]
            ),
            margin=ft.margin.symmetric(vertical=-10)
        )


    def build(self) -> None:
        gui = ft.Column(
            controls=[
                self.navbar(self.open_btn(), self.save_btn()),
                self.workspace()
            ]
        )

        self.page.add(gui)