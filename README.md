# Tugas 5 — Sistem Pakar Sederhana: Kualitas Air Kolam Lele

## 1. Identitas
- Nama: Kamrun Syah Syahidu
- NIM: F1D02410011
- Mata kuliah: Kecerdasan Buatan (MKL1303131), Teknik Informatika UNRAM

## 2. Topik dan cara menjalankan
Topik: diagnosis masalah kualitas air kolam budidaya lele (suhu, pH, oksigen terlarut, amonia, nitrit).

- Bahasa: Python 3 (diuji dengan Python 3.10+), tanpa library tambahan.
- File: `main.py` (mesin), `kb_lele.json` (basis aturan).
- Perintah (jalankan dari folder repository):

```
python main.py
```

Jawab pertanyaan dengan `y` atau `t`.

## 3. Sumber dan aturan

Tanggal akses kedua sumber: 9 November 2026.

| Kode | Sumber |
|---|---|
| S1 | Haliyani (2020). *Performansi Kinerja Budidaya Pembesaran Ikan Lele Sangkuriang (Clarias gariepinus) di CV. Dampo Awang, Kecamatan Jatinangor, Kabupaten Sumedang, Jawa Barat.* Buletin Jalanidhitah Sarva Jivitam 2(1):1-11. Politeknik Ahli Usaha Perikanan (KKP). https://ejournal-balitbang.kkp.go.id/index.php/JSJ/article/download/8445/7400 |
| S2 | Pujiharsono, H. & Kurnianto, D. (2020). *Sistem inferensi fuzzy Mamdani untuk menentukan tingkat kualitas air pada kolam bioflok dalam budidaya ikan lele.* Jurnal Teknologi dan Sistem Komputer 8(2):84-88. DOI 10.14710/jtsiskom.8.2.2020.84-88. https://jtsiskom.undip.ac.id/article/download/13209/12555 |

Aturan ditulis dengan kata-kata sendiri (parafrasa), bukan kutipan.

| Aturan | IF | THEN | Sumber |
|---|---|---|---|
| R1 | suhu < 25 °C **OR** suhu > 30 °C | suhu tidak layak | S1, S2 |
| R2 | pH < 6,5 **OR** pH > 8,5 | pH tidak layak | S2 |
| R3 | DO < 3 mg/L | oksigen rendah | S1 |
| R4 | air kolam pekat **OR** sisa pakan menumpuk | amonia berpotensi tinggi | S1 |
| R5 | oksigen rendah **AND** amonia berpotensi tinggi | limbah beracun menumpuk | S1, S2 |
| R6 | nitrit > 0,05 mg/L | nitrit melebihi ambang batas | S1 |
| R7 | suhu berubah-ubah drastis **AND** tubuh ikan berdarah | infeksi bakteri akibat suhu tidak stabil | S1 |
| R8 | suhu tidak layak **OR** pH tidak layak **OR** oksigen rendah | kondisi air tidak layak | S2 |
| R9 | kondisi air tidak layak **AND** nafsu makan ikan menurun | ikan stres dan pertumbuhan terhambat | S2 |
| R10 | limbah beracun menumpuk **AND** ikan stres dan pertumbuhan terhambat | risiko kematian ikan tinggi | S1, S2 |

Aturan yang memakai hasil aturan lain: R5 (dari R3 dan R4), R8 (dari R1/R2/R3), R9 (dari R8), R10 (dari R5 dan R9).

Catatan perbedaan sumber: S2 menyebut pH normal 6,5–8,5 sehingga dipakai di R2 (S1 menyebut rentang yang lebih longgar, 6–9). Untuk oksigen, S1 mengutip batas minimal 3 mg/L (R3), sedangkan S2 memakai batas lebih rendah (> 1,7 mg/L) untuk benih di kolam bioflok. Batas S1 dipilih karena lebih berhati-hati.

## 4. Metode: Forward Chaining
Forward chaining dipilih karena data di lapangan berupa pengamatan (fakta) yang lalu dicari kesimpulannya. Cocok untuk diagnosis berantai: hasil satu aturan (misalnya "oksigen rendah") menjadi syarat aturan berikutnya.

Langkah:
1. Fakta yang tidak pernah menjadi hasil aturan manapun ditanyakan ke user; jawaban "y" masuk ke memori.
2. Cari aturan yang syaratnya terpenuhi (mode `dan` = semua, `atau` = salah satu) dan hasilnya belum ada di memori.
3. Jalankan aturan pertama yang cocok, tambahkan hasilnya ke memori, catat aturan asalnya.
4. Ulangi sampai tidak ada aturan baru.
5. Kesimpulan akhir = hasil yang tidak dipakai sebagai syarat aturan lain. Alasan ditelusuri mundur dari catatan aturan asal.

Aturan yang hasilnya sudah ada di memori tidak dijalankan lagi supaya program berhenti.

## 5. Tiga kasus uji

| # | Jawaban "ya" | Kesimpulan |
|---|---|---|
| 1 | DO < 3 mg/L, air pekat, nafsu makan menurun | risiko kematian ikan tinggi |
| 2 | nafsu makan menurun saja | tidak ada (kasus negatif) |
| 3 | nitrit > 0,05, suhu berubah-ubah, ikan berdarah | nitrit melebihi ambang batas; infeksi bakteri akibat suhu tidak stabil |

### Kasus 1
```
Fakta awal: oksigen terlarut di bawah 3 mg/L, air kolam berwarna pekat, nafsu makan ikan menurun
Siklus 1: R3 -> oksigen rendah
Siklus 2: R4 -> amonia berpotensi tinggi
Siklus 3: R5 -> limbah beracun menumpuk
Siklus 4: R8 -> kondisi air tidak layak
Siklus 5: R9 -> ikan stres dan pertumbuhan terhambat
Siklus 6: R10 -> risiko kematian ikan tinggi
Siklus 7: tidak ada aturan baru, berhenti

Kesimpulan: risiko kematian ikan tinggi
Alasan:
  risiko kematian ikan tinggi <- R10 (limbah beracun menumpuk, ikan stres dan pertumbuhan terhambat) [sumber: S1, S2]
  limbah beracun menumpuk <- R5 (oksigen rendah, amonia berpotensi tinggi) [sumber: S1, S2]
  oksigen rendah <- R3 (oksigen terlarut di bawah 3 mg/L) [sumber: S1]
  amonia berpotensi tinggi <- R4 (air kolam berwarna pekat) [sumber: S1]
  ikan stres dan pertumbuhan terhambat <- R9 (kondisi air tidak layak, nafsu makan ikan menurun) [sumber: S2]
  kondisi air tidak layak <- R8 (oksigen rendah) [sumber: S2]
```
![Kasus 1](screenshot/kasus1.png)

### Kasus 2 (negatif)
```
Fakta awal: nafsu makan ikan menurun
Siklus 1: tidak ada aturan baru, berhenti

Kesimpulan: tidak ada kesimpulan dari fakta yang diberikan.
```
![Kasus 2](screenshot/kasus2.png)

### Kasus 3
```
Fakta awal: nitrit di atas 0,05 mg/L, suhu air berubah-ubah drastis, tubuh ikan berdarah
Siklus 1: R6 -> nitrit melebihi ambang batas
Siklus 2: R7 -> infeksi bakteri akibat suhu tidak stabil
Siklus 3: tidak ada aturan baru, berhenti

Kesimpulan: nitrit melebihi ambang batas; infeksi bakteri akibat suhu tidak stabil
Alasan:
  nitrit melebihi ambang batas <- R6 (nitrit di atas 0,05 mg/L) [sumber: S1]
  infeksi bakteri akibat suhu tidak stabil <- R7 (suhu air berubah-ubah drastis, tubuh ikan berdarah) [sumber: S1]
```
![Kasus 3](screenshot/kasus3.png)

## 6. Batas keberlakuan
Pengetahuan dalam program ini berasal dari dua artikel jurnal: satu pengamatan di sebuah unit budidaya lele sangkuriang di Jatinangor (kolam bundar) dan satu penelitian pada kolam bioflok. Ambang batas dalam literatur berbeda antar penulis dan antar jenis kolam, sehingga aturan ini hanya cocok sebagai panduan awal untuk pembudidaya lele skala kecil-menengah. Hasil program adalah saran, bukan keputusan akhir; ukur ulang parameter air dan konsultasikan dengan penyuluh perikanan sebelum bertindak. Catatan yang sama ditampilkan di akhir keluaran program.

## 7. Penggunaan alat bantu AI
Claude (Anthropic) dipakai untuk membantu mencari sumber, menyusun draf aturan, kode, dan README. Aturan, kode, dan hasil uji sudah saya baca, jalankan, dan pahami sendiri.