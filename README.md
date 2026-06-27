# AKSARA

[![Python CI](https://github.com/zrdub/aksara/actions/workflows/python.yml/badge.svg)](https://github.com/zrdub/aksara/actions/workflows/python.yml)
![Python Versions](https://img.shields.io/badge/python-3.12%20%7C%203.13-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

AKSARA adalah bahasa pemrograman interpreted modern dengan kata kunci berbahasa
Indonesia. Repositori ini berisi implementasi awal lexer, parser, AST, runtime,
interpreter, standard library, CLI, contoh program, dokumentasi bahasa, dan
pengujian otomatis.

## Current Version

Versi saat ini: `0.1.0`

AKSARA membutuhkan Python `3.12` atau yang lebih baru.

## Installation

Instal dari checkout lokal:

```bash
git clone https://github.com/zrdub/aksara.git
cd aksara
python -m pip install --upgrade pip
python -m pip install -e .
```

Instal dependensi pengembangan untuk menjalankan test suite:

```bash
python -m pip install -e ".[dev]"
python -m pip install build ruff
```

## Usage

Jalankan program contoh:

```bash
aksara jalankan examples/halo.aks
```

Atau gunakan modul CLI langsung dari checkout:

```bash
python -m aksara.cli.main jalankan examples/halo.aks
python -m aksara.cli.main versi
python -m aksara.cli.main bantuan
```

Perintah CLI utama:

- `aksara jalankan [file.aks]`
- `aksara versi`
- `aksara bantuan`
- `aksara buat nama_proyek`
- `aksara bangun`

Resolusi berkas untuk `aksara jalankan`:

- Jika nama berkas diberikan, AKSARA mencari di folder saat ini, `examples/`,
  `src/`, dan root proyek.
- Jika nama berkas tidak diberikan, AKSARA otomatis menjalankan `main.aks` atau
  `utama.aks` jika salah satunya ditemukan.
- Jika berkas tidak ditemukan, CLI menampilkan pesan Indonesia yang menjelaskan
  lokasi yang diperiksa dan saran perintah eksplisit, misalnya
  `aksara jalankan examples/halo.aks`.

## Examples

Contoh dasar:

```aksara
buat nama = "Reza"
buat umur = 21

jika umur >= 18
    tulis "Halo, " + nama
jika_tidak
    tulis "Anak"
selesai
```

Contoh dengan list, dictionary, dan fungsi standar:

```aksara
buat daftar_topik = ["lexer", "parser", "runtime", "cli"]
buat ringkasan = {"nama": "Reza", "umur": 21, "kota": "Bandung"}

tulis "Jumlah topik: " + panjang(daftar_topik)
tulis "Topik: " + gabung(daftar_topik, ", ")
tulis "Ringkasan: " + ringkasan
```

Lihat contoh lengkap di [`examples/halo.aks`](examples/halo.aks).

## Documentation

- Panduan bahasa: [`docs/bahasa.md`](docs/bahasa.md)
- Panduan kontribusi: [`CONTRIBUTING.md`](CONTRIBUTING.md)
- Kebijakan keamanan: [`SECURITY.md`](SECURITY.md)
- Riwayat perubahan: [`CHANGELOG.md`](CHANGELOG.md)

## Development

Jalankan test suite:

```bash
python -m pytest
```

Periksa formatting:

```bash
python -m ruff format --check src tests
```

Bangun source distribution dan wheel:

```bash
python -m build
```

## Roadmap

- Memperkuat stabilitas lexer, parser, runtime, dan CLI melalui regression tests.
- Memperluas dokumentasi sintaks, tipe data, standard library, dan pesan error.
- Menambahkan contoh program yang mencakup workflow pembelajaran bertahap.
- Menetapkan proses rilis berulang dengan changelog, tag Git, dan artefak paket.
- Mengevaluasi dukungan tooling tambahan seperti formatter resmi, linter, dan type checking.

## Contributing

Kontribusi diterima melalui issue dan pull request. Sebelum membuka PR, baca
[`CONTRIBUTING.md`](CONTRIBUTING.md), ikuti [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md),
jalankan test suite, dan pastikan perubahan tercatat di [`CHANGELOG.md`](CHANGELOG.md)
jika memengaruhi perilaku pengguna.

## License

AKSARA dirilis di bawah lisensi MIT. Lihat [`LICENSE`](LICENSE).
