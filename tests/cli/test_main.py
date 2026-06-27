from pathlib import Path

import pytest

from aksara.cli.main import PROJECT_ROOT, main, resolve_source_file
from aksara.errors import AksaraError


def test_cli_version_outputs_version(capsys) -> None:
    exit_code = main(["versi"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "AKSARA" in captured.out


def test_cli_runs_file(tmp_path: Path, capsys) -> None:
    program = tmp_path / "program.aks"
    program.write_text('tulis "Halo"\n', encoding="utf-8")

    exit_code = main(["jalankan", str(program)])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out.strip() == "Halo"


def test_cli_resolves_example_file_by_name(tmp_path: Path, capsys, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    exit_code = main(["jalankan", "halo.aks"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out.splitlines() == [
        "=== Profil Siswa ===",
        "Nama: Reza",
        "Kota: Bandung",
        "Bahasa favorit: AKSARA",
        "Status umur: Dewasa",
        "=== Nilai ===",
        "Nilai tugas: 84",
        "Nilai ujian: 91",
        "Bonus: 5",
        "Rata-rata: 90",
        "Hasil: Lulus",
        "Catatan: Pertahankan ritme belajar.",
        "=== Rencana Belajar ===",
        "Jumlah topik: 4",
        "Topik: lexer, parser, runtime, cli",
        "Ringkasan: {nama: Reza, umur: 21, kota: Bandung}",
        "=== Olah Teks ===",
        "aksara membuat belajar pemrograman terasa dekat",
        "Jumlah kata: 6",
    ]


def test_cli_runs_default_main_file(tmp_path: Path, capsys, monkeypatch) -> None:
    (tmp_path / "main.aks").write_text('tulis "Utama dari main"\n', encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    exit_code = main(["jalankan"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out.strip() == "Utama dari main"


def test_cli_runs_default_utama_file_when_main_is_absent(tmp_path: Path, capsys, monkeypatch) -> None:
    (tmp_path / "utama.aks").write_text('tulis "Utama"\n', encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    exit_code = main(["jalankan"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out.strip() == "Utama"


def test_resolve_source_file_searches_common_locations(tmp_path: Path, monkeypatch) -> None:
    examples_dir = tmp_path / "examples"
    src_dir = tmp_path / "src"
    examples_dir.mkdir()
    src_dir.mkdir()
    (examples_dir / "contoh.aks").write_text('tulis "Contoh"\n', encoding="utf-8")
    (src_dir / "modul.aks").write_text('tulis "Modul"\n', encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    assert resolve_source_file("contoh.aks") == Path("examples/contoh.aks")
    assert resolve_source_file("modul.aks") == Path("src/modul.aks")
    assert resolve_source_file("halo.aks") == PROJECT_ROOT / "examples" / "halo.aks"


def test_cli_reports_missing_file_in_indonesian(tmp_path: Path, capsys, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    exit_code = main(["jalankan", "tidak-ada.aks"])

    captured = capsys.readouterr()

    assert exit_code == 1
    assert 'Berkas "tidak-ada.aks" tidak ditemukan.' in captured.err
    assert "Lokasi yang telah diperiksa:" in captured.err
    assert "✓ Folder saat ini" in captured.err
    assert "✓ examples/" in captured.err
    assert "✓ src/" in captured.err
    assert "Saran:" in captured.err
    assert "aksara jalankan examples/tidak-ada.aks" in captured.err


def test_resolve_source_file_reports_missing_default_files(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    with pytest.raises(AksaraError) as error:
        resolve_source_file()

    assert 'Berkas "main.aks atau utama.aks" tidak ditemukan.' in str(error.value)


def test_cli_build_validates_recursive_sources(tmp_path: Path, capsys, monkeypatch) -> None:
    source_dir = tmp_path / "contoh"
    source_dir.mkdir()
    (source_dir / "program.aks").write_text('tulis "Halo"\n', encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    exit_code = main(["bangun"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "1 berkas .aks" in captured.out
