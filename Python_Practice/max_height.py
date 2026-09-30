height=input("Enter the heights : ")
height_list=height.split()
count=0
for i in height_list:
    count+=1
max_height=float(height_list[0])
for i in range(count):
    if float(height_list[i])>max_height:
        max_height=float(height_list[i])
print(f"The maximum height is: {max_height}")