<div align="center">

# 🤖 Arcia AI 🤖

### Asisten Pribadi Cerdas Berbasis Teks dan Suara

Sebuah asisten virtual berbasis Python yang dirancang untuk membantu Anda melakukan tugas-tugas di komputer melalui perintah suara dan teks.

![Garis Pemisah](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

</div>

Arcia AI adalah kerangka dasar yang mudah dipahami, baik bagi pengguna awam yang ingin mencoba asisten virtual, maupun bagi programmer yang ingin mengembangkannya lebih jauh.

---

## ✨ Fitur Utama

- **🎙️ Interaksi Ganda**: Mendukung perintah melalui **suara** (voice mode) dan **ketikan teks** (text mode).
- **🚀 Peluncur Aplikasi**: Membuka aplikasi favorit Anda dengan cepat langsung dari perintah suara atau teks.
- **🌐 Navigasi Web**: Membuka situs web apa pun hanya dengan menyebutkan alamatnya.
- **🎬 Pemutar YouTube**: Mencari dan memutar video dari YouTube, dengan opsi filter berdasarkan channel.
- **🖥️ Monitor Sistem**: Memberikan laporan singkat mengenai penggunaan CPU, RAM, dan Disk komputer Anda.
- **⌨️ Pintasan Cepat (Hotkey)**: Beralih mode dengan mudah menggunakan `Ctrl+Shift+T` (teks) dan `Ctrl+Shift+O` (suara).

---

## ⚙️ Instalasi & Konfigurasi (Wajib Dibaca)

Untuk menjalankan Arcia, ikuti tiga langkah mudah berikut.

### Langkah 1: Instalasi Dependensi

Proyek ini memerlukan beberapa library Python untuk berjalan. Karena file `requirements.txt` sudah tersedia, Anda cukup menjalankan satu perintah ini di terminal atau CMD pada folder proyek Anda:

```bash
pip install -r requirements.txt
```

### Langkah 2: Buat File Konfigurasi Aplikasi (`config.json`)

Arcia perlu tahu di mana lokasi aplikasi yang ingin Anda buka. Anda harus membuat file ini secara manual.

1.  Buat file baru di folder proyek Anda bernama **`config.json`**.
2.  Salin dan tempel kode di bawah ini ke dalamnya.
3.  **SESUAIKAN PATH** agar cocok dengan lokasi aplikasi di komputer Anda. Klik kanan ikon aplikasi > Properties > salin path dari kolom "Target".

```json
{
  "app_paths": {
    "notepad": "C:\\Windows\\System32\\notepad.exe",
    "calculator": "C:\\Windows\\System32\\calc.exe",
    "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "steam": "C:\\Program Files (x86)\\Steam\\steam.exe"
  }
}
```

### Langkah 3: Buat File API Key (`.env`)

Untuk fitur pencarian YouTube, Anda memerlukan API Key dari Google Console. Simpan kunci ini dengan aman.

1.  Buat file baru di folder proyek Anda bernama **`.env`**. (Pastikan namanya hanya `.env`, tanpa nama di depannya).
2.  Salin dan tempel teks di bawah ini ke dalamnya, lalu ganti `MASUKKAN_API_KEY_ANDA_DI_SINI` dengan API Key yang Anda dapatkan dari Google Console.

```
YOUTUBE_API_KEY="MASUKKAN_API_KEY_ANDA_DI_SINI"
```

---

## 🚀 Cara Menggunakan

Setelah ketiga langkah di atas selesai, Anda siap menggunakan Arcia.

1.  **Jalankan Program**
    - Buka Terminal atau CMD di folder proyek dan jalankan:
      ```bash
      python V1.py
      ```

2.  **Berikan Perintah**
    - Arcia akan mulai dalam mode suara. Cukup ucapkan perintah Anda.
    - Gunakan hotkey `Ctrl+Shift+T` (teks) atau `Ctrl+Shift+O` (suara) untuk beralih mode.

---

## ✍️ Tips Mengedit di VS Code

- Gunakan `Ctrl+Shift+V` untuk membuka panel **preview** berdampingan. Anda bisa menulis di kiri dan melihat hasilnya secara langsung di kanan.
- Instal ekstensi **"Markdown All in One"** untuk fitur tambahan seperti membuat daftar isi otomatis dan *shortcut* keyboard.

<div align="center">

![Garis Pemisah](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

### 📜 Lisensi: MIT License

</div>
