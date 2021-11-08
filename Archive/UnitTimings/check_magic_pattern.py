import functools
import time

def check_magic_pattern_1(data) -> int:
        if (data[0] == 2 and data[1] == 1 and data[2] == 4 and data[3] == 3 and data[4] == 6 and data[5] == 5 and data[6] == 8 and data[7] == 7):
            return 1
        return 0

set_comp = set([2,1,4,3,6,5,8,7])
list_comp = [2,1,4,3,6,5,8,7]

def check_magic_pattern_2(data) -> int:
    if set(data) == set_comp:
        return 1
    return 0

def check_magic_pattern_3(data) -> int:
    return functools.reduce(lambda x, y : x and y, map(lambda p, q: p == q,data,list_comp), True)


data1 = [2,1,4,3,6,5,8,7]
data2 = [2,1,4,3,6,5,8,6]
data3 = [3,1,4,3,6,5,8,5]
data4 = [3,1,3,3,5,4,3,4]

def test(data):
    start = time.time()
    check_magic_pattern_1(data)
    end = time.time()
    print(end-start)

    start = time.time()
    check_magic_pattern_2(data)
    end = time.time()
    print(end-start)

    start = time.time()
    check_magic_pattern_3(data)
    end = time.time()
    print(end-start)

print("data1")
test(data1)
print("data2")
test(data2)
print("data3")
test(data3)
print("data4")
test(data4)

# magic pattern 1

