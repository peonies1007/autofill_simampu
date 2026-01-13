from select_date import select_date
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.by import By
import sys
from select_date import select_date
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from xpath_krs_krg import xpathmap
from data_krs_krg import data_krs_krg

from selenium.webdriver.common.keys import Keys

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=chrome_options
)


def tambah_krs_krg(driver, data_obj):
    print("🚀 Membuka halaman data kejadian...")
    wait = WebDriverWait(driver, 10)

    # "btn_tambah_kerusakan_kerugian",
    # "btn_simpan_dampak_terkini"
    form_header = [
        "kerusakan_kerugian_kecamatan",
        "kerusakan_kerugian_ds_kelurahan",
        "kerusakan_kerugian_tgl_waktu",
        "kerugian_total",
    ]

    kategori = [
        "rumah",
        "rumah_ibadah",
        "fasilitas_pendidikan",
        "fasilitas_umum",
        "jalan_km",
        "jembatan",
        "lahan_persawahan_ha",
        "lahan_perkebunan_ha",
        "hewan_ternak",
    ]

    field_kategori = {
        "rumah": [
            "rusak_rumah_rusak_ringan",
            "rusak_rumah_rusak_sedang",
            "rusak_rumah_rusak_berat",
            "rusak_rumah_rusak_terendam",
            "rugi_rumah",
        ],
        "rumah_ibadah": [
            "rusak_ibadah_rusak_ringan",
            "rusak_ibadah_rusak_sedang",
            "rusak_ibadah_rusak_berat",
            "rusak_ibadah_rusak_terendam",
            "rugi_ibadah",
        ],
        "fasilitas_pendidikan": [
            "rusak_pendidikan_rusak_ringan",
            "rusak_pendidikan_rusak_sedang",
            "rusak_pendidikan_rusak_berat",
            "rusak_pendidikan_rusak_terendam",
            "rugi_pendidikan",
        ],
        "fasilitas_umum": [
            "rusak_umum_rusak_ringan",
            "rusak_umum_rusak_sedang",
            "rusak_umum_rusak_berat",
            "rusak_umum_rusak_terendam",
            "rugi_umum",
        ],
        "jalan_km": [
            "rusak_jalan_rusak_ringan",
            "rusak_jalan_rusak_sedang",
            "rusak_jalan_rusak_berat",
            "rusak_jalan_rusak_terendam",
            "rugi_jalan",
        ],
        "jembatan": [
            "rusak_jembatan_rusak_ringan",
            "rusak_jembatan_rusak_sedang",
            "rusak_jembatan_rusak_berat",
            "rusak_jembatan_rusak_terendam",
            "rugi_jembatan",
        ],
        "lahan_persawahan_ha": [
            "rusak_sawah_rusak_ringan",
            "rusak_sawah_rusak_sedang",
            "rusak_sawah_rusak_berat",
            "rusak_sawah_rusak_terendam",
            "rugi_sawah",
        ],
        "lahan_perkebunan_ha": [
            "rusak_kebun_rusak_ringan",
            "rusak_kebun_rusak_sedang",
            "rusak_kebun_rusak_berat",
            "rusak_kebun_rusak_terendam",
            "rugi_kebun",
        ],
        "hewan_ternak": ["total_hewan", "rugi_hewan"],
    }
    for value_data_krs_krg in data_krs_krg:
        btn_tambah = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, xpathmap["btn_tambah_kerusakan_kerugian"])
            )
        )
        btn_tambah.click()
        time.sleep(0.5)
        for key in form_header:
            element = wait.until(
                EC.visibility_of_element_located((By.XPATH, xpathmap[key]))
            )
            element.click()
            time.sleep(0.2)
            if key == "kerusakan_kerugian_tgl_waktu":
                select_date(driver, value_data_krs_krg[key], xpathmap[key])
            elif key == "kerugian_total":
                element.send_keys(value_data_krs_krg[key])
            else:
                element.click()
                wait.until(
                    EC.visibility_of_element_located(
                        (
                            By.XPATH,
                            f"//div/span[text()='{value_data_krs_krg[key]}']",
                        )
                    )
                ).click()
                time.sleep(0.2)

        for key_kategori in kategori:
            for val_key_kategori in field_kategori[key_kategori]:
                if value_data_krs_krg["kategori"][key_kategori][val_key_kategori]:
                    element = wait.until(
                        EC.visibility_of_element_located(
                            (
                                By.XPATH,
                                xpathmap["kategori"][key_kategori][val_key_kategori],
                            )
                        )
                    )
                    element.send_keys(Keys.CONTROL, "a")  # Select all text
                    element.send_keys(Keys.DELETE)
                    time.sleep(0.2)
                    element.send_keys(
                        value_data_krs_krg["kategori"][key_kategori][val_key_kategori]
                    )
                    time.sleep(0.2)
        btn_simpan = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, xpathmap["btn_simpan_dampak_terkini"])
            )
        )

        wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "/html/body/div[2]/div[2]/div/button")
            )
        ).click()

        # btn_simpan.click()


tambah_krs_krg(driver, data_krs_krg)
