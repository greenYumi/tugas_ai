
# Chess voice controller

program ini adalah tugas akademik, berkelompok.

Mengimplementasikan model STT (speech-to-text) VOSK ke dalam program permainan catur. Fokus utamanya adalah menggerakan bidak catur menggunakan suara.

grafik menggunakan basis teks (terminal)

#### _cara kerja_
---
menggunakan model vosk untuk mengenal suara dan mengubah menjadi teks, teks disaring menggukan engine KaldiRecognizer untuk menghasilan kata yang paling mendekati dari set yang telah ditentukan. Hasil teks akan diproses ke dalam program game untuk menggerakan bidak secara logikal.

#### _cara pakai_
---
clone semua file di repo, jalankan `chess.py` demo akan berjalan, pada saat itu mikrofon akan terus aktif menangkap suara.

menggerakan pion cukup mudah. Ucapkan tiles dimana bidak akan bergerak. 

Game diprogram menggunakan gerakan logika dimana untuk menggerakan bidak cukup sebutkan lokasi tile yang ingin dituju tanpa menyebutkan nama bidak.

_cth_, menyebutkan "c4", dengan maksud menggerakan bidak knight ke tile c4, maka jika memang pada saat itu hanya knight yang bisa bergeraka ke tile c4, knight akan bergerak ke tile yang dimaksud secara otomatis, jika terdapat lebih dari 1 bidak yang dapat ke tile yang dimaksud game akan menanyakan bidak mana yang akan digerakan.

untuk lebih spesifik, sebutkan nama bidak dan tile,
"knight", "c4"

---
(**_program masih dalam tahap pengembangan_**)
