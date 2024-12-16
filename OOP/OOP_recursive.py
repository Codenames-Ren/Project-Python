class Player:
    #Objek *Notes : __init__ itu konstruktor di python
    #berarti 2 underscore di awal sama akhir nandain kalo si functionnya special
    def __init__(self, nama):
        self.nama = nama
        self.total_waktu = 0
        self.total_item = 0
        self.level_tertinggi = 0
    
    #Recursive Function
    def data_player(self, level):
        #basecasenya
        if level > self.level_tertinggi:
            return 
        
        print (f"Data Player di Level {level} : ")
        #Looping sama Error Handling kalo user salah inputan
        while True:
            try:
                waktu = int(input("Lama Waktu bermain (satuan menit) : "))
                item = int(input("Jumlah item yang didapatkan : "))
                if waktu <= 1 and item >= 0:
                    raise ValueError("Waktu tidak boleh kurang dari 1")
                print()
                break
            except ValueError as e:
                print (f"Error: {e}, Gunakan angka untuk menginput Waktu dan Item!")
                print()

        self.total_waktu += waktu
        self.total_item += item

        #Recursive untuk level up
        self.data_player(level + 1)

    def informasi_player(self):
        print ("Informasi Player : ")
        print (f"Nama Player                 : {self.nama}")
        print (f"Total Waktu Bermain         : {self.total_waktu} menit")
        print (f"Total Item yang didapat     : {self.total_item} item")
        print (f"Level yang berhasil dicapai : {self.level_tertinggi}")

def main():
    while True:
        print ("=====DATA PLAYER=====")
        nama_player = input("Nama Player : ")
        #Error Handling juga 
        while True:
            try:
                level_tertinggi = int(input("Level saat ini : "))
                if level_tertinggi < 1:
                    raise ValueError("Level tidak boleh kurang dari 1!")
                print()
                break
            except ValueError as e:
                print (f"Error: {e}, Gunakan angka untuk menginput level!")
                print()

        #bikin object Playernya
        player = Player(nama_player)
        player.level_tertinggi = level_tertinggi
        player.data_player(1)
        player.informasi_player()

        #Looping lagi, yang ini buat ngulang program atau keluar 
        while True:
            retry = input("Ingin input lagi? [Y/T] : ")
            print()
            if retry.lower() == 'y':
                print("Dimengerti.")
                print()
                break

            elif retry.lower() == 't':
                print("Please Wait...")
                exit()
            
            else:
                print("Tidak Valid! Pilih Y/T!")
                print()

main()