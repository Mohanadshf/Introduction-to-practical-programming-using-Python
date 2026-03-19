def main():
    while True:
        try:
            decimal = input("enter a positive int ")
            if decimal.isdigit() :
                decimal = int(decimal)
                if decimal > 0 :
                    break
            
            print("please enter a positive int")
        except ValueError:
            print ("invalid input")
            
    remainders = []
    
    while decimal != 0:
        quetiont = decimal //2
        remainder = decimal % 2
        remainders.append(str(remainder))
        print(f"decimal {decimal} = quetiont {quetiont} x 2 + remainder {remainder}")
        decimal = quetiont
    for _ in reversed(remainders):
        print(_, end="")
        
if __name__ == "__main__":
    main()