import customtkinter
from core import *
from PIL import Image
from io import BytesIO
from data import country_codes
import threading


def fetch_weather():
    threading.Thread(target=_fetch_weather, daemon=True).start()


def _fetch_weather():
    unit = get_unit()
    city = entry.get()
    try:
        (country, weather, description, icon) = get_weather(city, unit)
        print(country, weather, description, icon)
        country_label.configure(text=(city.capitalize() + ', ' + country_codes.get(country)))
        weather_label.configure(text=str(weather) + ' °')
        description_label.configure(text=description.capitalize())

        icon_url = f'https://openweathermap.org/img/wn/{icon}@2x.png'
        response = requests.get(icon_url)
        if response.status_code == 200:
            img_data = response.content     # store the actual image in bytes
            img = Image.open(BytesIO(img_data)) # convert raw bytes into a format pillow can read, bec CTkImage requires
            # a pillow image
            img = customtkinter.CTkImage(light_image=img, dark_image=img, size=(100, 100))

            icon_label.configure(image=img)
            """
            In Tkinter and CustomTkinter, images are handled by Python’s garbage collector.
            If you don’t explicitly keep a reference to the image, Python might delete it after the function ends.
            This means your image could disappear right after being displayed.
            By assigning the image to icon_label.image, the label itself holds a reference, preventing Python from deleting
            it
            """
    except:
        weather_label.configure(text='Invalid City')
        country_label.configure(text='')  # Clear country label
        description_label.configure(text='')  # Clear description
        icon_label.configure(image=None)  # Remove previous icon


def get_unit():
    unit = unit_var.get()
    if unit == 'c':
        unit_switch.configure(text='Celsius')
        return '&units=metric'
    else:
        unit_switch.configure(text='Fahrenheit')
        return '&units=imperial'


def set_mode():
    # dark mode
    if mode_switch.get() == 'off':
        customtkinter.set_appearance_mode('dark')
        mode_switch.configure(text='Dark Mode')
        bottom_frame.configure(fg_color='#333333')
        search_button.configure(
            fg_color='#206ca4',
            bg_color='#333333',
            hover_color='#1a5b8a',
            border_color='#206ca4',
            corner_radius=10,
            text_color='white'
        )

    # light mode
    else:
        customtkinter.set_appearance_mode('light')
        mode_switch.configure(text='Light Mode')
        bottom_frame.configure(fg_color='#4D77FF')
        search_button.configure(
            fg_color='#f0ecec',
            bg_color='#4D77FF',
            hover_color='#d9d9d9',
            border_color='#f0ecec',
            corner_radius=10,
            text_color='#4D77FF'
        )


# constants
APP_DIMENSIONS = '300x500'
MY_FONT = ('Roboto', 12)
DISPLAY_FONT = ('Roboto', 20)
WEATHER_FONT = ('Roboto', 32)

window = customtkinter.CTk()
window.geometry(APP_DIMENSIONS)
window.title('Iron Forecast')
window.resizable(width=False, height=False)


# ---------------------------------------------------
# create a frame for system mode
mode_frame = customtkinter.CTkFrame(window, fg_color='transparent')
# add frame to window
mode_frame.pack(anchor='ne', padx=10, pady=10)

customtkinter.set_appearance_mode('dark')
# add a switch to the frame
mode_var = customtkinter.StringVar()
mode_switch = customtkinter.CTkSwitch(mode_frame,
                                      text='Dark Mode',
                                      command=set_mode,
                                      variable=mode_var,
                                      onvalue='on',
                                      offvalue='off',
                                      font=MY_FONT)
mode_switch.pack()
# ---------------------------------------------------
# add a unit switch to check the unit
unit_var = customtkinter.StringVar(value='c')
unit_switch = customtkinter.CTkSwitch(window,
                                      text='Celsius',
                                      command=get_unit,
                                      variable=unit_var,
                                      onvalue='f',
                                      offvalue='c',
                                      font=MY_FONT)
unit_switch.pack(anchor='ne', padx=10)
# ---------------------------------------------------


# -------------------------- Display Section --------------------------------------------
country_label = customtkinter.CTkLabel(window,
                                       text='',
                                       font=DISPLAY_FONT,
                                       )
country_label.pack(pady=25)

icon_label = customtkinter.CTkLabel(window,
                                    text=''
                                    )
icon_label.pack(pady=10)

weather_label = customtkinter.CTkLabel(window,
                                       text='',
                                       font=WEATHER_FONT)
weather_label.pack(pady=15)

description_label = customtkinter.CTkLabel(window,
                                           text='',
                                           font=DISPLAY_FONT)
description_label.pack(pady=10)

# ---------------------------------------------------------------------------------------
# create an Entry that is going to take the city name and the search button
bottom_frame = customtkinter.CTkFrame(window,
                                      fg_color='#333333',
                                      width=window.winfo_width(),
                                      corner_radius=10
                                      )
bottom_frame.pack(side='bottom', fill='x')
entry = customtkinter.CTkEntry(bottom_frame,
                               placeholder_text='Enter a city',
                               font=('Roboto', 18),
                               width=250
                               )
entry.pack(pady=10)
search_button = customtkinter.CTkButton(bottom_frame,
                                        text='Get Weather',
                                        width=250,
                                        font=('Roboto', 18),
                                        command=fetch_weather
                                        )
search_button.pack(pady=10)


window.mainloop()
