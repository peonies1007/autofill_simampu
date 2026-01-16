import threading
import tkinter as tk
import ttkbootstrap as tb
from tkinter import messagebox


def loading_components(target_func, *args):
    status_hasil = {}
    # 1. Buat Jendela
    loading_window = tb.Toplevel(title="Memproses Data")
    loading_window.geometry("300x150")

    # Letakkan di tengah layar agar tidak sembunyi
    loading_window.position_center()

    # PENTING: Pastikan jendela selalu di atas (Win 7 sering menumpuk jendela)
    loading_window.attributes("-topmost", True)
    loading_window.grab_set()

    lbl = tb.Label(
        loading_window, text="Mohon tunggu sebentar...", font=("Helvetica", 10)
    )
    lbl.pack(pady=20)

    progress = tb.Progressbar(
        loading_window, mode="indeterminate", bootstyle="primary", length=200
    )
    progress.pack(pady=10)
    progress.start(10)

    # --- KRITIKAL UNTUK WINDOWS 7 ---
    # Memaksa Windows menggambar jendela SEKARANG juga sebelum thread dimulai
    loading_window.update()

    def worker():
        try:
            # Jalankan fungsi
            is_success, data = target_func(*args)

            # Gunakan fungsi bantuan untuk eksekusi UI agar aman
            def selesai():
                if loading_window.winfo_exists():
                    loading_window.destroy()

                status_hasil.update({"is_success": is_success, "data": data})

            loading_window.after(0, selesai)
        except Exception as e:
            error_fatal = str(e)
            print(f"Error di Thread: {error_fatal}")  # Muncul di terminal untuk debug

            def error_handler():
                if loading_window.winfo_exists():
                    loading_window.destroy()
                messagebox.showerror("Error Fatal", f"Sistem Crash: {error_fatal}")

            status_hasil.update({"is_success": False, "data": e})
            loading_window.after(0, error_handler)

    # Jalankan thread
    t = threading.Thread(target=worker, daemon=True)
    t.start()
    # Fungsi akan BERHENTI di sini (tapi GUI tetap jalan) sampai window ditutup/destroy
    loading_window.wait_window()

    # Setelah window hancur, baru return nilai variabelnya
    return status_hasil["is_success"], status_hasil["data"]


def custom_askyesno(title, text):
    # Setup window
    window = tk.Toplevel()
    window.title(title)
    width_geo = 1200
    window.geometry(f"{width_geo}x700")

    result = {"value": None}

    def select(choice):
        result["value"] = choice
        window.destroy()

    # --- KONFIGURASI GRID UTAMA ---
    # Baris 0 (Area Teks) mengambil sisa ruang vertikal (weight=1)
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)

    # --- FRAME ATAS (Area Teks & Scrollbar) ---
    frame_top = tk.Frame(window, padx=10, pady=10)
    frame_top.grid(row=0, column=0, sticky="nsew")

    # --- FRAME BAWAH (Tombol) ---
    frame_bot = tk.Frame(window, padx=10, pady=20)
    frame_bot.grid(row=1, column=0, sticky="ew")

    # ============================================================
    # PERUBAHAN UTAMA: MENGGUNAKAN TEXT WIDGET + SCROLLBAR
    # ============================================================

    # 1. Buat Scrollbar
    scrollbar = tk.Scrollbar(frame_top)
    scrollbar.pack(side="right", fill="y")

    # 2. Buat Text Widget (Pengganti Label)
    # wrap="word" -> Agar pemenggalan baris rapi per kata, bukan per huruf
    text_area = tk.Text(
        frame_top,
        font=("Arial", 11),
        yscrollcommand=scrollbar.set,  # Hubungkan dengan scrollbar
        wrap="word",
        bd=0,  # Hilangkan border agar terlihat flat seperti label
        bg="#f0f0f0",  # (Opsional) Samakan warna dengan background window
        padx=10,
        pady=10,
    )

    # 3. Masukkan teks ke dalam widget
    text_area.insert("1.0", text)

    # 4. Kunci Text Widget agar Read-Only (Tidak bisa diedit user)
    text_area.config(state="disabled", cursor="arrow")

    # 5. Pasang Text Widget
    text_area.pack(side="left", fill="both", expand=True)

    # 6. Hubungkan balik scrollbar ke text widget
    scrollbar.config(command=text_area.yview)

    # ============================================================

    # Custom styled buttons
    tk.Button(
        frame_bot,
        text="YES",
        bg="green",
        fg="white",
        width=10,
        command=lambda: select(True),
    ).pack(side="left", padx=40, expand=True)

    tk.Button(
        frame_bot,
        text="NO",
        bg="red",
        fg="white",
        width=10,
        command=lambda: select(False),
    ).pack(side="right", padx=40, expand=True)

    window.grab_set()  # Modal behavior
    window.wait_window()
    return result["value"]
