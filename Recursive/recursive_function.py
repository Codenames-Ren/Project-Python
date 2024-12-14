def data_pemain(level, level_tertinggi, total_waktu=0, total_item=0):
    if level > level_tertinggi:
        return total_waktu, total_item
    
    print (f"Data Pemain di Level {level} ")
    print()
    waktu = int(input("Waktu yang dihabiskan untuk bermain (satuan menit) : "))
    item =  int(input("Jumlah item yang telah dikumpulkan : "))
    print()

    return data_pemain(
        level + 1,
        level_tertinggi,
        total_waktu + waktu,
        total_item + item
    )

#Awal Program
pemain = input("Nama Pemain : ")
level_sekarang = int(input("Level saat ini : "))
total_waktu, total_item = data_pemain(1, level_sekarang)

print()
print ("Informasi Pemain : ")
print (f"Nama Pemain                           : {pemain}")
print (f"Total Waktu Bermain                   : {total_waktu} Menit")
print (f"Jumlah item yang berhasil dikumpulkan : {total_item} Item")
print (f"Level yang tercapai                   : {level_sekarang}")