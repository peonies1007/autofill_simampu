from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.by import By
import sys
from logic.select_date import select_date

data_kejadian = [
    {
        "dampak_kecamatan": "Sragen",
        "dampak_ds_kelurahan": "Sragen Tengah",
        "dampak_tgl_waktu": "2026-01-08 17:15:00",
        "total_kk": "1",
        "terdampak_orang": "6",
        "meninggal_orang": "",
        "hilang_orang": "",
        "luka_ringan_orang": "",
        "luka_berat_orang": "",
        "mengungsi_orang": "",
        "titik_pengungsian": "",
    },
    {
        "dampak_kecamatan": "Karangmalang",
        "dampak_ds_kelurahan": "Puro",
        "dampak_tgl_waktu": "2026-01-08 17:15:00",
        "total_kk": "1",
        "terdampak_orang": "6",
        "meninggal_orang": "",
        "hilang_orang": "",
        "luka_ringan_orang": "",
        "luka_berat_orang": "",
        "mengungsi_orang": "",
        "titik_pengungsian": "",
    },
    {
        "dampak_kecamatan": "Karangmalang",
        "dampak_ds_kelurahan": "Saradan",
        "dampak_tgl_waktu": "2026-01-08 17:15:00",
        "total_kk": "1",
        "terdampak_orang": "6",
        "meninggal_orang": "",
        "hilang_orang": "",
        "luka_ringan_orang": "",
        "luka_berat_orang": "",
        "mengungsi_orang": "",
        "titik_pengungsian": "",
    },
]

xpathmap = {
    "btn_kelola_dampak_terkini": '//*[@id="content-container"]/div[3]/div/section[3]/div/div/div/div[1]/a/button',
    "tambah_korban_jiwa": {
        "btn_tambah_korban_jiwa": '//*[@id="content-container"]/div[3]/div[2]/div[1]/div/div/div[1]/button',
        "dampak_kecamatan": "/html/body/div[2]/div[2]/div/div/div/div/div[2]/div[1]/div/div/div/div/input",
        "dampak_ds_kelurahan": "/html/body/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div/div/div/div/input",
        "dampak_tgl_waktu": "/html/body/div[2]/div[2]/div/div/div/div/div[2]/div[3]/div/div/div/input",
        "total_kk": "/html/body/div[2]/div[2]/div/div/div/div/div[3]/form/div/div/div[1]/div/div/div[1]/input",
        "terdampak_orang": "/html/body/div[2]/div[2]/div/div/div/div/div[3]/form/div/div/div[2]/div/div/div[1]/input",
        "meninggal_orang": "/html/body/div[2]/div[2]/div/div/div/div/div[3]/form/div/div/div[3]/div/div/div[1]/input",
        "hilang_orang": "/html/body/div[2]/div[2]/div/div/div/div/div[3]/form/div/div/div[4]/div/div/div[1]/input",
        "luka_ringan_orang": "/html/body/div[2]/div[2]/div/div/div/div/div[3]/form/div/div/div[5]/div/div/div[1]/input",
        "luka_berat_orang": "/html/body/div[2]/div[2]/div/div/div/div/div[3]/form/div/div/div[6]/div/div/div[1]/input",
        "mengungsi_orang": "/html/body/div[2]/div[2]/div/div/div/div/div[3]/form/div/div/div[7]/div/div/div[1]/input",
        "titik_pengungsian": "/html/body/div[2]/div[2]/div/div/div/div/div[3]/form/div/div/div[8]/div/div/div[1]/input",
        "btn_simpan_korban_jiwa": "/html/body/div[2]/div[2]/div/div/div/div/div[3]/form/button",
        "btn_close": "/html/body/div[2]/div[2]/div/button",
    },
}

xpath_kj = xpathmap["tambah_korban_jiwa"]


def tambah_korban(driver, data_obj):
    print("🚀 Membuka halaman data kejadian...")
    wait = WebDriverWait(driver, 10)

    all_field = [
        "dampak_kecamatan",
        "dampak_ds_kelurahan",
        "dampak_tgl_waktu",
        "total_kk",
        "terdampak_orang",
        "meninggal_orang",
        "hilang_orang",
        "luka_ringan_orang",
        "luka_berat_orang",
        "mengungsi_orang",
        "titik_pengungsian",
    ]

    field_sebaran_dampak = [
        "dampak_kecamatan",
        "dampak_ds_kelurahan",
    ]
    try:
        for value_korban in data_obj:
            btn_tambah_korban_jiwa = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, xpath_kj["btn_tambah_korban_jiwa"])
                )
            )
            btn_tambah_korban_jiwa.click()
            time.sleep(0.5)
            for key in all_field:
                element = wait.until(
                    EC.visibility_of_element_located((By.XPATH, xpath_kj[key]))
                )
                time.sleep(0.2)
                if key in field_sebaran_dampak:
                    element.click()
                    wait.until(
                        EC.visibility_of_element_located(
                            (
                                By.XPATH,
                                f"//div/span[text()='{value_korban[key]}']",
                            )
                        )
                    ).click()

                elif key == "dampak_tgl_waktu":
                    select_date(driver, value_korban[key], xpath_kj[key])
                elif value_korban[key]:
                    element.click()
                    element.send_keys(value_korban[key])
            sys.exit(0)
            wait.until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        xpath_kj["btn_close"],
                    )
                )
            ).click()
    except Exception as e:
        print("Error", e)
