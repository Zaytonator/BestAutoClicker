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
            "icecream": {"bg": "#FF55BB", "label_bg": "#FFD3A3", "button_bg": "#FCFFB2", "fg": "#1D5D9B"},
            "midnight": {"bg": "#0C134F", "label_bg": "#1D267D", "button_bg": "#5C469C", "fg": "#D4ADFC"},
            "ocean": {"bg": "#F6F1F1", "label_bg": "#AFD3E2", "button_bg": "#19A7CE", "fg": "#146C94"},
            "End": {"bg": "#191825", "label_bg": "#865DFF", "button_bg": "#E384FF", "fg": "#FFA3FD"},
            "Nether": {"bg": "#F56EB3", "label_bg": "#CB1C8D", "button_bg": "#7F167F", "fg": "#460C68"},
            "Night Sky": {"bg": "#1D1CE5", "label_bg": "#4649FF", "button_bg": "#7978FF", "fg": "#C47AFF"},
            "Simplistic": {"bg": "#072227", "label_bg": "#35858B", "button_bg": "#4FBDBA", "fg": "#AEFEFF"},
            "Jungle": {"bg": "#164B60", "label_bg": "#1B6B93", "button_bg": "#4FC0D0", "fg": "#A2FF86"},
            "Icy": {"bg": "#BEDCFA", "label_bg": "#98ACF8", "button_bg": "#B088F9", "fg": "#DA9FF9"},
}

        # Variables
        self.Cps = tk.DoubleVar()
        self.num_clicks = tk.IntVar()
        self.theme = tk.StringVar()
        self.theme.set("dark_blue")
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
    
        self.file_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="Settings", menu=self.file_menu)


        self.click_menu = tk.Menu(self.menu, tearoff=False)
        self.click_menu.add_checkbutton(label="Middle Click", variable=self.middle_button_click_var)
        self.click_menu.add_checkbutton(label="Double Click", variable=self.middle_button_double_click_var)
        self.menu.add_cascade(label="Click Options", menu=self.click_menu)

        self.theme_menu = tk.Menu(self.menu, tearoff=False)
        self.theme_menu.add_radiobutton(label="Dark Blue", variable=self.theme, value="dark_blue", command=self.update_theme)
        self.theme_menu.add_radiobutton(label="Light Blue", variable=self.theme, value="light_blue", command=self.update_theme)
        self.theme_menu.add_radiobutton(label="Candy", variable=self.theme, value="candy", command=self.update_theme)
        self.theme_menu.add_radiobutton(label="Icecream", variable=self.theme, value="icecream", command=self.update_theme)
        self.theme_menu.add_radiobutton(label="Midnight", variable=self.theme, value="midnight", command=self.update_theme)
        self.theme_menu.add_radiobutton(label="Ocean", variable=self.theme, value="ocean", command=self.update_theme)
        self.theme_menu.add_radiobutton(label="End", variable=self.theme, value="End", command=self.update_theme)
        self.theme_menu.add_radiobutton(label="Nether", variable=self.theme, value="Nether", command=self.update_theme)
        self.theme_menu.add_radiobutton(label="Night Sky", variable=self.theme, value="Night Sky", command=self.update_theme)
        self.theme_menu.add_radiobutton(label="Simplistic", variable=self.theme, value="Simplistic", command=self.update_theme)
        self.theme_menu.add_radiobutton(label="Jungle", variable=self.theme, value="Jungle", command=self.update_theme)
        self.theme_menu.add_radiobutton(label="Icy", variable=self.theme, value="Icy", command=self.update_theme)

        self.menu.add_cascade(label="Themes", menu=self.theme_menu)

        self.config(menu=self.menu)

        # GUI Elements
        self.cps_label = tk.Label(self, text="Click Interval:")
        self.cps_entry = tk.Entry(self, textvariable=self.Cps)
        self.clicks_label = tk.Label(self, text="Click Amount:")
        self.clicks_entry = tk.Entry(self, textvariable=self.num_clicks)
        self.start_button = tk.Button(self, text="Start Autoclicker", command=self.start_autoclicker)
        self.stop_button = tk.Button(self, text="Stop Autoclicker", command=self.stop_autoclicker, state=tk.DISABLED)

        # Set initial theme
        self.set_theme(self.theme.get())

        self.cps_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.cps_entry.grid(row=0, column=1, padx=5, pady=5)
        self.clicks_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.clicks_entry.grid(row=1, column=1, padx=5, pady=5)
        self.start_button.grid(row=2, column=0, padx=5, pady=5, columnspan=2, sticky=tk.W+tk.E)
        self.stop_button.grid(row=3, column=0, padx=5, pady=5, columnspan=2, sticky=tk.W+tk.E)

        # Button Styles
        self.button_style = {
            "bg": self.color_palettes[self.theme.get()]["button_bg"],
            "fg": self.color_palettes[self.theme.get()]["fg"],
            "font": font.Font(family="Arial", size=12),
            "relief": "raised"

        
        }


        self.iconbitmap("Assets/Icon.ico")
    

        self.autoclicker_thread = None

    def set_theme(self, theme):
        self.configure(bg=self.color_palettes[theme]["bg"])
        self.cps_label.configure(bg=self.color_palettes[theme]["label_bg"], fg=self.color_palettes[theme]["fg"])
        self.clicks_label.configure(bg=self.color_palettes[theme]["label_bg"], fg=self.color_palettes[theme]["fg"])
        self.start_button.configure(bg=self.color_palettes[theme]["button_bg"], fg=self.color_palettes[theme]["fg"])
        self.stop_button.configure(bg=self.color_palettes[theme]["button_bg"], fg=self.color_palettes[theme]["fg"])
        self.clicks_entry.configure(bg=self.color_palettes[theme]["button_bg"], fg=self.color_palettes[theme]["fg"])
        self.cps_entry.configure(bg=self.color_palettes[theme]["button_bg"], fg=self.color_palettes[theme]["fg"])

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

        self.show_notification("Autoclicking will start in 5 seconds. Switch to the target window. (this may take a second to start, please be patient)")

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
        self.show_notification("Autoclicking started. (may take a second to start, please be patient)")
        time.sleep(5)

        for _ in range(self.num_clicks):
            if keyboard.is_pressed('q'):
                self.show_notification("Autoclicking stopped by the user.")
                break

            if self.middle_button_click_var.get():
                pyautogui.middleClick()
            elif self.middle_button_double_click_var.get():
                pyautogui.doubleClick()

            time.sleep(self.Cps)
        else:
            self.show_notification("Autoclicking completed.")

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
