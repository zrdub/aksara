# AKSARA

AKSARA adalah bahasa pemrograman interpreted modern dengan kata kunci berbahasa
Indonesia. Implementasi awal ini menyediakan lexer, parser, AST, runtime,
interpreter, standard library, CLI, contoh program, dokumentasi, dan pengujian.

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
