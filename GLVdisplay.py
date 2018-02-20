import Tkinter as tk

def init_display():
    win = tk.Tk()
    #app = FullScreenApp(win)
    display = tk.Text(win)
    display.pack(expand=True, fill='both')
    display.bbox
    win.update()

def update_display():
