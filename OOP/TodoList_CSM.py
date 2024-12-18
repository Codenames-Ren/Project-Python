from datetime import datetime

class ToDOList:
    def __init__(self):
        self.aktivitas = []
        self.tanggal = datetime.now().strftime("%d-%m-%Y, %I:%M:%S %p")

    def tambah_aktivitas(self, tugas, nama, partner, location):
        self.aktivitas.append(tugas)
        self.aktivitas.append(nama)
        self.aktivitas.append(partner)
        self.aktivitas.append(location)
    
    def rincian_data(self):
        print("===== Jadwal Harian Public Safety Devil Hunter =====")
        print("=====            Special Divison 4             =====")
        print()
        print(f"Dibuat Pada : {self.tanggal}")
        print()
        for idx, tugas in enumerate(self.aktivitas, start = 1):
            print (f"{idx}. {tugas}")
    
    def cancel(self):
        self.aktivitas = []

def main():
    todo = ToDOList()

    while True:
        print ("Jadwal Harian Public Safety Devil Hunter Special Divison 4")
        print()
        tugas = input("Kegiatan hari ini : ")
        nama = input("Anggota yang bertugas : ")
        partner = input("Akan berpasangan dengan : ")
        location = input("Misi hari ini akan berlangsung di Kota : ")
        print()
        todo.tambah_aktivitas(tugas, nama, partner, location)
        
        while True:
            pilihan = input("Ketik [Y] untuk submit data atau [T] untuk membatalkan : ")
            if pilihan.lower() == 'y':
                print()
                todo.rincian_data()
                break
            elif pilihan.lower() == 't':
                todo.cancel()
                print("Operasi dibatalkan, data berhasil dihapus!")
                print("Kembali ke Awal Program.")
                main()
            else:
                print()
                print("Pilihan tidak valid! pilih [Y] untuk Submit atau [T] untuk membatalkan!")
        
        while True:
            print()
            ulangi =  input("Ada data lain yang ingin diinput? [Y/T] : ")
            print()
            if ulangi.lower() == 'y':
                print("Mohon Tunggu.")
                break
            elif ulangi.lower() == 't':
                print("Telah di konfirmasi oleh : Makima")
                exit()
            else:
                print("Tidak valid! pilih [Y/T]!")

main()