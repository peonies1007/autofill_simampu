import tkinter as tk
from tkinter import messagebox

# from tkinter import ttk
from tkinter import scrolledtext

root = tk.Tk()
root.title("The Grid Geometry Manager")


def select_all_text(event):
    event.widget.tag_add("sel", "1.0", "end")
    return "break"


def show_info():
    print(laporan.get("1.0", "end-1c"))
    messagebox.showinfo("judul", laporan.get("1.0", "end-1c"))


tk.Label(
    root,
    text="Laporan:",
).grid(row=0, column=0, padx=5, pady=5)

laporan = scrolledtext.ScrolledText(root, width=50, height=30)
laporan.grid(row=1, column=0, padx=5, pady=5)


tk.Button(root, text="Submit", width=10, height=3, command=show_info).grid(
    row=2, column=0, pady=5
)

laporan.bind("<Control-a>", select_all_text)
laporan.bind("<Control-A>", select_all_text)
laporan.bind("<Command-a >", select_all_text)

root.mainloop()
