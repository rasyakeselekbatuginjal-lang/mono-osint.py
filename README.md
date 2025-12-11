# mono-osint.py

# 🕵️ Mono OSINT - Ultimate Edition

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Status](https://img.shields.io/badge/Status-Active-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-orange?style=for-the-badge)

**Mono Ultimate** adalah alat *Open Source Intelligence* (OSINT) all-in-one yang dirancang untuk melakukan investigasi digital secara mendalam. Tools ini menggabungkan pencarian username, pelacakan identitas asli (Real Name), dan analisis nomor telepon dalam satu antarmuka CLI yang modern.

> *"Tools ini dibuat untuk mempermudah security researcher dalam melakukan reconnaissance."*

## 🔥 Fitur Revolusioner (v4.0)

| Fitur | Deskripsi |
| :--- | :--- |
| **👤 Username Profiler** | Melacak ketersediaan akun di **120+ situs** (Sosmed, Coding, Gaming, Dewasa) dengan sistem *Multi-threading* super cepat. |
| **🧬 Real Name DNA** | **[BARU]** Melacak jejak digital berdasarkan **Nama Lengkap**. Mencari kebocoran CV (PDF), Skripsi, Data Kampus, dan LinkedIn secara spesifik. |
| **📱 Phone Tracker** | **[BARU]** Melacak informasi Nomor HP (Provider, Negara, Timezone) dan mendeteksi akun WhatsApp/Telegram tanpa koneksi internet (Offline Database). |
| **🔍 Dorking Arsenal** | Generator otomatis Google Dork untuk mencari password bocor, file konfigurasi, database, dan kamera CCTV. |
| **🌍 IP & Domain Recon** | Melacak lokasi geografis (GeoIP), ISP, dan koordinat peta dari target IP Address. |
| **📄 Auto Report** | Hasil scan otomatis tersimpan dalam format `.txt` yang rapi untuk dokumentasi. |

## 🛠️ Instalasi

Pastikan kamu sudah menginstall **Python 3** dan **Git**.

1.  **Clone repository ini:**
    ```bash
    git clone [https://github.com/rasyakeselekbatuginjal-lang/mono-osint.py.git](https://github.com/rasyakeselekbatuginjal-lang/mono-osint.py.git)
    cd mono-osint.py
    ```

2.  **Install library wajib:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Library yang dibutuhkan: `requests`, `rich`, `phonenumbers`)*

## 🚀 Cara Penggunaan

Jalankan script utama menggunakan Python:

```bash
python mono.py
