import tkinter as tk
from tkinter import font, messagebox, filedialog
from threading import Thread
import time
import pyautogui
import keyboard
from win10toast import ToastNotifier
import json

class AutoclickerGUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Autoclicker")
        self.toaster = ToastNotifier()

        # Color Palettes
        self.color_palettes = {
            "dark_blue": {"bg": "#001C30", "label_bg": "#176B87", "button_bg": "#64CCC5", "fg": "white"},
            "light_blue": {"bg": "#DAFFFB", "label_bg": "#64CCC5", "button_bg": "#176B87", "fg": "black"},
            "candy": {"bg": "#40128B", "label_bg": "#9336B4", "button_bg": "#DD58D6", "fg": "#FFE79B"},
            "icecream": {"bg": "#FF55BB", "label_bg": "#FFD3A3", "button_bg": "#FCFFB2", "fg": "#B6EAFA"},
            "midnight": {"bg": "#0C134F", "label_bg": "#1D267D", "button_bg": "#5C469C", "fg": "#D4ADFC"},
            "ocean": {"bg": "#F6F1F1", "label_bg": "#AFD3E2", "button_bg": "#19A7CE", "fg": "#146C94"}
        }

        # Variables
        self.Cps = tk.DoubleVar()
        self.num_clicks = tk.IntVar()
        self.theme = tk.StringVar()
        self.theme.set("dark_blue")
        self.cords = tk.StringVar()
        self.middle_button_click_var = tk.BooleanVar()
        self.middle_button_double_click_var = tk.BooleanVar()
        self.middle_button_click_var.set(False)
        self.middle_button_double_click_var.set(False)

        # Menu
        self.menu = tk.Menu(self)
        self.file_menu = tk.Menu(self.menu, tearoff=False)
        self.file_menu.add_command(label="Save Settings", command=self.save_settings)
        self.file_menu.add_command(label="Import Settings", command=self.import_settings)
        self.file_menu.add_command(label="Export Settings", command=self.export_settings)
        self.menu.add_cascade(label="File", menu=self.file_menu)

        self.theme_menu = tk.Menu(self.menu, tearoff=False)
        self.theme_menu.add_radiobutton(label="Dark Blue", variable=self.theme, value="dark_blue", command=self.update_theme)
        self.theme_menu.add_radiobutton(label="Light Blue", variable=self.theme, value="light_blue", command=self.update_theme)
        self.theme_menu.add_radiobutton(label="Candy", variable=self.theme, value="candy", command=self.update_theme)
        self.theme_menu.add_radiobutton(label="Icecream", variable=self.theme, value="icecream", command=self.update_theme)
        self.theme_menu.add_radiobutton(label="Midnight", variable=self.theme, value="midnight", command=self.update_theme)
        self.theme_menu.add_radiobutton(label="Ocean", variable=self.theme, value="ocean", command=self.update_theme)
        self.menu.add_cascade(label="Themes", menu=self.theme_menu)

        self.config(menu=self.menu)

        # GUI Elements
        self.cps_label = tk.Label(self, text="Click Interval:")
        self.cps_entry = tk.Entry(self, textvariable=self.Cps)
        self.clicks_label = tk.Label(self, text="Click Amount:")
        self.clicks_entry = tk.Entry(self, textvariable=self.num_clicks)
        self.start_button = tk.Button(self, text="Start Autoclicker", command=self.start_autoclicker)
        self.stop_button = tk.Button(self, text="Stop Autoclicker", command=self.stop_autoclicker, state=tk.DISABLED)
        self.cords_label = tk.Label(self, text="Click Coordinates:")
        self.cords_entry = tk.Entry(self, textvariable=self.cords)
        self.click_button = tk.Button(self, text="Click on Screen", command=self.select_cords)

        # Set initial theme
        self.set_theme(self.theme.get())

        self.cps_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.cps_entry.grid(row=0, column=1, padx=5, pady=5)
        self.clicks_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.clicks_entry.grid(row=1, column=1, padx=5, pady=5)
        self.start_button.grid(row=2, column=0, padx=5, pady=5, columnspan=2, sticky=tk.W+tk.E)
        self.stop_button.grid(row=3, column=0, padx=5, pady=5, columnspan=2, sticky=tk.W+tk.E)
        self.cords_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.cords_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
        self.click_button.grid(row=5, column=0, padx=5, pady=5, columnspan=2, sticky=tk.W+tk.E)

        # Button Styles
        self.button_style = {
            "bg": self.color_palettes[self.theme.get()]["button_bg"],
            "fg": self.color_palettes[self.theme.get()]["fg"],
            "font": font.Font(family="Arial", size=12),
            "relief": "raised"
        }

        # Binding Window Maximize event
        self.bind('<Configure>', self.window_resize_event)

        self.autoclicker_thread = None

    def set_theme(self, theme):
        self.configure(bg=self.color_palettes[theme]["bg"])
        self.cps_label.configure(bg=self.color_palettes[theme]["label_bg"], fg=self.color_palettes[theme]["fg"])
        self.clicks_label.configure(bg=self.color_palettes[theme]["label_bg"], fg=self.color_palettes[theme]["fg"])
        self.start_button.configure(bg=self.color_palettes[theme]["button_bg"], fg=self.color_palettes[theme]["fg"])
        self.stop_button.configure(bg=self.color_palettes[theme]["button_bg"], fg=self.color_palettes[theme]["fg"])
        self.cords_label.configure(bg=self.color_palettes[theme]["bg"], fg=self.color_palettes[theme]["fg"])
        self.cords_entry.configure(bg=self.color_palettes[theme]["bg"], fg=self.color_palettes[theme]["fg"])
        self.click_button.configure(bg=self.color_palettes[theme]["button_bg"], fg=self.color_palettes[theme]["fg"])

    def update_theme(self):
        self.set_theme(self.theme.get())

    def show_notification(self, message):
        self.toaster.show_toast("Autoclicker", message, duration=5)

    def start_autoclicker(self):
        self.Cps = float(self.cps_entry.get())
        self.num_clicks = int(self.clicks_entry.get())

        self.cps_entry.config(state=tk.DISABLED)
        self.clicks_entry.config(state=tk.DISABLED)
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        self.show_notification("Autoclicking will start in 5 seconds. Switch to the target window.")

        self.autoclicker_thread = Thread(target=self.autoclicker)
        self.autoclicker_thread.start()

    def stop_autoclicker(self):
        self.cps_entry.config(state=tk.NORMAL)
        self.clicks_entry.config(state=tk.NORMAL)
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

        self.show_notification("Autoclicker stopped by the user.")

        if self.autoclicker_thread and self.autoclicker_thread.is_alive():
            keyboard.press('q')
            self.autoclicker_thread.join()

    def autoclicker(self):
        self.show_notification("Autoclicking started.")
        time.sleep(5)

        for _ in range(self.num_clicks):
            if keyboard.is_pressed('q'):
                self.show_notification("Autoclicking stopped by the user.")
                break

            if self.middle_button_click_var.get():
                pyautogui.middleClick()
            elif self.middle_button_double_click_var.get():
                pyautogui.doubleClick()
            else:
                click_cords = self.cords_entry.get().split(",")
                if len(click_cords) == 2:
                    try:
                        x = int(click_cords[0].strip())
                        y = int(click_cords[1].strip())
                        pyautogui.click(x, y)
                    except ValueError:
                        self.show_notification("Invalid click coordinates.")
                else:
                    self.show_notification("Invalid click coordinates.")

            time.sleep(self.Cps)
        else:
            self.show_notification("Autoclicking completed.")

    def select_cords(self):
        self.hide_window()
        self.show_notification("Select click coordinates on the screen.")
        time.sleep(1)
        cords = pyautogui.position()
        self.cords.set(f"{cords.x}, {cords.y}")
        self.show_window()

    def hide_window(self):
        self.withdraw()

    def show_window(self):
        self.update()
        self.deiconify()

    def save_settings(self):
        settings = {
            "Cps": self.Cps.get(),
            "num_clicks": self.num_clicks.get(),
            "theme": self.theme.get(),
            "cords": self.cords.get(),
            "middle_button_click": self.middle_button_click_var.get(),
            "middle_button_double_click": self.middle_button_double_click_var.get()
        }

        filename = filedialog.asksaveasfilename(defaultextension=".json")
        if filename:
            try:
                with open(filename, "w") as file:
                    json.dump(settings, file)
                self.show_notification("Settings saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save settings: {str(e)}")

    def import_settings(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if filename:
            try:
                with open(filename, "r") as file:
                    settings = json.load(file)

                self.Cps.set(settings.get("Cps", 0))
                self.num_clicks.set(settings.get("num_clicks", 0))
                self.theme.set(settings.get("theme", "dark_blue"))
                self.cords.set(settings.get("cords", ""))
                self.middle_button_click_var.set(settings.get("middle_button_click", False))
                self.middle_button_double_click_var.set(settings.get("middle_button_double_click", False))

                self.set_theme(self.theme.get())

                self.show_notification("Settings imported successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import settings: {str(e)}")

    def export_settings(self):
        settings = {
            "Cps": self.Cps.get(),
            "num_clicks": self.num_clicks.get(),
            "theme": self.theme.get(),
            "cords": self.cords.get(),
            "middle_button_click": self.middle_button_click_var.get(),
            "middle_button_double_click": self.middle_button_double_click_var.get()
        }

        filename = filedialog.asksaveasfilename(defaultextension=".json")
        if filename:
            try:
                with open(filename, "w") as file:
                    json.dump(settings, file)
                self.show_notification("Settings exported successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export settings: {str(e)}")

    def window_resize_event(self, event):
        self.update()

    def on_resize(self, event):
        font_size = max(8, int(self.default_font_size * self.winfo_width() / self.default_width))
        self.custom_font.configure(size=font_size)
        self.configure_font()

    def button_hover_in(self, event):
        event.widget.configure(bg=self.color_palettes[self.theme.get()]["fg"],
                               fg=self.color_palettes[self.theme.get()]["button_bg"])

    def button_hover_out(self, event):
        event.widget.configure(bg=self.color_palettes[self.theme.get()]["button_bg"],
                               fg=self.color_palettes[self.theme.get()]["fg"])

    def button_click(self, event):
        event.widget.configure(relief="sunken")

    def button_release(self, event):
        event.widget.configure(relief="raised")


autoclicker_gui = AutoclickerGUI()
autoclicker_gui.mainloop()
