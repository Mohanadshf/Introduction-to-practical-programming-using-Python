__author__ = 'Al-Ramessi, 8658986'

"""
Inventory Management System

Manage items in nested storage locations. Supports:
- Adding items
- Listing all items alphabetically
- Searching for items and showing their locations
- Summarizing storage contents
- Updating item properties
- Creating and viewing backups with timestamps
"""

import copy
from datetime import datetime


lager = {}

def insert(lagerort, item_name):
    current = lager
    for ort in lagerort:
        if ort not in current:
            current[ort] = {}
        current = current[ort]
    current[item_name] = {}

def list_all(storage):
    Items=[]
    stack =[storage]

    while stack:
        current = stack.pop()
        for key,value in current.items():
            if value == {}:
                Items.append(key)
            else:
                stack.append(value)
    return sorted(Items)

def find_item(storage,target):
    results = []
    stack = [(storage, [])]

    while stack:
        current, path = stack.pop()
        for key, value in current.items():
            if key == target and value == {}:
                results.append(path + [key])
            elif value != {}:
                stack.append((value, path + [key]))
    return results

def summarize_locations(storage, locations):
    summary = {}
    for loc in locations:
        if loc not in storage:
            summary[loc] = "Lagerort existiert nicht"
            continue

        items = []
        stack = [(storage[loc], [loc])]  #starting point

        while stack:
            current, path = stack.pop()

            for key in current:
                value = current[key]

                if value == {}:
                    items.append("/".join(path + [key])) 
                elif value != {}:
                    stack.append((value, path + [key]))  # move to lower storage

        summary[loc] = sorted(items)

    return summary

def update_item(storage, path, item_name, new_properties):
    current = storage
    for place in path:
        if place not in current:
            print(f"Lagerort '{place}' existiert nicht.")
            return
        current = current[place]
    
    if item_name not in current:
        print(f"Gegenstand '{item_name}' existiert hier nicht.")
        return
    
    # eigenschaften aktualisieren
    current[item_name].update(new_properties)

def create_backup(storage):
    backup = copy.deepcopy(storage)  
    timestamp = datetime.now()        
    return {"backup": backup, "timestamp": timestamp}

def show_backup(backup_info, storage):

    print(f"Backup erstellt am: {backup_info['timestamp']}")
    print("\n Aktuelles Inventar: ")
    print(storage)
    print("\nBackup: ")
    print(backup_info['backup'])

#test cases:

# Insert items
insert(["Keller", "Werkzeugkiste"], "Hammer")
insert(["Keller", "Werkzeugkiste"], "Zange")
insert(["Schrank", "Kiste"], "Hammer")
insert(["Schrank"], "Handtücher")

# List all
print(list_all(lager))

# Search
print(find_item(lager, "Hammer"))

# Summarize
print(summarize_locations(lager, ["Keller", "Schrank", "Dachboden"]))

# Update
update_item(lager, ["Keller", "Werkzeugkiste"], "Hammer", {"zustand": "neu"})
print(lager["Keller"]["Werkzeugkiste"]["Hammer"])

# Backup
backup_info = create_backup(lager)
show_backup(backup_info, lager)
