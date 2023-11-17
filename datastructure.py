import numpy as np
import pandas as pd
import pickle

# A = np.array([1,2,3])
# B = np.array([4,5,6,7])
# C = np.ones(3)
# D = np.zeros(2)
# points_list = [A, B, C, D]
# points_array = np.array(points_list, dtype=np.object_)
# print(f'shape1: {points_array.shape}')
# print(f'type of points_array: {type(points_array)}. type of elements: {type(points_array[1])}')
#
# add_points = [3,2]
# print(f'shapes: {points_array.shape}, {np.empty(1).shape}') #shapes: (4,), (1,)
#
# points_array = np.hstack((points_array, np.empty(1)))
# points_array[-1] = np.array(add_points)
# print(f'added array of additional points: {add_points}')
# print(f'result: {points_array}')

# with open('data', 'wb') as f:
#     pickle.dump(points_array, f)
#
# with open('data', 'rb') as f:
#     arr = pickle.load(f)
#     print(f'loaded from pickle: {type(arr)}')
# for el in arr:
#     print(el)
#
# arr = np.hstack((arr, np.empty(1)))
# arr[-1] = np.array([10,10,10])
# with open('data', 'wb') as f:
#     pickle.dump(arr, f)
#     print('wrote to pickle with additional np.array [10,10,10]')
# with open('data', 'rb') as f:
#     arr = pickle.load(f)
#     print(f'loaded from pickle: {type(arr)}')
# for el in arr:
#     print(el)

# ar0 = [0] #!!!!!!!!!!
# # ar1 = [1, 1]
# ar1 = np.zeros(1280*3)
# # ar2 = np.ones(1280*3)
# # ar = [ar0, ar1, ar2]
# ar = [ar0, ar1]
# ar = np.array(ar, dtype=np.object_)
# print(f'shape1: {ar.shape}')
# with open('data', 'wb') as f:
#     pickle.dump(ar, f)
# ar2 = np.ones(1280*3)
# with open('data', 'rb') as f:
#     ar = pickle.load(f)
# for el in ar:
#     print(el)
# print(f'shapes: {ar.shape}, {np.empty(1).shape}')
# ar = np.hstack((ar, np.empty(1)))
# ar[-1] = ar2
# with open('data', 'wb') as f:
#     pickle.dump(ar, f)
# with open('data', 'rb') as f:
#     ar = pickle.load(f)
#     print(f'loaded from pickle: {type(ar)}')
# new_ar = np.delete(ar, 0)
# for el in new_ar:
#     print(el)

def addNewFrameToPickle(addArr, filename):
    with open(filename, 'rb') as file:
        arr = pickle.load(file)
    arr = np.hstack((arr, np.empty(1)))
    arr[-1] = addArr
    with open(filename, 'wb') as file:
        pickle.dump(arr, file)

def initNewPickle(filename):
    arr0 = [0] #!!! only with this two rows
    arr1 = np.zeros(1280*3) #!!! only with this two rows
    arr = [arr0, arr1]
    arr = np.array(arr, dtype=np.object_)
    # print(f'shape1: {arr.shape}')
    with open(filename, 'wb') as file:
        pickle.dump(arr, file)

def finalizePickle(filename):
    with open(filename, 'rb') as file:
        arr = pickle.load(file)
    new_arr = np.delete(arr, [0, 1])
    with open(filename, 'wb') as file:
        pickle.dump(new_arr, file)

def converPickleToCSV(filename):
    with open(filename, 'rb') as file:
        arr = pickle.load(file)
    # fmt = '%f,%f,%f'
    # with open('111', 'w') as file:
    #     np.savetxt(file, arr, delimiter=',', fmt=fmt)
    print('converted')
    df = pd.DataFrame([el for el in arr])
    df.to_csv('1111.csv', index=False)
    df1 = pd.read_csv('111.csv')
    # print(df1.iloc[1, 3839])


def printPickle(filename):
    with open(filename, 'rb') as file:
        arr = pickle.load(file)
    for element in arr:
        print(element)

filename = 'testdata1'
print(f'1. initialization of pickle {filename}')
initNewPickle(filename)
print(f'    pickle {filename}:')
printPickle(filename)

# arr2 = np.ones(1280*3)
# print(f'2. adding arr {arr2} to pickle {filename}')
# addNewFrameToPickle(arr2, filename)
# print(f'    new pickle {filename}:')
# printPickle(filename)

for i in range(5000):
    addNewFrameToPickle(np.full(1280*3, float(i)), filename)
    # print(f'{i}    pickle {filename}:')
    # printPickle(filename)
finalizePickle(filename)
print(f'print finalized pickle {filename}:')
printPickle(filename)

converPickleToCSV(filename)