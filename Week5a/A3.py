
user_input = input("Insert your String: ")
print(len(user_input))
print(user_input.isalpha())
print(user_input.isidentifier())
print(user_input.endswith('ing'))
print(user_input.islower())
print(user_input.replace('a', 'e'))

# Three test cases
tests = ["hello123", "class", "123abc"]
for s in tests:
    print(len(s))
    print(s.isalpha())
    print(s.isidentifier())
    print(s.endswith('ing'))
    print(s.islower())
    print(s.replace('a', 'e'))
