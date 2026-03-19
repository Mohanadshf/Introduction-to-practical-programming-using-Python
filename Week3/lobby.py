__author__ = 'Al-Ramessi, 8658986'


from guess import run as run_guess
from turtle_game import run as run_turtle
from binary_converter import run as run_binary

def main_menu():
    while True:
        print("\n--- Main Menu ---")
        print("1: Number Guessing Game")
        print("2: Turtle Drawing (Chaos Game)")
        print("3: Decimal to Binary Converter")
        print("q: Quit Program")

        choice = input("Enter your choice: ").strip().lower()

        if choice == "1":
            run_guess()
        elif choice == "2":
            run_turtle()
        elif choice == "3":
            run_binary()
        elif choice == "q":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ =="__main__":
    main_menu()