from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from logic.select_date import select_date

kejadian_dump = {
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


def tambah_kejadian(driver, data_obj):
    print("🚀 Membuka halaman Tambah Kejadian...")
    wait = WebDriverWait(driver, 10)
    # 2. XPATH Map sesuai data yang Anda berikan
    xpath_map = {
        "nama_kejadian": '//*[@id="content-container"]/div[3]/div/div/div/div/div/div/div/div/div/form/div[1]/div[1]/div/div/input',
        "tanggal_waktu_kejadian_terjadi": '//*[@id="content-container"]/div[3]/div/div/div/div/div/div/div/div/div/form/div[2]/div[1]/div/div/div/div/input',
        "tanggal_waktu_kejadian_berakhir": '//*[@id="content-container"]/div[3]/div/div/div/div/div/div/div/div/div/form/div[2]/div[2]/div/div/div/div/input',
        "jenis_bencana": '//*[@id="content-container"]/div[3]/div/div/div/div/div/div/div/div/div/form/div[3]/div[1]/div[4]/div[1]/div/div/div/div/div/input',
        "kronologi": '//*[@id="content-container"]/div[3]/div/div/div/div/div/div/div/div/div/form/div[4]/div/div/div/div[1]',
        "peringatan_dini": '//*[@id="content-container"]/div[3]/div/div/div/div/div/div/div/div/div/form/div[6]/div/div/div/div[1]',
        "sebab_kejadian": '//*[@id="content-container"]/div[3]/div/div/div/div/div/div/div/div/div/form/div[8]/div/div/div/div[1]',
        "deskripsi": '//*[@id="content-container"]/div[3]/div/div/div/div/div/div/div/div/div/form/div[10]/div/div/div/div[1]',
        "sebaran_dampak_kec": '//*[@id="content-container"]/div[3]/div/div/div/div/div/div/div/div/div/form/div[12]/div[1]/div/div[1]/div[1]/div/input',
        "sebaran_dampak_ds_kel": '//*[@id="content-container"]/div[3]/div/div/div/div/div/div/div/div/div/form/div[12]/div[2]/div/div[1]/div[1]/div/input',
        "simpan_tambah_kejadian": "//*[@id='content-container']/div[3]/div/div/div/div/div/div/div/div/div/form/div[14]/button",
    }

    try:
        print(f"🔗 Terhubung ke: {driver.title}")
        print("⏳ Memulai pengisian dengan delay 0.5 detik...")
        # print(data_obj)
        # --- A. Mengisi Input Fields (Tipe Input Teks) ---
        all_fields = [
            "nama_kejadian",
            "tanggal_waktu_kejadian_terjadi",
            "tanggal_waktu_kejadian_berakhir",
            "jenis_bencana",
            "kronologi",
            "peringatan_dini",
            "sebab_kejadian",
            "deskripsi",
        ]

        # List untuk membedakan mana yang input biasa dan mana yang DIV
        div_type_fields = [
            "kronologi",
            "peringatan_dini",
            "sebab_kejadian",
            "deskripsi",
        ]

        tanggal_field = [
            "tanggal_waktu_kejadian_terjadi",
            "tanggal_waktu_kejadian_berakhir",
        ]

        sebaran_dampak_field = [
            "sebaran_dampak_kec",
            "sebaran_dampak_ds_kel",
        ]

        # 2. Gunakan JAVASCRIPT untuk memaksa masuknya nilai
        # Ini akan menimpa batasan 'readonly' dan menghindari munculnya kalender

        for key in all_fields:
            # SEMUA menggunakan EC.element_to_be_clickable
            element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_map[key])))

            if key in div_type_fields:
                # Input untuk elemen DIV (Rich Text)
                driver.execute_script(
                    "arguments[0].innerText = arguments[1];", element, data_obj[key]
                )
                print(f"✅ Berhasil isi DIV: {key}")
            elif key in tanggal_field:
                select_date(driver, data_obj[key], xpath_map[key])
            elif key == "jenis_bencana":
                element.clear()
                element.click()
                # print(data_obj[key])
                wait.until(
                    EC.visibility_of_element_located(
                        (By.XPATH, f"//span[text()='{data_obj[key]}']")
                    )
                ).click()
                time.sleep(0.5)
                wait.until(
                    EC.invisibility_of_element_located(
                        (By.CSS_SELECTOR, "sb-oveflow-hidden")
                    )
                )

            else:
                # Input untuk elemen <input> biasa
                element.clear()
                element.send_keys(data_obj[key])
                print(f"✅ Berhasil isi INPUT: {key}")

            # Delay 0.5 detik sesuai permintaan
            time.sleep(0.5)
        for arr_wilayah in data_obj["sebaran_dampak"]:
            for i, kec_desa in enumerate(arr_wilayah):
                wait.until(
                    EC.visibility_of_element_located(
                        (By.XPATH, xpath_map[sebaran_dampak_field[i]])
                    )
                ).click()
                print(arr_wilayah[kec_desa])
                if kec_desa == sebaran_dampak_field[0]:
                    wait.until(
                        EC.visibility_of_element_located(
                            (
                                By.XPATH,
                                f"//li[.//text()='{arr_wilayah[kec_desa]}']",
                            )
                        )
                    ).click()
                else:
                    for desa in arr_wilayah[kec_desa]:
                        wait.until(
                            EC.visibility_of_element_located(
                                (
                                    By.XPATH,
                                    f"//li[.//text()='{desa}']",
                                )
                            )
                        ).click()
            time.sleep(0.2)
        print("\n✨ Proses selesai! Semua kolom telah terisi.")
        wait.until(
            EC.element_to_be_clickable((By.XPATH, xpath_map["simpan_tambah_kejadian"]))
        ).click()
    except Exception as e:
        print(f"❌ Error: {e}")
