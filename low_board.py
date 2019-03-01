# a = [1,2,3,6,8]
# b = [2,5,7]

# print(a,b)
# print('Expected board is 1,2,3,5,6')


a = [1,2,3,4,8]
b = [2,3,7]

print(a,b)
print('Expected board is 1,2h,3,4,7h')

# a = [1,2,3,4,7]
# b = [2,3,4,8]

# print(a,b)
# print('Expected board is 1,2h,3h,4,7')


a.sort()
b.sort()
f = []
dup_count = 0    
for z in range(2):
    if b[z] in a: dup_count += 1

if dup_count == 0:
    f = a[0:2] + b[0:1]
elif dup_count == 1:
    if len(a) > 3 and len(b) > 2:
        if a[3] >= b[2]:
            f = a[0:3] + b[0:3]
        else:
            f = a[0:4] + b[0:2]
    elif len(a) > 3 and len(b) = 2:
            f = a[0:4] + b[0:2]
    elif len(a) = 3 and len(b) > 2:
            f = a[0:3] + b[0:3]
    else:
        print('No low')
        f = []
elif dup_count == 2:
    if len(a) = 5 and len(b) = 3:
    if len(a) = 5 and len(b) = 4:

    
    
    elif len(a) = 4 and len(b) > 3:
            f = a[0:4] + b[0:3]        
    elif len(a) = 5 and len(b) = 2:
            f = a[0:5] + b[0:2]
    elif len(a) = 3 and len(b) = 4:
            f = a[0:3] + b[0:4]
    else:
        print('No low')
        f = []

f = list(set(f))
f.sort()    
print(f)

       