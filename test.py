import time

def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        print(f"Executing function '{func.__name__}'...")
        
        # Execute the function and capture its return value
        result = func(*args, **kwargs)

        print(f"Function '{func.__name__}' executed successfully.")
        
        end_time = time.time()
        print(f"Function '{func.__name__}' took {end_time - start_time:.4f} seconds to run.")
        
        # Return the original function's result
        return result
    return wrapper

@timer_decorator
def calculate_heavy_sum(n):
    return sum(range(n))

# Running the decorated function
total = calculate_heavy_sum(10_000_000)
print(f"Total Sum: {total}")