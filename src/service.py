from datetime import date
from uuid import uuid4

from src.models import Kamar, Reservasi


DISKON_LIBURAN = 0.15


def validasi_tanggal(check_in: date, check_out: date) -> None:
    if not isinstance(check_in, date) or not isinstance(check_out, date):
        raise TypeError("Tanggal harus menggunakan format date")

    if check_out <= check_in:
        raise ValueError("Check-out harus setelah check-in")


def sedang_musim_liburan(tanggal: date) -> bool:
    # Periode diskon: 20 Desember sampai 4 Januari.
    return (
        (tanggal.month == 12 and tanggal.day >= 20)
        or (tanggal.month == 1 and tanggal.day < 5)
    )


def hitung_total_sebelum_diskon(
    harga_per_malam: int,
    check_in: date,
    check_out: date,
) -> int:
    validasi_tanggal(check_in, check_out)

    if not isinstance(harga_per_malam, int) or isinstance(harga_per_malam, bool):
        raise TypeError("Harga kamar harus berupa bilangan bulat")

    if harga_per_malam <= 0:
        raise ValueError("Harga kamar harus lebih dari 0")

    jumlah_malam = (check_out - check_in).days
    return harga_per_malam * jumlah_malam


def hitung_diskon_liburan(
    harga_per_malam: int,
    check_in: date,
    check_out: date,
) -> int:
    total_awal = hitung_total_sebelum_diskon(
        harga_per_malam,
        check_in,
        check_out,
    )

    jumlah_malam = (check_out - check_in).days

    semua_malam_liburan = all(
        sedang_musim_liburan(
            date.fromordinal(check_in.toordinal() + hari)
        )
        for hari in range(jumlah_malam)
    )

    if semua_malam_liburan:
        return round(total_awal * DISKON_LIBURAN)

    return 0


def hitung_total(
    harga_per_malam: int,
    check_in: date,
    check_out: date,
) -> int:
    total_awal = hitung_total_sebelum_diskon(
        harga_per_malam,
        check_in,
        check_out,
    )
    diskon = hitung_diskon_liburan(
        harga_per_malam,
        check_in,
        check_out,
    )

    return total_awal - diskon


def cek_ketersediaan(
    kamar_id: str,
    check_in: date,
    check_out: date,
    reservasi: list[Reservasi],
) -> bool:
    validasi_tanggal(check_in, check_out)

    for item in reservasi:
        if item.kamar_id != kamar_id or item.status != "aktif":
            continue

        bertumpang_tindih = (
            check_in < item.check_out
            and item.check_in < check_out
        )

        if bertumpang_tindih:
            return False

    return True


def buat_reservasi(
    nama_tamu: str,
    kamar_id: str,
    check_in: date,
    check_out: date,
    daftar_kamar: list[Kamar],
    reservasi: list[Reservasi],
) -> Reservasi:
    if not isinstance(nama_tamu, str) or not nama_tamu.strip():
        raise ValueError("Nama tamu wajib diisi")

    if not isinstance(kamar_id, str) or not kamar_id.strip():
        raise ValueError("ID kamar wajib diisi")

    validasi_tanggal(check_in, check_out)

    kamar = next(
        (item for item in daftar_kamar if item.id == kamar_id),
        None,
    )

    if kamar is None:
        raise ValueError("Kamar tidak ditemukan")

    if not cek_ketersediaan(kamar_id, check_in, check_out, reservasi):
        raise ValueError("Kamar tidak tersedia pada tanggal tersebut")

    reservasi_baru = Reservasi(
        id=str(uuid4())[:8],
        nama_tamu=nama_tamu.strip(),
        kamar_id=kamar_id,
        check_in=check_in,
        check_out=check_out,
    )

    reservasi.append(reservasi_baru)
    return reservasi_baru


def batalkan_reservasi(
    id_reservasi: str,
    reservasi: list[Reservasi],
) -> Reservasi:
    for item in reservasi:
        if item.id == id_reservasi:
            if item.status == "dibatalkan":
                raise ValueError("Reservasi sudah dibatalkan")

            item.status = "dibatalkan"
            return item

    raise ValueError("Reservasi tidak ditemukan")