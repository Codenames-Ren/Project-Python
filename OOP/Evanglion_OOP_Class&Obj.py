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
                eva_data = input("Masukkan Data Pilot (Format Penulisan : EVA-XX, Nama Pilot) : ")
                print()
                try:
                    eva_data_entries = eva_data.split(',')
                    unit = eva_data_entries[0].strip()
                    pilot = eva_data_entries[1].strip()
                    list_eva.append(Evangelion(unit, pilot))
                    break
                
                except IndexError:
                    print ("Format Penulisan Salah! Gunakan Format EVA-XX, Nama Pilot!")
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