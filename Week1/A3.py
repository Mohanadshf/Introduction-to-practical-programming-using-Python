
__author__ = "8658986, Mohanad Al-Ramessi"

alter = input("Alter (jung / erwachsen / senior): ").lower().strip()
haltung = input("Haltungsart (hauskatze / freigänger): ").lower().strip()


match (alter, haltung):
    case ("jung", "hauskatze"):
        print("Kittenfutter für Wohnungskatzen (bis 12 Monate)")
    case ("jung", "freigänger"):
        print("Energiehaltiges Futter für junge Freigänger")
    case ("erwachsen", "hauskatze"):
        print("Futter für erwachsene Wohnungskatzen")
    case ("erwachsen", "freigänger"):
        print("Energiehaltiges Futter für aktive Katzen")
    case ("senior", "hauskatze"):
        print("Senior-Futter mit reduziertem Kaloriengehalt")
    case ("senior", "freigänger"):
        print("Senior-Futter mit mehr Energie")
    case _:
        print("Eingabe nicht erkannt.")
