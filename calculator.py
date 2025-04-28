import customtkinter as ctk
from buttons import Button, ImageButton, NumButton, MathButton, MathImageButton
from PIL import Image
import darkdetect
from settings import *
try:
    import ctypes
except:
    pass

class Calculator(ctk.CTk):
    def __init__(self, is_dark):
        
        # setup
        super().__init__(fg_color= (WHITE, BLACK))
        ctk.set_appearance_mode(f"{"dark" if is_dark else "light"}")
        self.geometry(f"{APP_SIZE[0]}x{APP_SIZE[1]}+{int(self.winfo_screenwidth() / 2 - APP_SIZE[0] / 2)}+{int(self.winfo_screenheight() / 2 - APP_SIZE[1] / 2)}")
        self.resizable(False, False)
        self.title("")
        self.iconbitmap("empty.ico")
        self.change_title_bar_color(is_dark)
        
        # grid layout
        self.rowconfigure(list(range(MAIN_ROWS)), weight = 1, uniform = "a")
        self.columnconfigure(list(range(MAIN_COLUMNS)), weight = 1, uniform = "a")
        
        # data
        self.result_string = ctk.StringVar(value= "0")
        self.formula_string = ctk.StringVar(value= "")
        self.display_nums = []
        self.full_operation = []
        
        # widgets
        self.create_widgets()
        self.mainloop()
           
    def create_widgets(self):
        # font 
        main_font = ctk.CTkFont(family= FONT, size= NORMAL_FONT_SIZE)
        result_font = ctk.CTkFont(family= FONT, size= OUTPUT_FONT_SIZE)
        
        OutputLabel(self, 0, "se", main_font, self.formula_string)
        OutputLabel(self, 1, "e", result_font, self.result_string)
        
        # clear (AC) button
        Button(parent= self,
               text= OPERATORS["clear"]["text"],
               func =  self.clear,
               col= OPERATORS["clear"]["col"], 
               row= OPERATORS["clear"]["row"],
               font= main_font,
               color= COLORS["dark-gray"])
        
        # percentage button
        Button(parent= self,
               text= OPERATORS["percent"]["text"],
               func =  self.perencent,
               col= OPERATORS["percent"]["col"], 
               row= OPERATORS["percent"]["row"],
               font= main_font,
               color= COLORS["dark-gray"])

        # invert button
        invert_image = ctk.CTkImage(
            light_image= Image.open(OPERATORS["invert"]["image path"]["dark"]),
            dark_image= Image.open(OPERATORS["invert"]["image path"]["light"])
            )
        ImageButton(
            parent= self,
            text= OPERATORS["invert"]["text"],
            col= OPERATORS["invert"]["col"],
            row= OPERATORS["invert"]["row"],
            image= invert_image,
            func= self.invert, 
            color= COLORS["dark-gray"]
            )
        
        # num buttons
        for num, data in NUM_POSITION.items():
            NumButton(
                parent= self,
                text= num,
                func= self.num_press,
                col= data["col"],
                row= data["row"],
                font= main_font,
                color= COLORS["light-gray"],
                span= data["span"]  
            )
            
        # math buttons
        for _, data in MATH_POSITIONS.items():
            if data["image path"]:
                divide_image = ctk.CTkImage(
                    light_image= Image.open(data["image path"]["dark"]),
                    dark_image= Image.open(data["image path"]["light"])
                )
                MathImageButton(
                    parent= self,
                    text= data["character"],
                    image= divide_image,
                    operator= data["operator"],
                    func= self.math_press,
                    col= data["col"],
                    row= data["row"],
                    color= COLORS["orange"]
                )
                
            else:
                MathButton(
                    parent= self,
                    text= data["character"],
                    operator= data["operator"],
                    func= self.math_press,
                    col= data["col"],
                    row= data["row"],
                    font= main_font,
                    color= COLORS["orange"]
                )
             
    def num_press(self, value):
        self.display_nums.append(str(value))
        full_number = "".join(self.display_nums)
        self.result_string.set(full_number)
             
    def math_press(self, value):
        current_num = "".join(self.display_nums)
        
        if current_num:
            self.full_operation.append(current_num)
            if value != "=":
                self.full_operation.append(value)
                self.display_nums.clear()
                
                # update output
                self.result_string.set("")
                self.formula_string.set(" ".join(self.full_operation))
        
            else:
                formula = " ".join(self.full_operation)
                result = eval(formula) 
                
                if isinstance(result, float):
                    if result.is_integer():
                        result = int(result)
                    else:
                        result = round(result, 5)
                
                # update data
                self.result_string.set(result)
                self.full_operation.clear()
                
                # update output
                self.formula_string.set(formula)
                self.display_nums = [str(result)]
                        
    def clear(self):
        # updata output
        self.result_string.set(0)
        self.formula_string.set("")
        
        # update data
        self.display_nums.clear()
        self.full_operation.clear()
    
    def perencent(self):
        if self.display_nums:
            current_num = float("".join(self.display_nums))
            percent_num = current_num / 100
            
            # update data
            self.display_nums = list(str(percent_num))
            self.result_string.set("".join(self.display_nums))
    
    def invert(self):
        current_num = "".join(self.display_nums)
        
        if current_num:
            if float(current_num) > 0:
                self.display_nums.insert(0, "-")
                
            else:
                del self.display_nums[0]
            
            self.result_string.set("".join(self.display_nums))
                
    def change_title_bar_color(self, is_dark):
        try:   
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
            DWMWA_CAPTION_COLOR = 35
            COLOR = TITLE_BAR_HEX_COLORS["dark"] if is_dark else TITLE_BAR_HEX_COLORS["light"]
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd,
                DWMWA_CAPTION_COLOR,
                ctypes.byref(ctypes.c_int(COLOR)),
                ctypes.sizeof(ctypes.c_int)
            ) 
        except:
            pass   
        
class OutputLabel(ctk.CTkLabel):
    def __init__(self, parent, row, anchor, font, string_var):
        super().__init__(parent, font= font, textvariable = string_var)
        self.grid(column = 0, row = row, columnspan = 4, sticky = anchor, padx = 10)

if __name__ == "__main__":
    Calculator(darkdetect.isDark())