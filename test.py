import numpy as np
import pickle

arr = np.array([7,7,7])
arr0 = np.array([0,1.1,2,3,0,0,6,7,8,9])
arr1 = np.array([0,1,0,3,4,5,6,7,8,0])
arr2 = np.array([10,11,12,13,14,15,16,17,18,19])
# print(arr2[np.logical_and(arr0!=0, arr1!=0)])
# arr4 = np.vstack([arr0, arr1, arr2])
# print(arr4)
# print(np.nonzero(arr0))
# print(np.nonzero(arr4))

# arr0 = np.array([1,2,3])
# arr1 = np.array([1,2,3,4])
# arr2 = np.array([1,2,3,4,5])

# error
# arr3 = np.vstack([arr0, arr1, arr2])
# print(arr3)

# arr3 = np.array([[1,2,3], [1,2,3]])

A = [arr, arr0, arr1, arr2]
print(A)
AAA = np.array(A, dtype=np.object_)
# print(AAA[1][1])
# print(len(AAA))
# print(len(AAA[1]))
with open('import', 'wb') as file:
    pickle.dump(AAA, file)



# with open('import', 'rb') as file:
#     data = pickle.load(file)
#     print(type(data))
# with open('import', 'wb') as file:
#     d = [data, arr]
#     print(d)
#     pickle.dump(d, file)

with open('import', 'rb') as file:
    data = pickle.load(file)
print('Showing the pickled data:')
cnt = 0
for item in data:
    print('The data ', cnt, ' is : ', item)
    cnt += 1

#with open('import', 'ab') as file:
with open('import', 'wb') as file:
    print(f'try to add to the end {arr}')
    # aa = np.empty(1, dtype=np.object_)
    # aa[0] = arr
    # a = np.concatenate(data, aa)
    a = np.hstack((data, np.empty(1)))
    a[-1] = arr
    #pickle.dump(arr, file)
    pickle.dump(a, file)

with open('mindata', 'rb') as file:
    data = pickle.load(file)
print('Showing the pickled data:')
cnt = 0
for item in data:
    print('The data ', cnt, ' is : ', item)
    cnt += 1

with open('mindata', 'wb') as file:
    arr = [1,1,1]#np.ones(1280*3)
    print(f'try to add to the end {arr}')
    # aa = np.empty(1, dtype=np.object_)
    # aa[0] = arr
    # a = np.concatenate(data, aa)
    a = np.hstack((data, np.empty(1)))
    a[-1] = arr
    #pickle.dump(arr, file)
    pickle.dump(a, file)

with open('mindata', 'rb') as file:
    data = pickle.load(file)
print('Showing the pickled data:')
cnt = 0
for item in data:
    print('The data ', cnt, ' is : ', item)
    cnt += 1