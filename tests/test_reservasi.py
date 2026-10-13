import unittest
from datetime import date

from src.models import Kamar, Reservasi
from src.service import (
    buat_reservasi,
    batalkan_reservasi,
    cek_ketersediaan,
    hitung_total,
)


class TestReservasiHotel(unittest.TestCase):
    def setUp(self):
        self.daftar_kamar = [
            Kamar("H101", "Standard", 500_000),
            Kamar("H201", "Deluxe", 800_000),
        ]
        self.reservasi = [
            Reservasi(
                "R001",
                "Ayu",
                "H101",
                date(2026, 11, 10),
                date(2026, 11, 12),
            )
        ]

    def test_total_tiga_malam_di_luar_musim_liburan(self):
        total = hitung_total(
            500_000,
            date(2026, 11, 10),
            date(2026, 11, 13),
        )
        self.assertEqual(total, 1_500_000)

    def test_diskon_musim_liburan(self):
        total = hitung_total(
            500_000,
            date(2026, 12, 20),
            date(2026, 12, 23),
        )
        self.assertEqual(total, 1_275_000)

    def test_kamar_bertumpang_tindih_tidak_tersedia(self):
        tersedia = cek_ketersediaan(
            "H101",
            date(2026, 11, 11),
            date(2026, 11, 13),
            self.reservasi,
        )
        self.assertFalse(tersedia)

    def test_reservasi_kamar_tersedia_berhasil(self):
        hasil = buat_reservasi(
            "Budi",
            "H201",
            date(2026, 11, 10),
            date(2026, 11, 12),
            self.daftar_kamar,
            self.reservasi,
        )
        self.assertEqual(hasil.nama_tamu, "Budi")

    def test_reservasi_kamar_bertumpang_tindih_ditolak(self):
        with self.assertRaises(ValueError):
            buat_reservasi(
                "Budi",
                "H101",
                date(2026, 11, 11),
                date(2026, 11, 13),
                self.daftar_kamar,
                self.reservasi,
            )

    def test_reservasi_bisa_dibatalkan(self):
        hasil = batalkan_reservasi("R001", self.reservasi)
        self.assertEqual(hasil.status, "dibatalkan")


if __name__ == "__main__":
    unittest.main()