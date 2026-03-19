
__author__ = 'Al-Ramessi, 8658986'
import random


def run():
    print("\n--- Guess the Number ---")
    print("Try to guess the secret number between -10 and 30.")
    print("Type 'm' at any time to return to the main menu.\n")
    
    target= random.randint(-10,30)
    attempts = 0
    while True:
        guess_text = input('Pick a number or press m for Menu:').strip()
        if guess_text.lower() in ('m','menu'):
            print('Returning to main Menu...')
            return
        
        try:
            guess=int(guess_text)
        except ValueError:
            print("Please print a valid whole number or 'm' to return.")
            continue
        
        attempts+=1
        if guess==target:
            print(f"You guessed correctly in {attempts} attempts!")
            return
        elif guess>target:
            print('your guess was too high, try guessing lower')
        else:
            print('your guess was too low, try guessing higher.')


if __name__ == "__main__":
    run()