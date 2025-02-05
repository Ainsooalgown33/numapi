from flask import Flask, jsonify
import requests
import random

app = Flask(__name__)

# Function to check if a number is prime
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# Function to check if a number is a perfect number
def is_perfect(n):
    if n < 2:
        return False
    divisors = [i for i in range(1, n) if n % i == 0]
    return sum(divisors) == n

# Function to check if a number is an Armstrong number
def is_armstrong(n):
    digits = [int(d) for d in str(n)]
    length = len(digits)
    return sum(d**length for d in digits) == n

# Function to calculate the sum of digits
def digit_sum(n):
    return sum(int(d) for d in str(n))

# Function to get a fun fact about the number (using Numbers API)
def get_fun_fact(n):
    url = f"http://numbersapi.com/{n}/math"
    response = requests.get(url)
    return response.text if response.status_code == 200 else "No fun fact available."

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    # Generate a random number between 1 and 1000
    number = random.randint(1, 1000)
    
    # Determine properties
    properties = []
    if is_armstrong(number):
        properties.append("armstrong")
    if number % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")
    
    # Prepare response
    response = {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": digit_sum(number),
        "fun_fact": get_fun_fact(number)
    }
    
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)