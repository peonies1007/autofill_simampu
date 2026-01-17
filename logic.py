import datetime


def get_all_date(input_str):
    # input_str = "2026-01-08 16:00"

    # 2. Parsing string menjadi objek datetime
    dt_obj = datetime.strptime(input_str, "%Y-%m-%d %H:%M")

    # 3. Kamus untuk konversi ke Bahasa Indonesia
    # Python weekday(): 0=Senin, 1=Selasa, ..., 6=Minggu
    daftar_hari = {
        0: "Senin",
        1: "Selasa",
        2: "Rabu",
        3: "Kamis",
        4: "Jumat",
        5: "Sabtu",
        6: "Minggu",
    }

    daftar_bulan = {
        1: "Januari",
        2: "Februari",
        3: "Maret",
        4: "April",
        5: "Mei",
        6: "Juni",
        7: "Juli",
        8: "Agustus",
        9: "September",
        10: "Oktober",
        11: "November",
        12: "Desember",
    }

    # 4. Ekstrak parameter
    hari = daftar_hari[dt_obj.weekday()]
    tanggal = dt_obj.day
    bulan = daftar_bulan[dt_obj.month]
    tahun = dt_obj.year
    waktu = dt_obj.strftime("%H:%M")

    return hari, tanggal, bulan, tahun, waktu
