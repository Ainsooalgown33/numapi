from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import requests
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Helper functions
def is_prime(n):
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    """Check if a number is perfect."""
    if n < 2:
        return False
    divisors = [i for i in range(1, n) if n % i == 0]
    return sum(divisors) == n

def is_armstrong(n):
    """Check if a number is an Armstrong number."""
    digits = [int(d) for d in str(n)]
    length = len(digits)
    return sum(d ** length for d in digits) == n

def digit_sum(n):
    """Calculate the sum of the digits of a number."""
    return sum(int(d) for d in str(n))

def get_fun_fact(n):
    """Fetch a fun fact about the number from numbersapi.com."""
    url = f"http://numbersapi.com/{n}/math"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return "No fun fact available."
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error fetching fun fact: {e}")
        return "No fun fact available."

# Root route
@app.route('/')
def home():
    """Root route to handle requests to the base URL."""
    # Default number to classify if no number is provided
    default_number = 6
    number = default_number

    # Calculate properties for the default number
    properties = []
    if is_prime(number):
        properties.append("prime")
    if is_perfect(number):
        properties.append("perfect")
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

    return jsonify(response)

# API endpoint
@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    """Classify a number and return its properties."""
    number = request.args.get('number')
    app.logger.debug(f"Received request with number: {number}")

    # Input validation
    if not number:
        app.logger.error("Missing 'number' parameter")
        return jsonify({
            "number": "null",
            "error": True
        }), 400

    # Check if the input is a valid integer
    try:
        number = int(number)
    except ValueError:
        app.logger.error(f"Invalid input: {number}")
        return jsonify({
            "number": number,
            "error": True
        }), 400

    # Calculate properties
    properties = []
    if is_prime(number):
        properties.append("prime")
    if is_perfect(number):
        properties.append("perfect")
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

    app.logger.debug(f"Returning response: {response}")
    return jsonify(response), 200

# Run the app
if __name__ == '__main__':
    app.run(debug=True)