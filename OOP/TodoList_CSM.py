from datetime import datetime
from fpdf import FPDF

class ToDOList:
    def __init__(self):
        self.aktivitas = []
        self.tanggal = datetime.now().strftime("%d-%m-%Y, %I:%M:%S %p")

    def tambah_aktivitas(self, tugas, nama, partner, location):
        self.aktivitas.append((tugas, nama, partner, location))
    
    def rincian_data(self):
        print("===== Jadwal Harian Public Safety Devil Hunter =====")
        print("=====            Special Divison 4             =====")
        print()
        print(f"Dibuat Pada : {self.tanggal}")
        print()
        for idx, (tugas, nama, partner, location) in enumerate(self.aktivitas, start = 1):
            print (f"Jadwal {idx} :")
            print (f"   - Kegiatan                 : {tugas}")
            print (f"   - Anggota yang bertugas    : {nama}")
            print (f"   - Partner yang berpasangan : {partner}")
            print (f"   - Lokasi                   : {location}")
            print()

    def cancel(self):
        self.aktivitas = []
    
    def save_to_pdf(self, nama_file="jadwal_harian.pdf"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt = "Jadwal Harian Public Safety Devil Hunter", ln=True, align='C')
        pdf.cell(200, 10, txt = "Special Division 4", ln=True, align='C')
        pdf.cell(200, 10, txt = f"Dibuat pada : {self.tanggal}", ln=True, align='C')
        pdf.ln(10)

        for idx, (tugas, nama, partner, location) in enumerate(self.aktivitas, start=1):
                pdf.cell(200,10,txt=f"Jadwal {idx}.  Kegiatan : {tugas}", ln=True)
                pdf.cell(200,10, txt=f"Anggota yang bertugas  : {nama}", ln=True)
                pdf.cell(200,10, txt=f"Berpasangan dengan     : {partner}", ln=True) 
                pdf.cell(200,10, txt=f"Lokasi                 : {location}", ln=True)
                pdf.ln(5)

                pdf.output(nama_file)
                print(f"File berhasil disimpan dengan nama {nama_file}")

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
                todo.save_to_pdf()
                break
            elif pilihan.lower() == 't':
                todo.cancel()
                print()
                print("Operasi dibatalkan, data berhasil dihapus!")
                print("Kembali ke Awal Program.")
                print()
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