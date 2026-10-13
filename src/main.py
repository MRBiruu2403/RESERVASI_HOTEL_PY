from datetime import date

from src.models import Kamar
from src.service import buat_reservasi, hitung_total


def main():
    daftar_kamar = [
        Kamar("H101", "Standard", 500_000),
        Kamar("H201", "Deluxe", 800_000),
        Kamar("H301", "Suite", 1_500_000),
    ]
    daftar_reservasi = []

    print("=== Sistem Reservasi Hotel ===")
    print("Daftar kamar:")

    for kamar in daftar_kamar:
        print(
            f"{kamar.id} | {kamar.tipe} | "
            f"Rp{kamar.harga_per_malam:,} per malam"
        )

    try:
        nama = input("\nNama tamu: ")
        kamar_id = input("ID kamar: ").strip().upper()
        check_in = date.fromisoformat(input("Check-in (YYYY-MM-DD): "))
        check_out = date.fromisoformat(input("Check-out (YYYY-MM-DD): "))

        hasil = buat_reservasi(
            nama,
            kamar_id,
            check_in,
            check_out,
            daftar_kamar,
            daftar_reservasi,
        )

        kamar = next(
            item for item in daftar_kamar
            if item.id == hasil.kamar_id
        )

        total = hitung_total(
            kamar.harga_per_malam,
            check_in,
            check_out,
        )

        print("\nReservasi berhasil!")
        print(f"ID reservasi: {hasil.id}")
        print(f"Nama tamu: {hasil.nama_tamu}")
        print(f"Kamar: {kamar.id} ({kamar.tipe})")
        print(f"Lama menginap: {(check_out - check_in).days} malam")
        print(f"Total pembayaran: Rp{total:,}")

    except (ValueError, TypeError) as error:
        print(f"\nReservasi gagal: {error}")


if __name__ == "__main__":
    main()