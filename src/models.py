from dataclasses import dataclass
from datetime import date


@dataclass
class Kamar:
    id: str
    tipe: str
    harga_per_malam: int


@dataclass
class Reservasi:
    id: str
    nama_tamu: str
    kamar_id: str
    check_in: date
    check_out: date
    status: str = "aktif"