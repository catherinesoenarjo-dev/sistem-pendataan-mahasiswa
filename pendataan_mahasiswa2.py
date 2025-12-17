import csv
from pathlib import Path

FILE_PATH = Path("C:\\Users\\Asus\\OneDrive\\Desktop\\data_mahasiswa\\data_mahasiswa.csv")

CSV_DELIM = ";"
PRESENSI_DELIM = "|"


def format_angka(x: float) -> str:
    x = float(x)
    return str(int(x)) if x.is_integer() else f"{x:.2f}"


class Mahasiswa:
    def __init__(self, nim, nama, tugas=None, uts=None, uas=None):
        self.nim = str(nim).strip()
        self.nama = str(nama).strip()
        self.tugas = tugas
        self.uts = uts
        self.uas = uas
        self.presensi = {}

    def __str__(self):
        return f"NIM: {self.nim}, Nama: {self.nama}"

    # PRESENSI 
    def input_presensi(self, n: int, status: str):
        status = status.strip().capitalize()
        if status not in ["Hadir", "Alpha", "Izin"]:
            raise ValueError("Status harus 'Hadir', 'Alpha', atau 'Izin'.")
        self.presensi[int(n)] = status

    def hitung_presensi(self) -> float:
        hitung_persen = (
            lambda pres: (sum(1 for s in pres.values() if s == "Hadir")
                          / len(pres) * 100) if pres else 0
        )
        return float(hitung_persen(self.presensi))

    # NILAI 
    def input_nilai(self,tugas: int, uts: int, uas: int):
        if not (0 <= tugas <= 100 and 0 <= uts <= 100 and 0 <= uas <= 100):
            raise ValueError("Nilai harus berada dalam rentang 0-100")
            
        self.tugas = int(tugas)
        self.uts = int(uts)
        self.uas = int(uas)

    def hitung_nilai(self) -> float:
        if None in (self.tugas, self.uts, self.uas):
            return 0.0
        nilai_total = lambda a, b, c: (a * 0.30) + (b * 0.35) + (c * 0.35)
        return round(float(nilai_total(self.tugas, self.uts, self.uas)), 2)

    def grade(self) -> str:
        nilai = self.hitung_nilai()
        if nilai >= 85:
            return "A"
        elif nilai >= 70:
            return "B"
        elif nilai >= 55:
            return "C"
        elif nilai >= 40:
            return "D"
        else:
            return "E"


class ManajemenDataMahasiswa:
    def __init__(self):
        self.data_mahasiswa = []

    # DATA MAHASISWA
    def tambah_mahasiswa(self, nim, nama):
        nim = str(nim).strip()
        nama = str(nama).strip()

        if self.cari_mahasiswa(nim) is not None:
            raise ValueError("NIM sudah terdaftar. Masukkan NIM yang berbeda.")
    
        mahasiswa_baru = Mahasiswa(nim, nama)
        self.data_mahasiswa.append(mahasiswa_baru)
        print(f"Data Mahasiswa {nama} (NIM: {nim}) berhasil ditambahkan")

    def cari_mahasiswa(self, nim: str):
        nim = str(nim).strip()
        for mhs in self.data_mahasiswa:
            if mhs.nim == nim:
                return mhs
        return None

    # NILAI SISTEM
    def input_nilai_sistem(self, nim: str, tugas: int, uts: int, uas: int):
        mhs = self.cari_mahasiswa(nim)
        if not mhs:
            print("Mahasiswa dengan NIM ini tidak ditemukan")
            return
        try:
            mhs.input_nilai(tugas, uts, uas)
            print(f"Nilai akademik berhasil diinput untuk {mhs.nama} (NIM: {mhs.nim})")
        except ValueError as ve:
            raise ve

    # PRESENSI SISTEM
    def input_presensi_sistem(self, n: int):
        if not self.data_mahasiswa:
            print("Belum ada data mahasiswa.")
            return

        n = int(n)
        sesi = "Sesi Teori" if n % 2 != 0 else "Sesi Praktikum"
        print(f"Pertemuan ke-{n} adalah {sesi}")
        print("Masukkan status kehadiran: Hadir / Alpha / Izin")

        for mhs in self.data_mahasiswa:
            while True:
                status = input(
                    f"Masukkan status kehadiran untuk {mhs.nama} (Hadir/Alpha/Izin): "
                ).strip()
                try:
                    mhs.input_presensi(n, status)
                    break
                except ValueError as ve:
                    print(ve)

    # TAMPIL DATA DI TERMINAL
    def tampil_data_mahasiswa(self):
        if not self.data_mahasiswa:
            print("Belum ada data mahasiswa.")
            return

        print(f"{'NIM':<15}{'Nama':<20}{'Tugas':<7}{'UTS':<7}{'UAS':<7}"
              f"{'Nilai Akhir':<12}{'Grade':<7}{'Kehadiran (%)':<15}")

        for mhs in self.data_mahasiswa:
            tugas = mhs.tugas if mhs.tugas is not None else "-"
            uts = mhs.uts if mhs.uts is not None else "-"
            uas = mhs.uas if mhs.uas is not None else "-"

            nilai_akhir = (
                format_angka(mhs.hitung_nilai())
                if None not in (mhs.tugas, mhs.uts, mhs.uas) else "-"
            )
            grade = (
                mhs.grade()
                if None not in (mhs.tugas, mhs.uts, mhs.uas) else "-"
            )
            kehadiran = (
                f"{format_angka(mhs.hitung_presensi())}%"
                if mhs.presensi else "-"
            )

            print(f"{mhs.nim:<15}{mhs.nama:<20}{tugas:<7}{uts:<7}{uas:<7}"
                  f"{nilai_akhir:<12}{grade:<7}{kehadiran:<15}")

    # SAVE DATA
    def simpan_data(self, filename: Path = FILE_PATH):
        filename = Path(filename)
        filename.parent.mkdir(parents=True, exist_ok=True)

        with open(filename, mode="w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(
                file,
                delimiter=CSV_DELIM,
                quoting=csv.QUOTE_MINIMAL
            )

            writer.writerow([
                "NIM", "Nama", "Tugas", "UTS", "UAS",
                "NilaiAkhir", "Grade", "KehadiranPersen", "Presensi"
            ])

            for mhs in self.data_mahasiswa:
                nilai_akhir = mhs.hitung_nilai()
                grade = mhs.grade()
                kehadiran_persen = mhs.hitung_presensi()

                nilai_akhir_str = format_angka(nilai_akhir)
                kehadiran_str = format_angka(kehadiran_persen) 

                presensi_str = PRESENSI_DELIM.join(
                    f"{k}:{v}" for k, v in sorted(mhs.presensi.items())
                )

                writer.writerow([
                    mhs.nim,
                    mhs.nama,
                    "" if mhs.tugas is None else mhs.tugas,
                    "" if mhs.uts is None else mhs.uts,
                    "" if mhs.uas is None else mhs.uas,
                    nilai_akhir_str,
                    grade,
                    kehadiran_str,
                    presensi_str
                ])

        print(f"Data berhasil disimpan ke file {filename}")

    # LOAD DATA (CSV)
    def load_data(self, filename: Path = FILE_PATH):
        filename = Path(filename)
        try:
            with open(filename, mode="r", newline="", encoding="utf-8-sig") as file:
                reader = csv.DictReader(file, delimiter=CSV_DELIM)
                self.data_mahasiswa.clear()

                for row in reader:
                    mhs = Mahasiswa(row["NIM"], row["Nama"])

                    if row.get("Tugas"):
                        mhs.tugas = int(row["Tugas"])
                    if row.get("UTS"):
                        mhs.uts = int(row["UTS"])
                    if row.get("UAS"):
                        mhs.uas = int(row["UAS"])

                    pres = row.get("Presensi", "")
                    if pres:
                        for item in pres.split(PRESENSI_DELIM):
                            if ":" in item:
                                n, status = item.split(":", 1)
                                mhs.presensi[int(n)] = status

                    self.data_mahasiswa.append(mhs)
            print(f"Data berhasil dimuat dari file {filename}")
        except FileNotFoundError:
            print(f"File {filename} belum ditemukan, mulai dengan data kosong.")


# MENU UTAMA 
def main():
    mhs_manager = ManajemenDataMahasiswa()
    mhs_manager.load_data()

    while True:
        print("\n1. Tambah Mahasiswa")
        print("2. Input Presensi Mahasiswa")
        print("3. Input Nilai Akademik")
        print("4. Tampilkan Semua Data Mahasiswa")
        print("5. Simpan Data")
        print("6. Keluar")
        pilihan = input("Pilih menu (1-6): ").strip()

        if pilihan == "1":
            while True:
                nim = input("Masukkan NIM: ").strip()
                nama = input("Masukkan Nama: ").strip()
                try:
                    mhs_manager.tambah_mahasiswa(nim, nama)
                    break
                except ValueError as ve:
                    print(ve)

        elif pilihan == "2":
            try:
                n = int(input("Masukkan nomor pertemuan ke-n: "))
                mhs_manager.input_presensi_sistem(n)
            except ValueError:
                print("Input nomor pertemuan harus angka.")

        elif pilihan == "3":
            while True:
                nim = input("Masukkan NIM mahasiswa: ").strip()
                mhs = mhs_manager.cari_mahasiswa(nim)
                if not mhs:
                    print(f"Error: Mahasiswa dengan NIM {nim} tidak ditemukan. Silakan coba lagi.")
                    continue
                nilai_sukses = False
                while not nilai_sukses:
                    try:
                        tugas = int(input("Nilai Tugas (0-100): "))
                        uts = int(input("Nilai UTS (0-100): "))
                        uas = int(input("Nilai UAS (0-100): "))
                        mhs_manager.input_nilai_sistem(nim, tugas, uts, uas)
                        nilai_sukses=True
                    except ValueError as ve:
                        print("Input nilai tidak valid:", ve)
                        continue
                if nilai_sukses:
                    break

        elif pilihan == "4":
            mhs_manager.tampil_data_mahasiswa()

        elif pilihan == "5":
            mhs_manager.simpan_data()

        elif pilihan == "6":
            print("Keluar program. Pastikan sudah menyimpan data.")
            break

        else:
            print("Pilihan tidak valid, silakan coba lagi.")

if __name__ == "__main__":
    main()
