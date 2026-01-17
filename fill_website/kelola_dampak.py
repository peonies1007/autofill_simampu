from tambah_korban import tambah_korban
from tambah_kerusakan_kerugian import tambah_krs_krg
from tambah_informasi_terkini import tambah_informasi_terkini
from tambah_detali_ker_kgr import tambah_detail_ker_keg


def kelola_dampak(driver, data_obj):
    tambah_korban(driver, data_obj)
    tambah_krs_krg(driver, data_obj)
    tambah_informasi_terkini(driver, data_obj)
    tambah_detail_ker_keg(driver, data_obj)
