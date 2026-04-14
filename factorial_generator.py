import time

def factorial(n):
    ans = 1
    for i in range(1, n+1):
        ans *= i
        yield ans

start = time.time()

gen = factorial(1000)
result = None
for _ in range(1000):
    result = next(gen)
print(f"결과: {result}")

end = time.time()
print(f"{(end - start)*1000}ms")