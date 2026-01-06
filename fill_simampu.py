import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def script_input_tanggal(driver, element, tanggal):
    try:
        driver.execute_script(
            """
        var el = arguments[0];
        var val = arguments[1];
        
        // 1. Coba isi sebagai Input
        el.value = val;
        
        // 2. Coba isi sebagai DIV/SPAN (Rich Text)
        el.innerText = val;
        
        // 3. Paksa atribut value di HTML
        el.setAttribute('value', val);
        
        // 4. Trigger event agar website tahu ada perubahan data
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
        el.dispatchEvent(new Event('blur', { bubbles: true }));
    """,
            element,
            tanggal,
        )

    except Exception as e:
        print(e)


def isi_form_bpbd_sragen(data_obj):
    # 1. Koneksi ke browser yang sudah terbuka (Remote Debugging)
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )
    # 2. Buka URL Target (Ganti dengan URL formulir Anda)
    driver.get("https://simampu.bnpb.go.id/de/events_disaster_create")
    print("🚀 Membuka halaman formulir...")
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
    }

    try:
        print(f"🔗 Terhubung ke: {driver.title}")
        print("⏳ Memulai pengisian dengan delay 0.5 detik...")
        print(data_obj)
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
            "sebaran_dampak_kec",
            "sebaran_dampak_ds_kel",
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

        # 2. Gunakan JAVASCRIPT untuk memaksa masuknya nilai
        # Ini akan menimpa batasan 'readonly' dan menghindari munculnya kalender

        for key in all_fields:
            if key in data_obj:
                # SEMUA menggunakan EC.element_to_be_clickable
                element = wait.until(
                    EC.element_to_be_clickable((By.XPATH, xpath_map[key]))
                )

                if key in div_type_fields:
                    # Input untuk elemen DIV (Rich Text)
                    driver.execute_script(
                        "arguments[0].innerText = arguments[1];", element, data_obj[key]
                    )
                    print(f"✅ Berhasil isi DIV: {key}")
                elif key in tanggal_field:
                    script_input_tanggal(driver, element, data_obj[key])
                else:
                    # Input untuk elemen <input> biasa
                    element.clear()
                    element.send_keys(data_obj[key])
                    print(f"✅ Berhasil isi INPUT: {key}")

                # Delay 0.5 detik sesuai permintaan
                time.sleep(0.5)

        print("\n✨ Proses selesai! Semua kolom telah terisi.")

    except Exception as e:
        print(f"❌ Error: {e}")


# Contoh pemanggilan (Gunakan objek kejadian hasil ekstraksi AI Anda)
# isi_form_dengan_delay(kejadian)
