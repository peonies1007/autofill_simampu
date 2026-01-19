import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from selenium.common.exceptions import TimeoutException


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
    dt_object = datetime.strptime(date_string, "%Y-%m-%d %H:%M")

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


# def select_xpath(driver)


def select_date(driver, date_string, xpath_date):
    wait = WebDriverWait(driver, 10)
    header_wrap = ""
    date_obj = change_format_date(date_string)
    try:
        wait.until(EC.visibility_of_element_located((By.XPATH, xpath_date))).click()
        WebDriverWait(driver, 1.5).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]"))
        )
        header_wrap = "/html/body/div[3]/div[@class='header']"
        wrapper = "/html/body/div[3]"
    except TimeoutException:
        header_wrap = "/html/body/div[2]/div[@class='header']"
        wrapper = "/html/body/div[2]"

    current_wrap = f"{header_wrap}/div[@class='current']"
    xpath = {
        "tahun": f"{current_wrap}/div[@class='year']",
        "select_tahun": f"//div[@class='year-list-wrapper']/div[text()='{date_obj['year']}']",
        "bulan": f"{current_wrap}/div[2]",
        "select_bulan": f"//div[@class='month-list-wrapper']/div[text()='{date_obj['month']}']",
        "tanggal": "/html/body/div[2]/div[6]/div[2]",
        "select_tanggal": f"//div[@class='dates-wrapper']/div[text()='{date_obj['day']}']",
        "time": f"{wrapper}/div[7]/button[1]",
        "hour": f"{wrapper}/div[6]/div[3]/div/div[1]/div[2]",
        "select_hour": f"//div[@class='hour-list-wrapper']/div[text()='{date_obj['hour']}']",
        "minute": f"{wrapper}/div[6]/div[3]/div/div[3]/div[2]",
        "select_minute": f"//div[@class='minute-list-wrapper']/div[text()='{date_obj['minute']}']",
    }

    field = [
        "tahun",
        "select_tahun",
        "bulan",
        "select_bulan",
        "select_tanggal",
        "time",
        "hour",
        "select_hour",
        "minute",
        "select_minute",
    ]
    for key in field:
        element = wait.until(EC.visibility_of_element_located((By.XPATH, xpath[key])))
        element.click()
        print(f"click {key}")
        time.sleep(0.2)

    wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Save']"))
    ).click()

    print("clear")
