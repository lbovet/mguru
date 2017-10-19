import Tkinter as tk
import time
root = tk.Tk()

while(True):
    time.sleep(0.1)
    print root.winfo_pointerxy()
