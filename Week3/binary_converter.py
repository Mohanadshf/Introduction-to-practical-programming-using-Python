
def run():
    while True:
        user_input = input('Enter a positive number or press m for main Menu. ').strip()

        if user_input.lower() == 'm':
            print("Returning to main menu...\n")
            break

        if not user_input.isdigit():
            print(f"'{user_input}' is not a positive integer. Try again or press 'm' for menu.\n")
            continue

        n = int(user_input)
        if n == 0:
            print("Decimal 0 = Binary 0\n")
            continue

        original_n = n
        remainders = []

        print("\nStep-by-step division:")
        while n > 0:
            quotient = n // 2
            remainder = n % 2
            remainders.append(remainder)
            print(f"{n} / 2 = {quotient} remainder {remainder}")
            n = quotient
        
        binary_str = ""
        for digit in reversed(remainders):
            binary_str += str(digit)


        print(f"\nDecimal {original_n} = Binary {binary_str}\n")

            

if __name__ == "__main__":
    run()
