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
        waktu = int(input("Lama Waktu bermain (satuan menit) : "))
        item = int(input("Jumlah item yang didapatkan : "))
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

print ("=====DATA PLAYER=====")
nama_player = input("Nama Player : ")
level_tertinggi = int(input("Level saat ini : "))

#bikin object Player
player = Player(nama_player)
player.level_tertinggi = level_tertinggi
player.data_player(1)
player.informasi_player()