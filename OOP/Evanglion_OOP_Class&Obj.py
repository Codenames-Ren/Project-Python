class Evangelion:
    def __init__(self, unit, pilot):
        self.unit = unit
        self.pilot = pilot

    #Objek tampilan untuk informasi dari unit dan pilot
    def pilot_information(self):
        print (f"Unit  : {self.unit}")
        print (f"Pilot : {self.pilot}")
    
def main():
    list_eva = []

    while True:
        print ("===== Format Input Data =====")
        print()
        print("1. Manual Input Unit dan Pilot Terpisah")
        print("2. Input Cepat (Format Penulisan : EVA-XX, Pilot)")
        print()
        pilihan =  input("Pilih Format Inputan [1/2] : ")
        print()

        #Manual Input
        if pilihan == '1':
            unit = input("Unit Number EVA (EX: EVA-XX) : ")
            pilot = input("Nama Pilot EVA : ")
            print()
            list_eva.append(Evangelion(unit, pilot))

        elif pilihan == '2':
            while True:
                try:
                    eva_data = input("Masukkan Data Pilot (Format Penulisan : EVA-XX, Nama Pilot) : ")
                    print()
                    #Buat ngecek ada tanda koma apa nggak saat inputan sebelumnya
                    if ',' not in eva_data:
                        #raise buat bikin error secara manual untuk kondisi tertentu
                        raise ValueError("Format input harus menggunakan tanda koma (,)!")

                    eva_data_entries = eva_data.split(',')
                    unit = eva_data_entries[0].strip()
                    pilot = eva_data_entries[1].strip()

                    if not unit or not pilot:
                        raise ValueError("Unit dan Nama Pilot tidak boleh kosong!")

                    list_eva.append(Evangelion(unit, pilot))
                    break
                
                #keyword except dipake buat nangkep pesan error terus diubah pesannya supaya lebih friendly
                except ValueError as e:
                    print (f"Error: {e}, Gunakan Format EVA-XX, Nama Pilot!")
                    print()
                
                except IndexError:
                    print ("Error: Format Input Salah! Gunakan Format EVA-XX, Nama Pilot!")
                    print()

        else:
            print("Pilihan Tidak Valid!")
            print()
            continue
        
        #Looping untuk menginput data lain atau menampilkan data yang sudah diinput
        while True:
            retry = input("Input data lain? [Y/T] : ")
            print()
            if retry.lower() == 'y':
                break

            elif retry.lower() == 't':
                print ("===== Data Pilot Eva =====")
                print()
                if not list_eva:
                    print("Belum ada data yang di input!")
                else:
                    for eva in list_eva:
                        eva.pilot_information()
                        print()
                print("Checked by NERV.")
                return

            else:
                print("INVALID! Choose Y/T!")
                print()

main()