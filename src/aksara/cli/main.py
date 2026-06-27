"""AKSARA command-line interface."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Iterable
from pathlib import Path
from typing import Sequence

from aksara import __version__
from aksara.compiler import validate_source
from aksara.errors import AksaraError
from aksara.interpreter.runner import run_source

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_SOURCE_FILES = ("main.aks", "utama.aks")
SOURCE_SEARCH_DIRS = (
    ("Folder saat ini", Path(".")),
    ("examples/", Path("examples")),
    ("src/", Path("src")),
    ("root proyek", PROJECT_ROOT),
    ("examples/", PROJECT_ROOT / "examples"),
    ("src/", PROJECT_ROOT / "src"),
)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the AKSARA CLI and return a process exit code."""
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "jalankan":
            return _run_file(resolve_source_file(args.file))
        if args.command == "versi":
            print(f"AKSARA {__version__}")
            return 0
        if args.command == "bantuan" or args.command is None:
            parser.print_help()
            return 0
        if args.command == "buat":
            return _create_project(Path(args.name))
        if args.command == "bangun":
            return _build_project(Path.cwd())
    except AksaraError as error:
        print(error, file=sys.stderr)
        return 1
    except OSError as error:
        print(_format_os_error(error), file=sys.stderr)
        return 1

    parser.print_help()
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="aksara", description="Bahasa pemrograman AKSARA.")
    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser("jalankan", help="Jalankan berkas .aks.")
    run_parser.add_argument("file", nargs="?", help="Path berkas .aks.")

    subparsers.add_parser("versi", help="Tampilkan versi AKSARA.")
    subparsers.add_parser("bantuan", help="Tampilkan bantuan.")

    create_parser = subparsers.add_parser("buat", help="Buat proyek AKSARA baru.")
    create_parser.add_argument("name", help="Nama folder proyek.")

    subparsers.add_parser("bangun", help="Validasi proyek AKSARA saat ini.")
    return parser


def resolve_source_file(filename: str | None = None) -> Path:
    """Resolve a runnable AKSARA source file from common project locations."""
    names = (filename,) if filename else DEFAULT_SOURCE_FILES
    checked: list[tuple[str, Path]] = []
    seen: set[Path] = set()

    for label, directory in SOURCE_SEARCH_DIRS:
        for name in names:
            candidate = directory / name
            if candidate not in seen:
                checked.append((label, candidate))
                seen.add(candidate)
            if candidate.is_file():
                return candidate

    raise AksaraError(_format_source_not_found(filename, checked))


def _format_source_not_found(filename: str | None, checked: Sequence[tuple[str, Path]]) -> str:
    source_name = filename or "main.aks atau utama.aks"
    checked_labels = _unique_labels(label for label, _ in checked)
    message = [
        f'Berkas "{source_name}" tidak ditemukan.',
        "",
        "Lokasi yang telah diperiksa:",
        "",
    ]
    message.extend(f"✓ {label}" for label in checked_labels)

    suggestion = _first_suggested_path(filename)
    if suggestion:
        message.extend(["", "Saran:", "", f"aksara jalankan {suggestion}"])

    return "\n".join(message)


def _unique_labels(labels: Iterable[str]) -> list[str]:
    unique: list[str] = []
    for label in labels:
        if label not in unique:
            unique.append(label)
    return unique


def _first_suggested_path(filename: str | None) -> str | None:
    if not filename:
        return None
    if Path(filename).parent == Path("."):
        return (Path("examples") / filename).as_posix()
    for directory in (Path("examples"), PROJECT_ROOT / "examples", Path("src"), PROJECT_ROOT / "src"):
        candidate = directory / filename
        if candidate.is_file():
            try:
                return candidate.relative_to(Path.cwd()).as_posix()
            except ValueError:
                return candidate.as_posix()
    return None


def _run_file(path: Path) -> int:
    try:
        source = path.read_text(encoding="utf-8")
    except OSError as error:
        raise AksaraError(f'Tidak dapat membaca berkas "{path}": {error.strerror or error}') from error

    result = run_source(source)
    for line in result.output:
        print(line)
    return 0


def _format_os_error(error: OSError) -> str:
    detail = error.strerror or str(error)
    if error.filename:
        return f'Tidak dapat mengakses "{error.filename}": {detail}'
    return f"Operasi sistem gagal: {detail}"


def _create_project(path: Path) -> int:
    path.mkdir(parents=False, exist_ok=False)
    source_path = path / "utama.aks"
    source_path.write_text('buat nama = "AKSARA"\ntulis "Halo, " + nama\n', encoding="utf-8")
    print(f"Proyek dibuat: {path}")
    return 0


def _build_project(path: Path) -> int:
    files = sorted(source_file for source_file in path.rglob("*.aks") if ".git" not in source_file.parts)
    if not files:
        print("Tidak ada berkas .aks untuk dibangun.")
        return 0

    for source_file in files:
        validate_source(source_file.read_text(encoding="utf-8"))
    print(f"Berhasil memvalidasi {len(files)} berkas .aks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
