from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# from delete_data_dump import delete_data_dump
from fill_website.tambah_kejadian import tambah_kejadian
from fill_website.kelola_dampak import kelola_dampak


def isi_form_bpbd_sragen(data_obj):
    # 1. Koneksi ke browser yang sudah terbuka (Remote Debugging)
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )

    # delete_data_dump(driver)
    # sys.exit(0)
    # 2. Buka URL Target (Ganti dengan URL formulir Anda)
    # driver.get("https://simampu.bnpb.go.id/de/events_disaster_create")

    tambah_kejadian(driver, data_obj)
    kelola_dampak(driver, data_obj)
