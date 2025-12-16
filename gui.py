import tkinter as tk
from tkinter import messagebox
from gemini_process import extract_laporan

# from tkinter import ttk
from tkinter import scrolledtext

root = tk.Tk()
root.title("The Grid Geometry Manager")


def select_all_text(event):
    event.widget.tag_add("sel", "1.0", "end")
    return "break"


def show_info():
    result_extract_laporan = extract_laporan(laporan_textbox.get("1.0", "end-1c"))
    messagebox.showinfo("judul", result_extract_laporan)


tk.Label(
    root,
    text="Laporan:",
).grid(row=0, column=0, padx=5, pady=5)

laporan_textbox = scrolledtext.ScrolledText(root, width=50, height=30)
laporan_textbox.grid(row=1, column=0, padx=5, pady=5)


tk.Button(root, text="Submit", width=10, height=3, command=show_info).grid(
    row=2, column=0, pady=5
)

laporan_textbox.bind("<Control-a>", select_all_text)
laporan_textbox.bind("<Control-A>", select_all_text)
laporan_textbox.bind("<Command-a >", select_all_text)

root.mainloop()
