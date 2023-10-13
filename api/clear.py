k = 15
o = 22

cel = (o // k)
ost = 0 if o%k == 0 else 1

if k * 1.5 >= o:
    st = "green"
elif k * 2.5 >= o:
    st = "yellow"
elif k * 3.5 >= o:
    st = "orange"
else:
    st = "red"

print(st)


print((cel+ost)*10)