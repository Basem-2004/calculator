from customtkinter import CTkButton
from settings import *

class Button(CTkButton):
    def __init__(self, parent, text,func, col, row, font, color, span = 1):
        super().__init__(master= parent,
                         text= text,
                         command= func,
                         font= font,
                         corner_radius= STYLING["corner-radius"],
                         fg_color= color["fg"],
                         hover_color= color["hover"],
                         text_color= color["text"])
        self.grid(column = col, row = row, sticky = "nswe", padx = STYLING["gap"], pady = STYLING["gap"], columnspan = span)
        
class NumButton(Button):
    def __init__(self, parent, text, func, col, row, font, color, span):
        super().__init__(
            parent = parent,
            text = text,
            func = lambda : func(text),
            col = col,
            row = row,
            font = font,
            color = color,
            span= span
            )
        
class MathButton(Button):
    def __init__(self, parent, text, operator, func, col, row, font, color, span=1):
        super().__init__(
            parent = parent,
            text = text,
            func = lambda: func(operator),
            col = col,
            row = row,
            font = font,
            color = color,
            span = span
            )   
                 
class ImageButton(CTkButton):
    def __init__(self, parent, text, func, col, row, image, color):
        super().__init__(master= parent,
                         text= text,
                         image= image,
                         command= func,
                         corner_radius= STYLING["corner-radius"],
                         fg_color= color["fg"],
                         hover_color= color["hover"],
                         text_color= color["text"])
        self.grid(column = col, row = row, sticky = "nswe", padx = STYLING["gap"], pady = STYLING["gap"])

class MathImageButton(ImageButton):
        def __init__(self, parent, text, operator, func, col, row,image, color):
            super().__init__(
                parent = parent,
                text = text,
                image= image,
                func = lambda: func(operator),
                col = col,
                row = row,
                color = color
                )      