import tkinter as tk
from ttkthemes import ThemedTk

# Create the themed application window
root = ThemedTk(theme="arc")  # Choose the theme you prefer ("radiance", "arc", "scidgrey", etc.)
root.title("Custom Title Bar Color")
root.geometry("400x300")

# Set the title bar color to blue (you can use any valid color)
root.set_theme("arc", {"titlebar": "blue"})

# Set the taskbar icon (replace 'icon.ico' with the path to your icon file)
root.iconbitmap("Assets/Icon.ico")

# Set the taskbar icon (replace 'icon.ico' with the path to your icon file)
root.wm_iconbitmap("Assets/Icon.ico")

# Run the Tkinter event loop
root.mainloop()
