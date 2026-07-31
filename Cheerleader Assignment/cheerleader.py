word = input("Enter a word: ")
for character in word:
    if character in "AEIOUaeiou":
        print(f"Give me an {character.upper()}!")
    else:       
        print(f"Give me a {character.upper()}!")
print(f"What does it say????? {word.upper()}!!!!!!")