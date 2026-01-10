from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.by import By
import sys


def tambah_informasi_terkini(driver):
    driver.get("https://simampu.bnpb.go.id/de/events_disaster/3314104202601082/show")
    print("🚀 Membuka halaman data kejadian...")
    wait = WebDriverWait(driver, 10)

    xpathmap = {}

    wait.until(
        EC.visibility_of_element_located(
            By.XPATH, "//div[text()='Detil Kejadian Bencana']"
        )
    )
