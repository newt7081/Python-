f = open("text.txt", "w")
for i in range(100000000):
	if i==0:
		f.write("00000000")
	elif i<10000000:
		b = str(i)
		c = "0"+b
		for z in range(7-len(str(i))):
			c = "0"+c
		f.write(c)
	else:
		f.write(str(i))
	f.write("\n")
f.close()






# a = 1
# b = "0"+str(a)
# b = "0"+b
# print(b)








