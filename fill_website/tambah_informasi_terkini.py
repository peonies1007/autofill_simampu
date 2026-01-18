from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.by import By
from logic.select_date import select_date

kejadian_obj = {
    "waktu_penanganan_terkondisi": "2026-01-08 17:42:00",
    "sumber_informasi": "Tim Respon Cepat",
    "kondisi_mutakhir_dropdown": "Kondusif",
    "kondisi_mutakhir_deskripsi": "Pohon sudah dievakuasi",
    "upaya_penanganan": "Tim Respon Cepat datang ke lokasi untuk melakukan evakuasi pohon tumbang",
    "kebutuhan_mendesak": "Nihil",
    "kendala_lapangan": "Nihil",
    "informasi_tambahan": "Nihil",
}


def tambah_informasi_terkini(driver, kejadian):
    # driver.get("https://simampu.bnpb.go.id/de/events_disaster/3314104202601082/show")
    print("🚀 Membuka halaman data kejadian...")
    wait = WebDriverWait(driver, 20)

    xpathmap = {
        "btn_tambah_informasi_terkini": '//*[@id="content-container"]/div[3]/div/section[1]/div/div/div/div[1]/button',
        "waktu_penanganan_terkondisi": "/html/body/div[2]/div[2]/div/div/div/form/div[1]/div/div/div/input",
        "sumber_informasi": "/html/body/div[2]/div[2]/div/div/div/form/div[3]/div/div/input",
        "kondisi_mutakhir_dropdown": "/html/body/div[2]/div[2]/div/div/div/form/div[5]/div/div/div/div/input",
        "kondisi_mutakhir_deskripsi": "/html/body/div[2]/div[2]/div/div/div/form/div[7]/div/div/div/div[1]",
        "upaya_penanganan": "/html/body/div[2]/div[2]/div/div/div/form/div[9]/div/div/div/div[1]",
        "kebutuhan_mendesak": "/html/body/div[2]/div[2]/div/div/div/form/div[11]/div/div/div/div[1]",
        "kendala_lapangan": "/html/body/div[2]/div[2]/div/div/div/form/div[13]/div/div/div/div[1]",
        "informasi_tambahan": "/html/body/div[2]/div[2]/div/div/div/form/div[15]/div/div/div/div[1]",
        "btn_simpan": "/html/body/div[2]/div[2]/div/div/div/form/button",
    }
    all_fields = [
        "waktu_penanganan_terkondisi",
        "sumber_informasi",
        "kondisi_mutakhir_dropdown",
        "kondisi_mutakhir_deskripsi",
        "upaya_penanganan",
        "kebutuhan_mendesak",
        "kendala_lapangan",
        "informasi_tambahan",
    ]

    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[text()='Detil Kejadian Bencana']")
        )
    )
    try:
        wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, xpathmap["btn_tambah_informasi_terkini"])
            )
        ).click()

        for key in all_fields:
            element = wait.until(
                EC.visibility_of_element_located((By.XPATH, xpathmap[key]))
            )
            if key == "waktu_penanganan_terkondisi":
                select_date(driver, kejadian[key], xpathmap[key])

            elif key == "sumber_informasi":
                element.click()
                element.send_keys(kejadian[key])

            elif key == "kondisi_mutakhir_dropdown":
                element.click()
                wait.until(
                    EC.visibility_of_element_located(
                        (By.XPATH, f"//div/span[text()='{kejadian[key]}']")
                    )
                ).click()
            else:
                element.clear()
                driver.execute_script(
                    "arguments[0].innerText = arguments[1];", element, kejadian[key]
                )
            time.sleep(0.5)
        wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, xpathmap["btn_tambah_informasi_terkini"])
            )
        )

        wait.until(
            EC.visibility_of_element_located((By.XPATH, xpathmap["btn_simpan"]))
        ).click()
        time.sleep(5)
    except Exception as e:
        print(f"❌ Error: {e}")
