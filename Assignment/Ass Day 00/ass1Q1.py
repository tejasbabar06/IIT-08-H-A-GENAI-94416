sen = input("Entre the sentence : ")

print(len(sen))

words = sen.split()
print(len(words))

vowels = "aeiouAEIOU"
count = 0

for i in sen:
    if i in vowels:
        count+=1

print(count)