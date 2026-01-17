from constants.key_kategori import (
    KATEGORI,
    KATEGORI_RUSAK,
    FIELD_KATEGORI,
    KATEGORI_HEWAN,
)

# List 1 space 5
list_1 = "     "
# List 2 space 8
list_2 = "        "


def get_informasi_terkini(array):
    head = [
        {"head": "PENANGANAN", "waktu": "Penanganan"},
        {"head": "TERKONDISI", "waktu": "Terkondisi"},
    ]
    text = ""
    for i, item in enumerate(array):
        text += f"""
={head[i]["head"]}=
1. Waktu {head[i]["waktu"]}\t:\t{item["waktu_penanganan_terkondisi"]}
2. Sumber Informasi\t:\t{item["sumber_informasi"]} 
3. Kondisi Mutakhir Pendek\t:\t{item["kondisi_mutakhir_dropdown"]} 
4. Kondis Mutakhir Deskripsi\t:\t
{list_1}{item["kondisi_mutakhir_deskripsi"]}
5. Upaya Penanganan\t:\t{item["upaya_penanganan"]}
6. Kendala Lapangan\t:\t{item["kendala_lapangan"]}
7. Informasi Tambahan\t:\t{item["informasi_tambahan"]}

        """
    return text


def get_korban_jiwa(array_data):
    text = ""
    array_dict_korban = [
        {"under": "total_kk", "no_under": "Total KK"},
        {"under": "terdampak_orang", "no_under": "Terdampak"},
        {"under": "meninggal_orang", "no_under": "Meninggal"},
        {"under": "hilang_orang", "no_under": "Hilang"},
        {"under": "luka_ringan_orang", "no_under": "Luka Ringan"},
        {"under": "luka_berat_orang", "no_under": "Luka Berat"},
        {"under": "mengungsi_orang", "no_under": "Mengungsi"},
        {"under": "titik_pengungsian", "no_under": "Titik Penungsian"},
    ]
    for data in array_data:
        if data:
            text += "===KELOLA DAMPAK TERKINI===\n"
            array_korban_teks = []
            korban_teks = ""
            for key in array_dict_korban:
                if data[key["under"]]:
                    if int(data[key["under"]]):
                        array_korban_teks.append(key)

            for i, item in enumerate(array_korban_teks):
                korban_teks += (
                    f"{i + 3}. {item['no_under']}\t:\t{data[item['under']]}\n"
                )

            text += f"""=KEL/DS. {data["dampak_ds_kelurahan"]}, KEC. {data["dampak_kecamatan"]}=
1. Dampak Kecamatan\t:\t{data["dampak_kecamatan"]}
2. Dampak Desa / Kelurahan\t:\t{data["dampak_ds_kelurahan"]} 
{korban_teks}
"""
    return text


def get_kerusakan_kerugian(data_array):
    text = ""
    for data in data_array:
        text += f"=Kel/Ds. {data['kerusakan_kerugian_ds_kelurahan']}, Kec. {data['kerusakan_kerugian_kecamatan']}=\n"
        text += f"1. Kelurahan\t:\t{data['kerusakan_kerugian_kecamatan']}\n"
        text += f"2. Kelurahan\t:\t{data['kerusakan_kerugian_kecamatan']}\n"

        for key_kategori in KATEGORI:
            head_kategori = []
            value_kategori_text = ""
            for j, key_field_kategori in enumerate(FIELD_KATEGORI[key_kategori]):
                value = data["kategori"][key_kategori][key_field_kategori]
                if value:
                    head_kategori.append(key_kategori)
                    value_kategori_text += (
                        f"{list_1}- {KATEGORI_RUSAK[j]}\t:\t{value}\n"
                    )
                    if key_kategori == "hewan_ternak":
                        value_kategori_text += (
                            f"{list_1}- {KATEGORI_HEWAN[j]}\t:\t{value}\n"
                        )

            for k, item in enumerate(head_kategori):
                print(k)
                text += f"{k + 3}. {item.replace('_', ' ').title()}\n"
                text += value_kategori_text

    return text


def confirm_text(data):
    tambah_kejadian = data["tambah_kejadian"]
    detail_kejadian = data["detail_kejadian"]
    tambah_informasi_terkini = detail_kejadian["tambah_informasi_terkini"]

    kelola_dampak_terkini = detail_kejadian["kelola_dampak_terkini"]
    tambah_korban_jiwa = kelola_dampak_terkini["tambah_korban_jiwa"]
    tambah_kerusakan_dan_kerugian = kelola_dampak_terkini[
        "tambah_kerusakan_dan_kerugian"
    ]
    tambah_detail_ker_krg = kelola_dampak_terkini["tambah_detail_ker_krg"]

    sebaran_dampak = ""
    for i, item in enumerate(tambah_kejadian["sebaran_dampak"]):
        sebaran_dampak += f"{list_1}{i + 1}). {item['sebaran_dampak_kec']}\n"
        for kel_des in item["sebaran_dampak_ds_kel"]:
            sebaran_dampak += f"{list_2}- {kel_des}\n"

    return f"""
DATA PENGISIAN SIMAMPU BPBD KABUPATEN SRAGEN*

=====TAMBAH KEJADIAN=====
1. Nama Kejadian\t:\t{tambah_kejadian["nama_kejadian"]}
3. Tanggal & Waktu Kejadian Terjadi\t:\t{tambah_kejadian["tanggal_waktu_kejadian_terjadi"]} 
4. Tanggal & Waktu Kejadian Berakhir\t:\t{tambah_kejadian["tanggal_waktu_kejadian_berakhir"]} 
5. Jenis Bencana\t:\t{tambah_kejadian["jenis_bencana"]}
6. Kronologi\t:\t{tambah_kejadian["kronologi"]}
7. Peringatan Dini\t:\t{tambah_kejadian["peringatan_dini"]}
8. Sebab Kejadian\t:\t{tambah_kejadian["sebab_kejadian"]}
9. Deskripsi\t:\t{tambah_kejadian["deskripsi"]}
10. Sebaran Dampak\t:\t
{sebaran_dampak}
=====DETAIL KEJADIAN=====
===TAMBAH INFORMASI TERKINI==={get_informasi_terkini(tambah_informasi_terkini)}
{get_korban_jiwa(tambah_korban_jiwa)}
{get_kerusakan_kerugian(tambah_kerusakan_dan_kerugian)}
"""
