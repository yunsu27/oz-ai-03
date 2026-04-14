import time

def factorial(n):
    ans = 1
    for i in range(1, n+1):
        ans *= i
    return ans

start = time.time()
print(f"{factorial(1000)}")
end = time.time()
print(f"{(end - start)*1000}ms")