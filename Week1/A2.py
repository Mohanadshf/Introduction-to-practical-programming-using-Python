
__author__ = "8658986, Mohanad Al-Ramessi"


while True:
    try:
        jahr = int(input("gib ein jahr "))
        if jahr > 0:
            break
        else:
            print("es muss ein positive int sein")
    except ValueError:
        print("es muss ein int sein")

if jahr % 400 == 0 or (jahr % 4 == 0 and jahr % 100 != 0):
    print("Das Jahr", jahr, "ist ein Schaltjahr.")
else:
    print("Das Jahr", jahr, "ist kein Schaltjahr.")
