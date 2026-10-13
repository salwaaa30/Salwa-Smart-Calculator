# Salwa Smart Calculator

Aplikasi kalkulator desktop Windows dengan Python dan Tkinter. Runtime hanya menggunakan pustaka standar Python; PyInstaller dipakai saat membuat executable portable.

## Fitur

- Penjumlahan, pengurangan, perkalian, pembagian, persen, akar kuadrat, dan pangkat.
- Prioritas operator standar dan tanda kurung.
- Input dari keypad aplikasi atau keyboard fisik.
- Riwayat hingga 10 perhitungan terakhir dalam sesi aktif.
- Mode gelap/terang, jendela resizable, serta pesan kesalahan yang ramah.
- Evaluasi ekspresi terbatas; kode Python arbitrer tidak dieksekusi.

## Menjalankan dari sumber

Gunakan Python 3.8 atau yang lebih baru:

```powershell
python app.py
```

Jalankan tes:

```powershell
python -m unittest discover -s tests -v
```

## Build executable Windows

Jalankan `build_windows.bat` dari Windows dengan Python terpasang dan koneksi internet untuk mengunduh PyInstaller. Hasilnya akan berada di `dist\Salwa Smart Calculator.exe` dan dapat dijalankan tanpa instalasi Python pada perangkat pengguna.

Executable Windows harus dibangun di Windows. Uji di perangkat Windows bersih tetap diperlukan sebelum distribusi final.