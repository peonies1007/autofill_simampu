import google.generativeai as genai  # type: ignore # noqa: F811
import json
import os

# Konfigurasi API Key
# Pastikan Anda sudah memiliki API Key
os.environ["GOOGLE_API_KEY"] = "AIzaSyChPEIsWYdbqxyFuacQ245ANVbBH4b63ws"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])


def extract_report_with_strict_schema(text_laporan):
    with open("scheme.json", "r") as file:
        # Use json.load() to convert the file content to a Python object (dictionary)
        data = json.load(file)

        # Skema JSON yang ketat
        report_schema = data

    # Menggunakan model gemini-1.5-flash
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        generation_config={
            "response_mime_type": "application/json",
            "response_schema": report_schema,
        },
    )

    prompt = f"""
    Anda adalah sistem pengolah data darurat yang bertugas mengekstrak semua informasi dari laporan bencana Angin Kencang ini.
    **Ikuti skema JSON yang telah ditetapkan secara ketat.**
    Pastikan semua nilai numerik (umur, kerugian) diubah ke tipe 'integer' murni.

    Teks Laporan:
    {text_laporan}
    """

    response = model.generate_content(prompt)

    # Mengembalikan hasil sebagai object Python (Dictionary)
    return json.loads(response.text)


# --- Data Input (Sesuai yang Anda berikan) ---
laporan_raw = """
1.      Hari Kejadian              : Jumat
2.      TanggalKejadian        : 05 Desember 2025
3.      Waktu Kejadian          : 14.30 WIB
4.      Waktu Laporan           : 16.24 WIB
5.      Waktu Respons           : 16.25 WIB
6.      Waktu Penanganan      : 16.55 WIB
7.      Waktu Terkondisi        : 18.30 WIB
 
A.   Jenis Kejadian             : Angin Kencang
B.    Pelapor                          : Mansur / Sukiman ( Bagana )
C.   Lokasi Kejadian             : Dk. Jumbleng Rt. 21, Ds. Slendro, Kec. Gesi, Kab. Sragen
D.   Identitas Pemilik Lahan / Rumah  : 
-         1.Nama.              : Satiyem
-         Jenis Kelamin        : Perempuan
-         Umur.                : 57 Tahun
-         Alamat.              : SDA
E.    Kronologi                          :
-          Pada Hari Jum'at Sekitar Pukul 15:00 WIB Di Wilayah Kec.Gesi , Kabupaten Sragen Di Guyur Hujan Intensitas Deras Dan Disertai Angin Kencang  Yang Mengakibatkan 1 Pohon Jati Tumbang Menimpa Rumah Huni
F.     Penyebab Kejadian          :  Angin Kencang 
G.   Pengungsi                       : NIHIL
H.   Kerusakan                         :
-         Pohon Jenis Jati Diameter ± 40 Cm Tumbang
-         Genteng ± 200 Buah Pecah
I.      Kerugian                           :  ± Rp. 1.500.000.00 (Satu Juta Lima Ratus Ribu Rupiah)
J.     Dampak Kejadian            : 
-          Membuat Penghuni Rumah Shok
-          Membuat Rumah Huni Rusak Ringan
 
K.   Upaya Penanganan Awal
-         Pusdalop BPBD Setelah Menerima Informasi dari Sdr.Mansur/Sukiman(Anggota Relawan Bagana) Kemudian Menginformasikan Kepada TRC BPBD Menuju Lokasi untuk Asessment dan Evakuasi 
-         Koordinasi dengan Relawan PB Kab. Sragen, Lintas Sektoral, dan pemangku wilayah setempat untuk penanganan bencana dampak Angin Kencang
-         Menghubungi jejaring Relawan PB Kab. Sragen yang dekat dengan lokasi untuk membantu penanganan 
 
L.    Kajian Kebutuhan Logistik
-         NIHIL
M.   Kendala / Hambatan
-         Terlambatnya Laporan Masuk Ke BPBD Kab.Sragen
-         Saat Penanganan Di Lokasi Masih Kondisi Hujan Ringan
-         Minimnya Penerangan Di Sekitar Lokasi
 
N.   Kesimpulan dan Rekomendasi
-         Kerja Bakti Akan Di Laksanakan Warga Setempat Besok Hari Sabtu / Tgl 06 Desember 2025
-         Assesment dan Penangan telah dilaksanakan
-         Menghimbau kepada masyarakat sekitar agar lebih waspada terhadap cuaca exstrim
-         Diharapkan warga lebih waspada dalam kesiapsiagaan dengan dampak bencana Hidrometeorologi seperti Banjir, Tanah Longsor & Angin Kencang
-         Berkoordinasi dengan dinas terkait agar memangkas ranting pohon yang berpotensi patah
 
O.   TRC BPBD Kab. Sragen 
1. Anang Dwi Nugroho (Asn BPBD Kab.Sragen)
2. Bambang S (Assesment)
3. Nanda Sulistyo Aji
 
P.    PUSDALOP BPBD Kab. Sragen
1.     Darmono
2.     Janu Saputro
"""

# --- Eksekusi ---
if __name__ == "__main__":
    try:
        # Panggil fungsi
        json_output = extract_report_with_strict_schema(laporan_raw)

        # Print hasil JSON dengan indentasi agar mudah dibaca
        print("✅ **OUTPUT JSON DENGAN STRUKTUR KETAT** ✅")
        print("---")
        print(json.dumps(json_output, indent=4, ensure_ascii=False))

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
