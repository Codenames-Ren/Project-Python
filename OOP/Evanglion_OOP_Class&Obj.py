class Evangelion:
    def __init__(self, unit, pilot):
        self.unit = unit
        self.pilot = pilot

    def pilot_information(self):
        print (f"Unit  : {self.unit}")
        print (f"Pilot : {self.pilot}")
    
def main():
    list_eva = []

    while True:
        print ("===== Data Pilot Eva =====")
        print()
        unit = input("Unit Number EVA (EX: EVA-00) : ")
        pilot = input("Nama Pilot EVA : ")
        print()
        eva = Evangelion(unit, pilot)
        list_eva.append(eva)

        print ("===== DATA UNIT EVA =====")
        for eva in list_eva:
            eva.pilot_information()
            print()

        while True:
            retry = input("Input data lain? [Y/T] : ")
            print()
            if retry.lower() == 'y':
                print("Dimengerti.")
                print()
                break
            elif retry.lower() == 't':
                print("Please wait...")
                exit()
            else:
                print("INVALID! Choose Y/T!")
                print()

main()