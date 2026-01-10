from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.by import By
import sys


def delete_data_dump(driver):
    # Menghapus data kejadian terlebih dahulu
    driver.get("https://simampu.bnpb.go.id/de/events_disaster")
    print("🚀 Membuka halaman list data kejadian...")
    wait = WebDriverWait(driver, 10)

    filter = wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//*[@id='content-container']/div[3]/div[1]/form/div/div[1]/div[6]/div/div/div/input",
            )
        )
    )
    filter.clear()
    filter.send_keys(1)
    time.sleep(0.5)
    wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//*[@id='content-container']/div[3]/div[1]/form/div/div[2]/button[2]",
            )
        )
    ).click()
    time.sleep(0.5)

    try:
        WebDriverWait(driver, 1).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[@id='infinite-list']/div[1]/div/a/div/div[1][text()='Draft']",
                )
            )
        )
        time.sleep(0.5)

        wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[@id='infinite-list']/div[1]/div/div")
            )
        ).click()
        time.sleep(0.5)
        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[2]/div[2]/div[2]/div[3]/button[2]")
            )
        ).click()
        print("Data berhasil dihapus...")
    except TimeoutException:
        print("Data tidak ditemukan...")
        print("Lanjut pengisian data...")
