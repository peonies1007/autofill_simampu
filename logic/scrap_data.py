from google import genai
import json
import os
from dotenv import load_dotenv
from auto_fill_simampu.dump_data.data_kejadian_dump import (
    DATA_KEJADIAN_DUMP as target_schema,
)

load_dotenv()
# 2. Konfigurasi Client Gemini
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def get_disaster_object(laporan):
    extraction_rules = """
    ANDA ADALAH PARSER DATA BPBD YANG SANGAT KETAT. IKUTI ATURAN BERIKUT UNTUK MENGISI NILAI JSON:

    A. BAGIAN UMUM (tambah_kejadian)
    1. nama_kejadian: WAJIB format string: "[jenis_bencana] di Kabupaten Sragen Provinsi Jawa Tengah". Contoh: "Tanah Longsor di Kabupaten Sragen Provinsi Jawa Tengah".
    2. tanggal_waktu_kejadian_terjadi: Format datetime "YYYY-MM-DD HH:mm". Ambil waktu mulai kejadian.
    3. tanggal_waktu_kejadian_berakhir: Format datetime "YYYY-MM-DD HH:mm". Jika kejadian sudah selesai (surut/padam), isi waktunya. Jika belum, kosongkan "".
    4. jenis_bencana: Ambil jenis bencananya saja (contoh: Banjir, Bila Angin Kencang maka ganti dengan Cuaca Ekstrem, Kebakaran Hutan dan Lahan).
    5. kronologi: Ceritakan urutan kejadian secara lengkap berdasarkan teks.
    6. peringatan_dini: Jika ada info peringatan BMKG/EWS tuliskan. Jika tidak ada, TULIS "NIHIL".
    7. sebab_kejadian: Apa pemicu bencananya (contoh: Hujan intensitas tinggi, Konsleting listrik).
    8. deskripsi: Ringkasan singkat dampak dan kerusakan utama.
    9. sebaran_dampak (List):
       - sebaran_dampak_kec: Hanya nama Kecamatannya saja (contoh: "Sragen").
       - sebaran_dampak_ds_kel(List): Hanya nama Desa/Kelurahannya saja (contoh: ["Sragen Tengah", "Sragen Wetan"]).
       (Buat item baru dalam list jika kejadian di banyak lokasi).
    10. gambar: Biarkan kosong "".

    B. DETAIL & INFORMASI (tambah_informasi_terkini)
    - Ini adalah LIST. Hanya ada 2 data yaitu data saat Waktu Penanganan dan Waktu Terkondisi. 
    1. waktu_penanganan_terkondisi : Data yang pertama isi dengan Waktu Penanganan dan data yang kedua isi dengan Waktu Terkondisi
    2. sumber_informasi: Siapa yang melapor (Warga, TRC, Perangkat Desa) dan siapa yang melakukan assessment (biasanya TRC (Tim Respon Cepat)).
    3. kondisi_mutakhir_dropdown: Analisa dan pilih dari pilihan berikut: "Kondusif", "Masih dilakukan evakuasi", "Masih dalam pendataan", "Air sudah surut", "Air belum surut", "Air berangsur Surut". Apabila Waktu Terkondisi maka isi dengan "Kondusif"
    4. kondisi_mutakhir_deskripsi: Bila data Waktu Penanganan maka isi dengan *Dampak Kejadian* apabila Waktu Terkondisi isi dengan *Kesimpulan dan Rekomendasi* namun cari Kesimpulannya saja. Tidak usah diberi judul. buat menjadi seperti ini : 
        "- pertama
        - kedua"
    5. upaya_penanganan: Apa yang sudah dilakukan petugas di lapangan.
    6. kendala_lapangan: Hambatan akses/cuaca/alat. Jika tidak ada, TULIS "NIHIL".

    C. KORBAN JIWA (tambah_korban_jiwa)
    - Isi semua field angka (meninggal, luka, mengungsi, kk) dengan ANGKA saja (string format angka, contoh: "5").
    - Jika tidak ada korban, kosongkan "".
    - titik_pengungsian: Nama lokasi pengungsian jika ada.

    D. KERUSAKAN (tambah_kerusakan_dan_kerugian)
    - Ini adalah LIST. Buat 1 objek per lokasi (Kecamatan/Desa) yang terdampak.
    - Klasifikasikan kerusakan ke dalam kategori yang tepat (rumah/pendidikan/jalan/dll).
    - Apabila kerusakan merupakan pohon jangan masukkan ke kategori manapun namun hanya masukkan kerugiannya saja
    - rusak_..._ringan/sedang/berat: Isi dengan JUMLAH UNIT (angka).
    - Contoh: "2 rumah rusak berat" -> masukkan "2" ke field rusak_rumah_rusak_berat.
    
    E. DETAIL KERUSAKAN DAN KERUGIAN (tambah_detail_ker_krg)
    - Ini adalah LIST. Buat 1 objek per pemilik bangunan, lahan, atau pohon
    - nama_kerusakan : Isi dengan jenis kerusakan dapat berupa bangunan, lahan ataupun pohon
    - nama_pemilik : Isi dengan nama pemilik bangunan, pohon atau lahan yang rusak atau terdampak
    - kategori : Isi dengan sesuai kategori pada tambah_kerusakan_dan_kerugian, apabila kerusakannya pohon maka kosongi
    - kerusakan : Isi dengan Terdampak, Rusak Ringan, atau Rusak Berat
    - luasan_tedampak : isi bila memang ada di laporan (Biasanya kerusakan berupa lahan)
    - satuan_luasan : isi satuan dari luasan_terdampak
    - kerugian : Isi dengan kerugian
    - alamat : Isi dengan alamat terjadinya bencana tersebut
    - deskpripsi : Buat deskripsi sesuai dengan laporan
    
    F. ATURAN FORMAT
    - Format Tanggal: YYYY-MM-DD HH:mm
    - Field tombol (btn_...): Biarkan kosong "".
    - Data tidak tersedia: Biarkan string kosong "".
    - Bila tidak ada kategori kerusakan berat, sedang, atau ringan, kerusakan kurang dari 10000000 kategorikan menjadi rusak ringan, bila 10000000 - 20000000 kategorikan rusak sedang, bila lebih dari 20000000 kategorikan rusak berat.
    """

    # 3. Merakit Prompt
    prompt = f"""
    TUGAS: Ekstrak data laporan bencana berikut menjadi JSON sesuai aturan ketat di bawah ini.
    
    {extraction_rules}

    STRUKTUR JSON TARGET:
    {json.dumps(target_schema)}

    TEKS LAPORAN:
    "{laporan}"
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",  # Menggunakan model stabil terbaru
            contents=prompt,
            config={
                "response_mime_type": "application/json",
            },
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Error extracting data: {e}")
        return None


def scrap_data(laporan):
    # Eksekusi
    try:
        print("Sedang memproses data dengan Gemini AI...")
        result_data = get_disaster_object(laporan)

        if result_data:
            # ---------------------------------------------------------
            # CARA 1: MENYIMPAN KE FILE JSON
            # ---------------------------------------------------------
            nama_file_json = "hasil_insiden.json"

            with open(nama_file_json, "w", encoding="utf-8") as f:
                # ensure_ascii=False agar karakter Indonesia terbaca normal
                json.dump(result_data, f, indent=4, ensure_ascii=False)

            print(f"\n[SUKSES] Data berhasil disimpan ke file: {nama_file_json}")

            # ---------------------------------------------------------
            # CARA 2: MENGAKSES DATA DI PYTHON (READ BACK)
            # ---------------------------------------------------------
            print(
                "\n[INFO] Mencoba membaca kembali file untuk memastikan format Python benar..."
            )

            # Buka file yang baru saja dibuat
            with open(nama_file_json, "r", encoding="utf-8") as f:
                data_loaded = json.load(f)

        return True, data_loaded
        # isi_form_bpbd_sragen(kejadian)
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        return False, e
