"""Built-in AKSARA standard library functions."""

from __future__ import annotations

import random
import shutil
import time
from datetime import date, datetime
from pathlib import Path
from typing import Callable

from aksara.errors import RuntimeAksaraError
from aksara.runtime.environment import Environment

NativeFunction = Callable[..., object]


def create_standard_environment() -> Environment:
    """Create an environment containing AKSARA standard library functions."""
    environment = Environment()
    for name, function in _standard_functions().items():
        environment.define(name, function)
    return environment


def _standard_functions() -> dict[str, NativeFunction]:
    return {
        "panjang": _panjang,
        "acak": _acak,
        "huruf_besar": _huruf_besar,
        "huruf_kecil": _huruf_kecil,
        "gabung": _gabung,
        "pisah": _pisah,
        "tunggu": _tunggu,
        "waktu": _waktu,
        "tanggal": _tanggal,
        "buka": _buka,
        "tulis_berkas": _tulis_berkas,
        "hapus": _hapus,
        "buat_folder": _buat_folder,
    }


def _expect_arity(name: str, args: tuple[object, ...], minimum: int, maximum: int | None = None) -> None:
    max_args = minimum if maximum is None else maximum
    if not minimum <= len(args) <= max_args:
        if minimum == max_args:
            expected = str(minimum)
        else:
            expected = f"{minimum} sampai {max_args}"
        raise RuntimeAksaraError(f"Fungsi {name} membutuhkan {expected} argumen.")


def _panjang(*args: object) -> int:
    _expect_arity("panjang", args, 1)
    value = args[0]
    if not isinstance(value, (str, list, dict)):
        raise RuntimeAksaraError("Fungsi panjang() hanya menerima string, list, atau dictionary.")
    return len(value)


def _acak(*args: object) -> float | int:
    _expect_arity("acak", args, 0, 2)
    if not args:
        return random.random()
    if len(args) == 2 and all(isinstance(arg, int) for arg in args):
        return random.randint(int(args[0]), int(args[1]))
    raise RuntimeAksaraError("Fungsi acak() menerima nol argumen atau dua integer.")


def _huruf_besar(*args: object) -> str:
    _expect_arity("huruf_besar", args, 1)
    if not isinstance(args[0], str):
        raise RuntimeAksaraError("Fungsi huruf_besar() hanya menerima string.")
    return args[0].upper()


def _huruf_kecil(*args: object) -> str:
    _expect_arity("huruf_kecil", args, 1)
    if not isinstance(args[0], str):
        raise RuntimeAksaraError("Fungsi huruf_kecil() hanya menerima string.")
    return args[0].lower()


def _gabung(*args: object) -> str:
    _expect_arity("gabung", args, 2)
    items, separator = args
    if not isinstance(items, list) or not isinstance(separator, str):
        raise RuntimeAksaraError("Fungsi gabung() membutuhkan list dan string pemisah.")
    return separator.join(str(item) for item in items)


def _pisah(*args: object) -> list[str]:
    _expect_arity("pisah", args, 2)
    text, separator = args
    if not isinstance(text, str) or not isinstance(separator, str):
        raise RuntimeAksaraError("Fungsi pisah() membutuhkan string dan string pemisah.")
    return text.split(separator)


def _tunggu(*args: object) -> None:
    _expect_arity("tunggu", args, 1)
    seconds = args[0]
    if not isinstance(seconds, (int, float)):
        raise RuntimeAksaraError("Fungsi tunggu() membutuhkan angka detik.")
    time.sleep(float(seconds))
    return None


def _waktu(*args: object) -> str:
    _expect_arity("waktu", args, 0)
    return datetime.now().isoformat(timespec="seconds")


def _tanggal(*args: object) -> str:
    _expect_arity("tanggal", args, 0)
    return date.today().isoformat()


def _buka(*args: object) -> str:
    _expect_arity("buka", args, 1)
    if not isinstance(args[0], str):
        raise RuntimeAksaraError("Fungsi buka() membutuhkan path string.")
    return Path(args[0]).read_text(encoding="utf-8")


def _tulis_berkas(*args: object) -> None:
    _expect_arity("tulis_berkas", args, 2)
    path, content = args
    if not isinstance(path, str) or not isinstance(content, str):
        raise RuntimeAksaraError("Fungsi tulis_berkas() membutuhkan path dan isi string.")
    Path(path).write_text(content, encoding="utf-8")
    return None


def _hapus(*args: object) -> None:
    _expect_arity("hapus", args, 1)
    if not isinstance(args[0], str):
        raise RuntimeAksaraError("Fungsi hapus() membutuhkan path string.")
    path = Path(args[0])
    if path.is_dir():
        shutil.rmtree(path)
    elif path.exists():
        path.unlink()
    return None


def _buat_folder(*args: object) -> None:
    _expect_arity("buat_folder", args, 1)
    if not isinstance(args[0], str):
        raise RuntimeAksaraError("Fungsi buat_folder() membutuhkan path string.")
    Path(args[0]).mkdir(parents=True, exist_ok=True)
    return None
