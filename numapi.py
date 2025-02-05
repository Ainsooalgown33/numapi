import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Function to check if a number is prime
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# Function to check if a number is perfect
def is_perfect(n):
    return n > 1 and sum(i for i in range(1, n) if n % i == 0) == n

# Function to check if a number is an Armstrong number
def is_armstrong(n):
    digits = [int(d) for d in str(n)]
    return sum(d ** len(digits) for d in digits) == n

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    num = request.args.get("number")
    
    # Validate input
    if not num or not num.isdigit():
        return jsonify({"number": num, "error": True}), 400

    num = int(num)
    
    # Get properties
    properties = ["odd" if num % 2 else "even"]
    if is_armstrong(num):
        properties.insert(0, "armstrong")

    # Fetch fun fact
    fun_fact = requests.get(f"http://numbersapi.com/{num}/math").text
    
    # Return response
    return jsonify({
        "number": num,
        "is_prime": is_prime(num),
        "is_perfect": is_perfect(num),
        "properties": properties,
        "digit_sum": sum(int(d) for d in str(num)),
        "fun_fact": fun_fact
    })

if __name__ == "__main__":
    app.run()
