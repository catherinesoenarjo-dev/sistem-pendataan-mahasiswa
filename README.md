
# Sistem Pencatatan dan Manajemen Data Mahasiswa (Python)

Aplikasi berbasis terminal (CLI) sederhana yang ditulis dalam bahasa pemrograman Python untuk mengelola data akademik mahasiswa, mencakup pencatatan biodata, sistem presensi otomatis, penghitungan nilai akhir, hingga penyimpanan data ke file CSV.

## Fitur Utama

* **Tambah Mahasiswa**: Menambah dan menyimpan data mahasiswa (NIM dan Nama) dengan validasi NIM unik.
* **Sistem Presensi**:
  - Mencatat kehadiran per pertemuan.
  - Otomatisasi sesi pertemuan: Pertemuan Ganjil untuk **Sesi Teori** dan Pertemuan Genap untuk **Sesi Praktikum**.
  - Penghitungan persentase kehadiran secara otomatis.


* **Sistem Penilaian**:
  - Input nilai Tugas, UTS, dan UAS.
  - Penghitungan Nilai Akhir dengan bobot: Tugas (30%), UTS (35%), dan UAS (35%).
  - Konversi otomatis Nilai Akhir ke Grade (A, B, C, D, E).


* **Penyimpanan Data (CSV)**:
  - Menyimpan data ke file `.csv` dengan delimiter kustom (`;`).
  - Fitur load data otomatis saat program dijalankan kembali.



## Persyaratan Sistem

* **Python 3.6+**
* Library bawaan Python: `csv`, `pathlib`.

## Struktur Data CSV

Data disimpan dalam format CSV dengan struktur kolom sebagai berikut:
`NIM;Nama;Tugas;UTS;UAS;NilaiAkhir;Grade;KehadiranPersen;Presensi`

Kolom `Presensi` menyimpan histori kehadiran dalam format *key-value* (Contoh: `1:Hadir|2:Alpha`).

## Cara Penggunaan

1. **Clone Repositori**:
```bash
git clone https://github.com/username-anda/nama-repo.git
cd nama-repo

```


2. **Penyesuaian Jalur File (Opsional)**:
Buka file `pendataan_mahasiswa2.py` dan sesuaikan variabel `FILE_PATH` jika ingin mengubah lokasi penyimpanan file CSV:
```python
FILE_PATH = Path("C:\\Jalur\\Folder\\Anda\\data_mahasiswa.csv")

```


3. **Jalankan Aplikasi**:
```bash
python pendataan_mahasiswa2.py

```


4. **Menu**:
* `1`: Tambah Mahasiswa baru.
* `2`: Input Presensi Mahasiswa.
* `3`: Input Nilai akademik.
* `4`: Tampilkan Data Mahasiswa.
* `5`: Simpan Data.
* `6`: Keluar dari program.



## Aturan Penilaian

Aplikasi menggunakan logika grade sebagai berikut:

| Rentang Nilai | Grade |
| --- | --- |
| >= 85 | A |
| >= 70 | B |
| >= 55 | C |
| >= 40 | D |
| < 40 | E |

---

