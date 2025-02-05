from fastapi import FastAPI, Query, HTTPException
import requests
import asyncio
from functools import lru_cache

app = FastAPI()

# Enable CORS
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cache for fun facts to reduce external API calls
FUN_FACT_CACHE = {}

@lru_cache(maxsize=1000)  # Cache results for faster repeated requests
def is_prime(n: int) -> bool:
    """Check if a number is prime."""
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

@lru_cache(maxsize=1000)  # Cache results for faster repeated requests
def is_perfect(n: int) -> bool:
    """Check if a number is perfect."""
    if n < 2:
        return False
    divisors = {1}
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            divisors.add(i)
            divisors.add(n // i)
    return sum(divisors) == n

@lru_cache(maxsize=1000)  # Cache results for faster repeated requests
def is_armstrong(n: int) -> bool:
    """Check if a number is an Armstrong number."""
    digits = [int(d) for d in str(n)]
    length = len(digits)
    return sum(d ** length for d in digits) == n

@lru_cache(maxsize=1000)  # Cache results for faster repeated requests
def digit_sum(n: int) -> int:
    """Calculate the sum of the digits of a number."""
    return sum(int(d) for d in str(n))

async def fetch_fun_fact(number: int) -> str:
    """Fetch fun fact from Numbers API asynchronously."""
    if number in FUN_FACT_CACHE:
        return FUN_FACT_CACHE[number]

    try:
        response = await asyncio.to_thread(requests.get, f"http://numbersapi.com/{number}/math?json")
        fun_fact = response.json().get("text", "No fun fact available.")
        FUN_FACT_CACHE[number] = fun_fact  # Cache the result
        return fun_fact
    except requests.RequestException:
        return "No fun fact available."

@app.get("/api/classify-number")
async def classify_number(number: int = Query(..., description="The number to classify")):
    if not isinstance(number, int):
        raise HTTPException(status_code=400, detail={"number": str(number), "error": True})

    # Run computations concurrently
    properties = []
    is_armstrong_result = is_armstrong(number)
    is_even = number % 2 == 0

    if is_armstrong_result:
        properties.append("armstrong")
    if is_even:
        properties.append("even")
    else:
        properties.append("odd")

    # Fetch fun fact asynchronously
    fun_fact = await fetch_fun_fact(number)

    return {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": digit_sum(number),
        "fun_fact": fun_fact,
    }