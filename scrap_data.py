from dataclasses import dataclass
from google import genai
import json
import os
from dotenv import load_dotenv
from fill_simampu import isi_form_bpbd_sragen


# 1. Definisi Struktur Object menggunakan Dataclass
@dataclass
class LaporanBencana:
    nama_kejadian: str
    tanggal_waktu_kejadian_terjadi: str
    tanggal_waktu_kejadian_berakhir: str
    jenis_bencana: str
    kronologi: str
    peringatan_dini: str
    sebab_kejadian: str
    deskripsi: str
    sebaran_dampak_kec: str
    sebaran_dampak_ds_kel: str


load_dotenv()
# 2. Konfigurasi Client Gemini
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

laporan_teks = """
PEMERINTAH KABUPATEN SRAGEN
BADAN PENANGGULANGAN BENCANA DAERAH ( BPBD )
Jl.Veretan No.23 Sragen Telp.(0271)891433 -57211 E-mail : Bpbdsragen@gmail.com
LAPORAN TRC SATGAS PB BPBD KABUPATEN SRAGEN
HARI : Rabu TANGGAL : 18 Juni 2025 JAM : 10.30 WIB
Hari Kejadian : Selasa
Tanggal Kejadian : 17 Juni 2025
Waktu Kejadian : 18.30 WIB
Waktu Laporan : 21.21 WIB
Waktu Respons : 08.00 WIB ( 18 Juni 2025 )
Waktu Penanganan : 08.45 WIB ( 18 Juni 2025 )
Waktu Terkondisi : 09.20 WIB
Jenis Kejadian : Angin Kencang
Pelapor : Bapak Kresna ( Kepala Desa Sambi )
Lokasi Kejadian : Dk. Sambi RT. 19, Ds. Sambi, Kec. Sambirejo, Kab. Sragen
Kronologi : Sekitar pukul 18.30 wib di wilayah Kec. Sambirejo diguyur Hujan dengan Intensitas Sedang sampai Tinggi disertai Angin kencang yang mengakibatkan Sebuah Pohon Mahoni Roboh mengganggu pengguna jalan
Penyebab Kejadian : Hujan intensitas sedang sampai tinggi disertai Angin Kencang
Pengungsi : NIHIL
Kerusakan : 1 Pohon jenis Mahoni Roboh berdiameter 40 cm
Kerugian : ± Rp. 1.000.000,00
Dampak Kejadian : Membuat Akses Jalan tersendat
Upaya Penanganan Awal : Pusdalop BPBD begitu Menerima informasi dari Perangkat Desa Sambi segera menginformasikan kepada TRC BPBD menuju Lokasi untuk Asessment dan Evakuasi
"""


def get_disaster_object(text: str) -> LaporanBencana:
    prompt = f"""
    Ekstrak informasi dari laporan bencana berikut ke dalam format JSON dengan kunci:
    - nama_kejadian: isi dengan format sebagai berikut: "jenis_bencana" di Kabupaten Sragen Provinsi Jawa Tengah
    - tanggal_waktu_kejadian_terjadi: Tanggal dan waktu mulai (format: YYYY-MM-DD HH:mm)
    - tanggal_waktu_kejadian_berakhir: Tanggal dan waktu terkondisi/selesai (format: YYYY-MM-DD HH:mm)
    - jenis_bencana: Jenis bencana
    - kronologi: Urutan kejadian
    - peringatan_dini: Informasi peringatan dini jika ada, jika tidak tulis 'NIHIL'
    - sebab_kejadian: Penyebab bencana
    - deskripsi: Ringkasan kerusakan dan dampak
    - sebaran_dampak_kec: Nama Kecamatan
    - sebaran_dampak_ds_kel: Nama Desa atau Kelurahan
    Laporan: {text}
    """

    # Meminta Gemini memberikan output JSON yang valid
    response = client.models.generate_content(
        model="gemini-2.5-flash",  # Menggunakan model stabil terbaru
        contents=prompt,
        config={
            "response_mime_type": "application/json",
        },
    )

    # Parsing JSON mentah dari Gemini
    data_dict = json.loads(response.text)

    # 3. Inisialisasi dan Mengembalikan sebagai Python Object
    return LaporanBencana(**data_dict)


# Eksekusi
try:
    # Objek sekarang tersimpan di variabel 'kejadian'
    # kejadian = get_disaster_object(laporan_teks)

    # Contoh akses data layaknya sebuah Object
    # print("--- DATA OBJEK BERHASIL DISIMPAN ---")
    # print(f"Nama Kejadian : {kejadian.nama_kejadian}")
    # print(
    #     f"Lokasi        : Kec. {kejadian.sebaran_dampak_kec}, Desa {kejadian.sebaran_dampak_ds_kel}"
    # )
    # print(f"Waktu Mulai   : {kejadian.tanggal_waktu_kejadian_terjadi}")
    # print(f"Waktu Selesai : {kejadian.tanggal_waktu_kejadian_berakhir}")
    # print(f"Sebab         : {kejadian.sebab_kejadian}")
    # print(kejadian)
    kejadian = {
        "nama_kejadian": "Cuaca Ekstrem di Kabupaten Sragen Provinsi Jawa Tengah",
        "tanggal_waktu_kejadian_terjadi": "2026-01-08 17:15:00",
        "tanggal_waktu_kejadian_berakhir": "2026-01-08 18:00:00",
        "jenis_bencana": "Cuaca Ekstrem",
        "kronologi": "Pada Hari Kamis, 8 Januari 2026 Sekitar pukul ± 16.00 WIB wilayah Kab.Sragen Dan Sekitarnya di guyur Hujan intensitas Sedang Hingga Deras disertai angin Kencang yang Mengakibatkan  Pohon Tumbang Menutup Akses Jalan Kampung",
        "peringatan_dini": "NIHIL",
        "sebab_kejadian": "Hujan Disertai Angin Kencang",
        "deskripsi": "1 Pohon jenis Jati Roboh berdiameter 20 cm. Menghalangi jalan kampung.",
        "sebaran_dampak": [
            {
                "sebaran_dampak_kec": "Ngrampal",
                "sebaran_dampak_ds_kel": ["Bandung"],
            },
            {
                "sebaran_dampak_kec": "Sragen",
                "sebaran_dampak_ds_kel": ["Sragen Tengah", "Sragen Wetan"],
            },
        ],
    }
    isi_form_bpbd_sragen(kejadian)
except Exception as e:
    print(f"Terjadi kesalahan: {e}")
