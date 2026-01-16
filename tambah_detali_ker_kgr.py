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
from selenium.webdriver.common.keys import Keys

kejadian = [
    {
        "nama_kerusakan": "Pohon Jati",
        "nama_pemilik": "Satimin",
        "kategori": "rumah (unit)",
        "kerusakan": "Rusak Berat",
        "luasan_terdampak": "",
        "satuan_luasan": "",
        "kerugian": "500000",
        "alamat": "Kamp. Widoro , RT. 41/12, Kel.Sragen Wetan, Kec. Sragen, Kab. Sragen",
        "deskripsi": "1 Pohon Jati Diameter -+ 20 Cm Tumbang Menghalangi Jalan Kampung",
    },
    {
        "nama_kerusakan": "Pohon Jati",
        "nama_pemilik": "Bambang",
        "kategori": "rumah (unit)",
        "kerusakan": "Rusak Berat",
        "luasan_terdampak": "",
        "satuan_luasan": "",
        "kerugian": "500000",
        "alamat": "Kamp. Widoro , RT. 41/12, Kel.Sragen Wetan, Kec. Sragen, Kab. Sragen",
        "deskripsi": "1 Pohon Jati Diameter -+ 20 Cm Tumbang Menghalangi Jalan Kampung",
    },
]
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=chrome_options
)


def tambah_detail_ker_keg(driver, data_obj):
    print("🚀 Membuka halaman data kejadian...")
    wait = WebDriverWait(driver, 10)

    xpathmap = {
        "btn_tambah": '//*[@id="content-container"]/div[3]/div[4]/div/div/div[1]/button',
        "nama_kerusakan": "/html/body/div[2]/div[2]/div/div/form/div[1]/div[1]/div/div/input",
        "nama_pemilik": "/html/body/div[2]/div[2]/div/div/form/div[1]/div[2]/div/div/input",
        "kategori": "/html/body/div[2]/div[2]/div/div/form/div[1]/div[3]/div/div/div",
        "wrap_list_ktg_ker": "/html/body/div[3]",
        "kerusakan": "/html/body/div[2]/div[2]/div/div/form/div[1]/div[4]/div/div/div",
        "luasan_terdampak": "/html/body/div[2]/div[2]/div/div/form/div[2]/div[1]/div/div/div/input",
        "satuan_luasan": "/html/body/div[2]/div[2]/div/div/form/div[2]/div[2]/div/div/div/input",
        "kerugian": "/html/body/div[2]/div[2]/div/div/form/div[2]/div[3]/div/div/div[1]/input",
        "alamat": "/html/body/div[2]/div[2]/div/div/form/div[3]/div/div/input",
        "deskripsi": "/html/body/div[2]/div[2]/div/div/form/div[6]/div/div/div/textarea",
        "btn_simpan": "/html/body/div[2]/div[2]/div/div/form/button",
    }

    all_fields = [
        "nama_kerusakan",
        "nama_pemilik",
        "kategori",
        "kerusakan",
        "luasan_terdampak",
        "satuan_luasan",
        "kerugian",
        "alamat",
        "deskripsi",
    ]

    field_ktg_ker = [
        "kategori",
        "kerusakan",
    ]

    btn_tambah = wait.until(
        EC.visibility_of_element_located((By.XPATH, xpathmap["btn_tambah"]))
    )
    btn_tambah.click()
    time.sleep(0.5)
    for item in data_obj:
        for key in all_fields:
            if item[key]:
                element = wait.until(
                    EC.visibility_of_element_located((By.XPATH, xpathmap[key]))
                )
                element.click()

                if key in field_ktg_ker:
                    wait.until(
                        EC.visibility_of_element_located(
                            (
                                By.XPATH,
                                f"{xpathmap['wrap_list_ktg_ker']}/div/span[text()='{item[key]}']",
                            )
                        )
                    ).click()
                else:
                    element.send_keys(Keys.CONTROL, "a")  # Select all text
                    element.send_keys(Keys.DELETE)
                    element.send_keys(Keys.CONTROL, "A")  # Select all text
                    element.send_keys(Keys.DELETE)
                    element.send_keys(item[key])
                time.sleep(0.2)
    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "/html/body/div[2]/div[2]/div/button")
        )
    ).click()
    # btn_simpan.click()
    # btn_simpan = wait.until(
    #     EC.visibility_of_element_located((By.XPATH, xpathmap["btn_simpan"]))
    # )
    # btn_simpan.click()


tambah_detail_ker_keg(driver, kejadian)
