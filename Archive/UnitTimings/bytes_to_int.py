import time
def bytes_to_int_1(data) -> int:
    return (data[0] + data[1]*256 + data[2]*65536 + data[3]*16777216)

data = bytes([173, 134, 167,111])
start = time.time()
bytes_to_int_1(data)
end = time.time()
print(end-start)

start = time.time()
int.from_bytes(data, byteorder="little", signed=False)
end = time.time()
print(end-start)

# conversion 1 is faster