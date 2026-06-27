# AKSARA

AKSARA adalah bahasa pemrograman interpreted modern dengan kata kunci berbahasa
Indonesia. Implementasi awal ini menyediakan lexer, parser, AST, runtime,
interpreter, standard library, CLI, contoh program, dokumentasi, dan pengujian.

## Menjalankan Program

```bash
aksara jalankan examples/halo.aks
```

## Contoh

```aksara
buat nama = "Reza"
buat umur = 21

jika umur >= 18
    tulis "Halo, " + nama
jika_tidak
    tulis "Anak"
selesai
```

## Tipe Data Awal

- integer
- float
- string
- boolean
- list
- dictionary
- null melalui `kosong`
- function untuk fungsi bawaan

## Fungsi Standar Awal

`panjang`, `acak`, `huruf_besar`, `huruf_kecil`, `gabung`, `pisah`, `tunggu`, `waktu`,
`tanggal`, `buka`, `tulis_berkas`, `hapus`, dan `buat_folder`.


```bash
python -m aksara.cli.main jalankan examples/halo.aks
python -m aksara.cli.main jalankan halo.aks
python -m aksara.cli.main jalankan
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
