num = input("Enter numbers seprated by comma : ")
num_list = [int(n) for n in num.split(",")]

even = 0
odd = 0

for i in num_list:
    if i % 2 == 0:
        even+=1
    else:
        odd+=1

print(even)
print(odd)