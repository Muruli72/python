"""Leap year calculation module."""
#year=int(input("Enter a year: "))
#if(year%4==0 and year%100!=0)or(year%400==0):
 #   print(f"{year} is a leap year.")
#else:
 #   print(f"{year} is not a leap year.")
row1=['😃','😃','😃']
row2=['😃','😃','😃']
row3=['😃','😃','😃']
matrix=[row1,row2,row3]
a=(input("Enter a Number to find element:"))
row=int(a[0])
col=int(a[1])
matrix[row-1][col-1] = 'X'
print(f"{row1}\n{row2}\n{row3}")