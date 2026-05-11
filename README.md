# Tahfidz Overlay & Quran Reader

Aplikasi overlay Quran profesional yang dirancang khusus untuk kebutuhan siaran langsung (OBS), presentasi, atau alat bantu setoran tahfidz. Mendukung database lengkap 114 surah dengan sinkronisasi real-time.

## 🚀 Fitur Unggulan

- **Database Quran Lengkap**: Akses instan ke 114 surah beserta terjemahan Bahasa Indonesia.
- **Sinkronisasi Real-Time**: Panel kontrol dan tampilan overlay terhubung secara otomatis via server lokal.
- **Sistem Pemotong Ayat Pintar**: Membagi ayat yang sangat panjang menjadi beberapa bagian agar tetap terbaca jelas di layar.
- **Kustomisasi Layout Penuh**: 
  - Pengaturan ukuran font (Ayat, Surah, Terjemahan).
  - Pengaturan lebar kontainer, padding, dan tinggi baris.
  - Posisi teks fleksibel (Kanan, Tengah, Kiri, Atas, Bawah).
- **Smart Search**: Cari surah berdasarkan nama, nomor, atau format cepat `surah:ayat` (contoh: `114:1`).
- **Mode Persistence**: Aplikasi mengingat ayat terakhir dan pengaturan tampilan yang Anda gunakan.
- **Aesthetic Design**: Tampilan premium dengan font **LPMQ Isep Misbah** (Standar Kemenag RI), efek blur (glassmorphism), dan transisi halus.

## ⌨️ Kontrol & Shortcut

Aplikasi ini dioptimalkan untuk navigasi cepat menggunakan keyboard:

| Tombol | Fungsi |
| :--- | :--- |
| **Spasi** | Menampilkan Ayat Acak (*Random*) |
| **Panah Kanan** | Lanjut ke Ayat berikutnya |
| **Panah Kiri** | Kembali ke Ayat sebelumnya |
| **Panah Bawah** | Lanjut ke bagian berikutnya (jika ayat terpotong) |
| **Panah Atas** | Kembali ke bagian sebelumnya (jika ayat terpotong) |
| **Escape (Esc)** | Menyembunyikan tampilan overlay |
| **Klik Overlay** | Sama dengan menekan tombol Panah Bawah |
| **Floating Nav** | (Mobile Only) Selalu tampil di pojok kanan bawah |

## 🛠️ Cara Instalasi & Penggunaan

### 1. Jalankan Server
Buka terminal di direktori proyek dan jalankan server sinkronisasi:
```bash
python3 server.py
```

### 2. Buka Control Panel
Akses melalui browser di:
`http://localhost:8000`
*Tip: Panel kontrol disembunyikan secara otomatis. Arahkan kursor ke **pojok kiri atas** untuk memunculkan menu.*

### 3. Tambahkan ke OBS
1. Tambahkan Source baru tipe **Browser**.
2. Masukkan URL: `http://localhost:8000`
3. Atur lebar dan tinggi sesuai resolusi OBS Anda (contoh: 1920x1080).

## 📂 Struktur Data
Aplikasi menggunakan database JSON yang efisien:
- `/quran-json/surah/`: File data per-surah (1-114).
- `/data/surah_list.json`: Daftar nama dan metadata surah.
- `/fonts/`: Font Arab premium (LPMQ Isep Misbah & Amiri).

---
*Dikembangkan untuk kemudahan belajar dan syiar Al-Quran.*