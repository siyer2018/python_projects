VOWELS = "aeiou"
#store the vowels
vowels=''
#store the constants
consonants=''
index=0
new_word = ""
#while loop asking for the input of word
while len(vowels) != 5:
    word=input("Input a word: ").lower()
    #Enumerating the word
    for i, ch in enumerate(word):
        if ch in VOWELS:
            index=i
            if ch not in vowels:
                vowels+=ch
    #utilized the index of the last vowels in order to obtain the remaining consonants
    for a in word[index:]:
        if a not in VOWELS and a not in consonants:
                consonants += a
    if len(consonants) >= 5:
        break
print("\n"+"="*12)               
print("{:8s}{:7s} | {:12s}{:7s}".format("vowels","length","consonants","length"))
print("{:8s}{:7s} | {:12s}{:7s}".format(vowels,str(len(vowels)),consonants,str(len(consonants))))