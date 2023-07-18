import tkinter as tk
import pyautogui
import time
import keyboard
from threading import Thread
from win10toast import ToastNotifier

class AutoclickerGUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Autoclicker")
        self.toaster = ToastNotifier()
    
        self.cps_label = tk.Label(self, text="Click Interval (Pause):")
        self.cps_entry = tk.Entry(self)
        self.clicks_label = tk.Label(self, text="Number of Clicks:")
        self.clicks_entry = tk.Entry(self)
        self.start_button = tk.Button(self, text="Start Autoclicker", command=self.start_autoclicker)
        self.stop_button = tk.Button(self, text="Stop Autoclicker", command=self.stop_autoclicker, state=tk.DISABLED)
        #color for gui
        self.configure(bg='#003060')
        self.cps_label.configure(bg='#0E86D4')
        self.clicks_label.configure(bg='#0E86D4')
        self.start_button.configure(bg='#0E86D4')
        self.stop_button.configure(bg='#0E86D4')




        self.cps_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.cps_entry.grid(row=0, column=1, padx=5, pady=5)
        self.clicks_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.clicks_entry.grid(row=1, column=1, padx=5, pady=5)
        self.start_button.grid(row=2, column=0, padx=5, pady=5, columnspan=2, sticky=tk.W+tk.E)
        self.stop_button.grid(row=3, column=0, padx=5, pady=5, columnspan=2, sticky=tk.W+tk.E)

        self.Cps = 0
        self.num_clicks = 0
        self.autoclicker_thread = None
    
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
            pyautogui.click()
            time.sleep(self.Cps)
        else:
            self.show_notification("Autoclicking completed.")


autoclicker_gui = AutoclickerGUI()


autoclicker_gui.mainloop()
