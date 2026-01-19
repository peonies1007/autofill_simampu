import tkinter as tk
from tkinter import messagebox
from logic.scrap_data import scrap_data
from components import loading_components, custom_askyesno
from confirm_text import confirm_text
from dump_data.laporan_teks_dump import LAPORAN_TEKS
from fill_website.fill_simampu import isi_form_bpbd_sragen
from dump_data.dump_data_kejadian import DUMP_DATA

# from tkinter import ttk
from tkinter import scrolledtext

root = tk.Tk()
root.title("The Grid Geometry Manager")

root.option_add("*Dialog.msg.font", "Helvetica 11")


def select_all_text(event):
    event.widget.tag_add("sel", "1.0", "end")
    return "break"


def show_info():
    laporan_teks = laporan.get("1.0", "end-1c")
    is_success_fill, msg = loading_components(isi_form_bpbd_sragen, DUMP_DATA)
    if is_success_fill:
        messagebox.showinfo("Sukses", msg)
    else:
        messagebox.showerror("Error", f"Terjadi error saat mengisi Simampu: {msg}")

    # is_success, data = loading_components(scrap_data, laporan_teks)
    # text_confirm = confirm_text(data)

    # if is_success:
    #     confirm = custom_askyesno("Konfirmasi Laporan", f"Sukses: {text_confirm}")
    #     if confirm:
    #         is_success_fill, msg = loading_components(isi_form_bpbd_sragen, data)
    #         if is_success_fill:
    #             messagebox.showinfo("Sukses", msg)
    #         else:
    #             messagebox.showerror(
    #                 "Error", f"Terjadi error saat mengisis Simampu: {msg}"
    #             )
    #     else:
    #         pass
    # else:
    #     messagebox.showerror("Error", f"Terjadi error: {data}")


tk.Label(
    root,
    text="Laporan:",
).grid(row=0, column=0, padx=5, pady=5)

laporan = scrolledtext.ScrolledText(root, width=50, height=30)
laporan.grid(row=1, column=0, padx=5, pady=5)
laporan.insert(tk.INSERT, LAPORAN_TEKS)

tk.Button(root, text="Submit", width=10, height=3, command=show_info).grid(
    row=2, column=0, pady=5
)

laporan.bind("<Control-a>", select_all_text)
laporan.bind("<Control-A>", select_all_text)
laporan.bind("<Command-a >", select_all_text)

root.mainloop()
