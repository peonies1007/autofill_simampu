import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime


def change_month(int_bulan):
    nama_bulan_id = [
        "",
        "Januari",
        "Februari",
        "Maret",
        "April",
        "Mei",
        "Juni",
        "Juli",
        "Agustus",
        "September",
        "Oktober",
        "November",
        "Desember",
    ]
    bulan_lengkap = nama_bulan_id[int_bulan]
    month_change = {
        "Januari": "Jan",
        "Februari": "Feb",
        "Maret": "Mar",
        "April": "Apr",
        "Mei": "May",
        "Juni": "Jun",
        "Juli": "Jul",
        "Agustus": "Aug",
        "September": "Sep",
        "Oktober": "Oct",
        "November": "Nov",
        "Desember": "Dec",
    }

    return month_change.get(bulan_lengkap.title(), "Bulan tidak valid")


def change_format_date(date_string):
    # Mengonversi string menjadi objek datetime
    dt_object = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")

    month = change_month(dt_object.month)
    hour = ""
    minute = ""
    if dt_object.hour < 10:
        hour = f"0{dt_object.hour}"
    else:
        hour = dt_object.hour
    if dt_object.minute < 10:
        minute = f"0{dt_object.minute}"
    else:
        minute = dt_object.minute
    # Mengambil komponen masing-masing
    return {
        "year": dt_object.year,
        "month": month,
        "day": dt_object.day,
        "hour": hour,
        "minute": minute,
    }


def select_date(driver, date_string, xpath_date):
    wait = WebDriverWait(driver, 10)

    date_obj = change_format_date(date_string)

    xpath = {
        "tanggal_waktu_kejadian_terjadi": '//*[@id="content-container"]/div[3]/div/div/div/div/div/div/div/div/div/form/div[2]/div[1]/div/div/div/div/input',
        "tanggal_waktu_kejadian_berakhir": '//*[@id="content-container"]/div[3]/div/div/div/div/div/div/div/div/div/form/div[2]/div[2]/div/div/div/div/input',
        "tahun": "/html/body/div[2]/div[5]/div[2]/div[1]",
        "select_tahun": f"//div[@class='year-list-wrapper']/div[text()='{date_obj['year']}']",
        "bulan": "/html/body/div[2]/div[5]/div[2]/div[2]",
        "select_bulan": f"/html/body/div[2]/div[1]/div[text()='{date_obj['month']}']",
        "tanggal": "/html/body/div[2]/div[6]/div[2]",
        "select_tanggal": f"/html/body/div[2]/div[6]/div[2]/div[text()='{date_obj['day']}']",
        "simpan_tambah_kejadian": "//*[@id='content-container']/div[3]/div/div/div/div/div/div/div/div/div/form/div[14]/button",
        "time": "/html/body/div[2]/div[7]/button[1]",
        "hour": "/html/body/div[2]/div[6]/div[3]/div/div[1]/div[2]",
        "select_hour": f"/html/body/div[2]/div[3]/div[text()='{date_obj['hour']}']",
        "minute": "/html/body/div[2]/div[6]/div[3]/div/div[3]/div[2]",
        "select_minute": f"/html/body/div[2]/div[4]/div[text()='{date_obj['minute']}']",
    }

    wait.until(EC.visibility_of_element_located((By.XPATH, xpath_date))).click()

    tahun = wait.until(EC.visibility_of_element_located((By.XPATH, xpath["tahun"])))
    tahun.click()
    print("click tahun")

    select_tahun = wait.until(
        EC.visibility_of_element_located((By.XPATH, xpath["select_tahun"]))
    )
    select_tahun.click()
    print("select tahun")

    bulan = wait.until(EC.visibility_of_element_located((By.XPATH, xpath["bulan"])))
    bulan.click()
    print("click bulan")

    select_bulan = wait.until(
        EC.visibility_of_element_located((By.XPATH, xpath["select_bulan"]))
    )
    select_bulan.click()
    print("select bulan")

    select_tanggal = wait.until(
        EC.visibility_of_element_located((By.XPATH, xpath["select_tanggal"]))
    )
    select_tanggal.click()
    print("select tanggal")

    wait.until(EC.visibility_of_element_located((By.XPATH, xpath["time"]))).click()

    hour = wait.until(EC.visibility_of_element_located((By.XPATH, xpath["hour"])))
    hour.click()
    print("click hour")

    select_hour = wait.until(
        EC.visibility_of_element_located((By.XPATH, xpath["select_hour"]))
    )
    select_hour.click()
    print(date_obj["hour"])
    print("select hour")

    minute = wait.until(EC.visibility_of_element_located((By.XPATH, xpath["minute"])))
    minute.click()
    print("click minute")

    select_minute = wait.until(
        EC.visibility_of_element_located((By.XPATH, xpath["select_minute"]))
    )
    select_minute.click()
    print(date_obj["minute"])
    print("select minute")

    wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Save']"))
    ).click()

    print("clear")
