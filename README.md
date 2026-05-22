# CipherLab

Aplikasi web untuk mensimulasikan dan memvisualisasikan algoritma kriptografi klasik:
Caesar, Vigenère, Affine, Hill, dan Playfair.

Proyek ini dibuat untuk kebutuhan pembelajaran, sehingga hasil enkripsi/dekripsi tidak hanya ditampilkan sebagai output akhir, tetapi juga disertai langkah-langkah proses yang dikirim dari server.

## Fitur

- Enkripsi dan dekripsi untuk 5 algoritma klasik
- Langkah per langkah dari server (`steps`) untuk keperluan edukasi
- Riwayat operasi disimpan di sisi server dan dapat dibersihkan
- Visualisasi matriks untuk Hill Cipher
- Visualisasi tabel Playfair
- Mode terang/gelap dan tampilan responsif
- Validasi input penting, termasuk shift Caesar 1–25

## Demo

Tambahkan screenshot atau tautan demo di sini setelah aplikasi dideploy.

Contoh:

- Live demo: `https://...`
- Screenshot utama: `docs/screenshot-home.png`

## Teknologi

- Python
- Flask
- Jinja2
- HTML, CSS, JavaScript

## Struktur Proyek

```text
app/
	algorithms/     # implementasi Caesar, Vigenere, Affine, Hill, Playfair
	models/         # model data
	routes/         # halaman dan API routes
	services/       # layanan riwayat
	static/         # aset statis
	templates/      # template HTML
	utils/          # helper dan validator
instance/         # penyimpanan riwayat server-side
run.py            # entry point aplikasi
requirements.txt  # dependency Python
```

## Instalasi

### 1. Buat virtual environment

```bash
python -m venv venv
```

### 2. Aktifkan virtual environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Command Prompt:

```bat
venv\Scripts\activate.bat
```

### 3. Install dependency

```bash
pip install -r requirements.txt
```

### 4. Jalankan aplikasi

```bash
python run.py
```

Lalu buka:

```text
http://127.0.0.1:5000/kalkulator
```

## Cara Pakai

1. Pilih algoritma yang ingin dicoba.
2. Isi input teks dan parameter yang dibutuhkan.
3. Klik tombol enkripsi atau dekripsi.
4. Lihat hasil akhir, langkah proses, dan visualisasi pendukung.
5. Riwayat hasil akan tersimpan otomatis di server.



## Catatan Penting

- Caesar hanya menerima shift 1–25.
- Hill Cipher 6x6 lebih berat secara komputasi, jadi UI menampilkan peringatan saat dipilih.
- Riwayat disimpan di `instance/history.json`, bukan di browser.
- Langkah edukasi diambil dari server, sehingga frontend dan backend tetap konsisten.

## Pengembangan Berikutnya

- Menambahkan unit test untuk semua algoritma
- Menambahkan screenshot dan demo live setelah deployment
- Menyempurnakan visualisasi langkah agar lebih interaktif
- Menambahkan pagination atau filter pada riwayat jika data makin banyak

## Lisensi

Gunakan sesuai kebutuhan tugas atau pengembangan pribadi. Jika ingin, saya juga bisa bantu menambahkan bagian lisensi resmi seperti MIT.
