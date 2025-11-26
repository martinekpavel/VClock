from tkinter import *
from tkinter.ttk import *
from time import strftime
import json

root = Tk()
root.title('Clock')
root.attributes('-topmost', True)  
root.overrideredirect(True)  

def start_move(event):
    global x, y
    x = event.x
    y = event.y

def do_move(event):
    delta_x = event.x_root - root.winfo_rootx() - x
    delta_y = event.y_root - root.winfo_rooty() - y
    new_x = root.winfo_x() + delta_x
    new_y = root.winfo_y() + delta_y
    root.geometry(f"+{new_x}+{new_y}")

def time():
    string = strftime('%H:%M:%S')
    lbl_time.config(text=string)
    lbl_time.after(1000, time)

def countdown():
    global remaining_time
    if remaining_time > 0:
        minutes, seconds = divmod(remaining_time, 60)
        lbl_countdown.config(text=f"{minutes:02}:{seconds:02}")
        remaining_time -= 1
        if remaining_time <= 9 * 60:
            lbl_countdown.config(background=settings['countdown_bg_color_critical'], foreground=settings['countdown_fg_color_critical'])
        elif remaining_time <= 30 * 60:
            lbl_countdown.config(background=settings['countdown_bg_color_warning'], foreground=settings['countdown_fg_color_warning'])
    else:
        remaining_time = 1785 # seconds
    lbl_countdown.after(1000, countdown)

def reset_countdown(event):
    global remaining_time
    remaining_time = 1785

def open_settings(event):
    settings_window = Toplevel(root)
    settings_window.title("Settings")

    Label(settings_window, text="Font:").grid(row=0, column=0, padx=10, pady=10)
    font_entry = Entry(settings_window)
    font_entry.grid(row=0, column=1, padx=10, pady=10)
    font_entry.insert(0, settings['font'])

    Label(settings_window, text="Font Size:").grid(row=1, column=0, padx=10, pady=10)
    font_size_entry = Entry(settings_window)
    font_size_entry.grid(row=1, column=1, padx=10, pady=10)
    font_size_entry.insert(0, settings['font_size'])

    Label(settings_window, text="Font Color:").grid(row=2, column=0, padx=10, pady=10)
    fg_color_entry = Entry(settings_window)
    fg_color_entry.grid(row=2, column=1, padx=10, pady=10)
    fg_color_entry.insert(0, settings['fg_color'])

    Label(settings_window, text="BG Color:").grid(row=3, column=0, padx=10, pady=10)
    bg_color_entry = Entry(settings_window)
    bg_color_entry.grid(row=3, column=1, padx=10, pady=10)
    bg_color_entry.insert(0, settings['bg_color'])

    Label(settings_window, text="Font Color (first):").grid(row=4, column=0, padx=10, pady=10)
    countdown_fg_warning_entry = Entry(settings_window)
    countdown_fg_warning_entry.grid(row=4, column=1, padx=10, pady=10)
    countdown_fg_warning_entry.insert(0, settings['countdown_fg_color_warning'])

    Label(settings_window, text="BG Color (first):").grid(row=5, column=0, padx=10, pady=10)
    countdown_bg_warning_entry = Entry(settings_window)
    countdown_bg_warning_entry.grid(row=5, column=1, padx=10, pady=10)
    countdown_bg_warning_entry.insert(0, settings['countdown_bg_color_warning'])

    Label(settings_window, text="Font Color (second):").grid(row=6, column=0, padx=10, pady=10)
    countdown_fg_critical_entry = Entry(settings_window)
    countdown_fg_critical_entry.grid(row=6, column=1, padx=10, pady=10)
    countdown_fg_critical_entry.insert(0, settings['countdown_fg_color_critical'])

    Label(settings_window, text="BG Color (second):").grid(row=7, column=0, padx=10, pady=10)
    countdown_bg_critical_entry = Entry(settings_window)
    countdown_bg_critical_entry.grid(row=7, column=1, padx=10, pady=10)
    countdown_bg_critical_entry.insert(0, settings['countdown_bg_color_critical'])

    def save_settings():
        settings['font'] = font_entry.get()
        settings['font_size'] = int(font_size_entry.get())
        settings['fg_color'] = fg_color_entry.get()
        settings['bg_color'] = bg_color_entry.get()
        settings['countdown_fg_color_warning'] = countdown_fg_warning_entry.get()
        settings['countdown_bg_color_warning'] = countdown_bg_warning_entry.get()
        settings['countdown_fg_color_critical'] = countdown_fg_critical_entry.get()
        settings['countdown_bg_color_critical'] = countdown_bg_critical_entry.get()
        with open('conf.json', 'w') as conf_file:
            json.dump(settings, conf_file)
        apply_settings()

    Button(settings_window, text="Save", command=save_settings).grid(row=8, column=0, columnspan=2, padx=10, pady=10)

def apply_settings():
    lbl_time.config(font=(settings['font'], settings['font_size']), foreground=settings['fg_color'], background=settings['bg_color'])
    lbl_countdown.config(font=(settings['font'], settings['font_size']), foreground=settings['countdown_fg_color_warning'], background=settings['countdown_bg_color_warning'])

def load_settings():
    try:
        with open('conf.json', 'r') as conf_file:
            return json.load(conf_file)
    except FileNotFoundError:
        return {
            'font': 'calibri',
            'font_size': 12,
            'fg_color': 'white',
            'bg_color': 'purple',
            'countdown_fg_color_warning': 'black',
            'countdown_bg_color_warning': 'yellow',
            'countdown_fg_color_critical': 'white',
            'countdown_bg_color_critical': 'black'
        }

def exit_application(event):
    root.destroy()
settings = load_settings()

lbl_time = Label(root, font=(settings['font'], settings['font_size']),
                 background=settings['bg_color'],
                 foreground=settings['fg_color'])
lbl_time.pack(anchor='center')

lbl_countdown = Label(root, font=(settings['font'], settings['font_size']),
                      background=settings['countdown_bg_color_warning'],
                      foreground=settings['countdown_fg_color_warning'])
lbl_countdown.pack(anchor='center')

remaining_time = 1785 
countdown()

root.bind("<Button-1>", start_move)
root.bind("<B1-Motion>", do_move)

lbl_countdown.bind("<Button-1>", reset_countdown)

root.bind("<Button-3>", open_settings)
root.bind("<Button-2>", exit_application)

apply_settings()
time()
mainloop()
