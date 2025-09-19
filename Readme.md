<div align="center">

# 🤖 Arcia AI 🤖

### Asisten Pribadi Cerdas Berbasis Teks dan Suara

![Garis Pemisah](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

</div>

Arcia AI adalah sebuah asisten virtual berbasis Python yang dirancang untuk membantu Anda melakukan tugas-tugas di komputer melalui perintah suara dan teks. Proyek ini bertujuan untuk menjadi kerangka dasar yang mudah dipahami dan dikembangkan lebih lanjut.

---

## ✨ Fitur Utama

- **🎙️ Interaksi Ganda**: Mendukung perintah melalui **suara** (voice mode) dan **ketikan teks** (text mode).

- **🚀 Peluncur Aplikasi**: Membuka aplikasi favorit Anda dengan cepat langsung dari perintah suara atau teks.

- **🌐 Navigasi Web**: Membuka situs web apa pun hanya dengan menyebutkan alamatnya.

- **🎬 Pemutar YouTube**: Mencari dan memutar video dari YouTube, dengan opsi filter berdasarkan channel.

- **🖥️ Monitor Sistem**: Memberikan laporan singkat mengenai penggunaan CPU, RAM, dan Disk komputer Anda.

- **⌨️ Pintasan Cepat (Hotkey)**: Beralih mode dengan mudah menggunakan `Ctrl+Shift+T` (teks) dan `Ctrl+Shift+O` (suara).

---

## ⚙️ Instalasi & Konfigurasi

Untuk menjalankan Arcia, ikuti langkah-langkah berikut. Proses ini hanya perlu dilakukan sekali.

1.  **Persiapan Awal**
    - Pastikan **Python 3.6+** sudah terinstal di komputer Anda.
    - Unduh atau *clone* proyek ini ke komputer Anda.

2.  **Instalasi Dependensi**
    - Buat file bernama `requirements.txt` dan isi dengan teks di bawah ini:
      ```
      google-api-python-client
      psutil
      keyboard
      SpeechRecognition
      PyAudio
      python-dotenv
      ```
    - Buka Terminal atau CMD di folder proyek, lalu jalankan perintah:
      ```bash
      pip install -r requirements.txt
      ```

3.  **Konfigurasi API Key (Wajib)**
    - Buat file baru bernama `.env` di folder proyek.
    - Isi file tersebut dengan format berikut untuk menyimpan API Key YouTube Anda secara aman:
      ```
      YOUTUBE_API_KEY="MASUKKAN_API_KEY_ANDA_DI_SINI"
      ```

4.  **Konfigurasi Path Aplikasi (Wajib)**
    - Buat file baru bernama `config.json`.
    - Sesuaikan path aplikasi sesuai dengan lokasi instalasi di komputer Anda. Ini membuat Arcia tahu di mana harus mencari aplikasi.
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

---

## 🚀 Cara Menggunakan

Setelah instalasi dan konfigurasi selesai, Anda siap menggunakan Arcia.

1.  **Jalankan Program**
    - Buka Terminal atau CMD di folder proyek dan jalankan:
      ```bash
      python V1.py
      ```

2.  **Berikan Perintah**
    - Arcia akan mulai dalam mode suara. Cukup ucapkan perintah Anda.
    - Untuk beralih mode, gunakan hotkey atau berikan perintah suara/teks ("mode teks" atau "mode suara").

3.  **Daftar Perintah yang Tersedia**
    > - `Buka aplikasi [nama aplikasi]`
    > - `Buka website https://en.wikipedia.org/wiki/Website`
    > - `Mainkan video [judul video] di YouTube`
    > - `Mainkan video [judul video] dari channel [nama channel] di youtube`
    > - `Pantau sistem`
    > - `Bantuan`
    > - `Keluar`

---

## 👨‍💻 Panduan untuk Pengembang

Bagian ini menjelaskan rekomendasi perubahan pada kode `V1.py` agar lebih aman dan portabel.

### 1. Keamanan: Pindahkan API Key dari Kode

> **Alasan**: Menyimpan API Key langsung di dalam kode sangat berisiko. Gunakan file `.env` untuk memisahkannya.

- **Sebelum Diubah (di `V1.py`)**:
  ```python
  API_KEY = "AIzaSyD8vjBett9APr_xbNbj24b8sunZ8I2RpSg"
  ```

- **Sesudah Diubah (di `V1.py`)**:
  ```python
  import os
  from dotenv import load_dotenv
  
  load_dotenv()
  API_KEY = os.getenv("YOUTUBE_API_KEY")
  ```

### 2. Portabilitas: Pindahkan Path Aplikasi ke `config.json`

> **Alasan**: Memudahkan pengguna lain untuk menyesuaikan path aplikasi tanpa harus mengedit file Python utama.

- **Sebelum Diubah (di `V1.py`)**:
  ```python
  app_paths = {
      "notepad": "C:\\Windows\\System32\\notepad.exe",
      # ...dan seterusnya
  }
  ```

- **Sesudah Diubah (di `V1.py`)**:
  ```python
  import json

  # Di dalam method __init__
  self.app_paths = self.load_config().get("app_paths", {})

  # Method baru untuk memuat konfigurasi
  def load_config(self):
      try:
          with open('config.json', 'r') as f:
              return json.load(f)
      except FileNotFoundError:
          return {}
  ```
