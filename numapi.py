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
    digits = [int(d) for d in str(abs(n))]  # Handle negative numbers
    length = len(digits)
    return sum(d ** length for d in digits) == abs(n)

def digit_sum(n):
    """Calculate the sum of the digits of a number."""
    return sum(int(d) for d in str(abs(n)))  # Handle negative numbers

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
    # Get the number from query parameters
    number = request.args.get('number')
    app.logger.debug(f"Received request with number: {number}")

    # Input validation
    if not number:
        # Default to 2 if no number is provided
        number = 2
    else:
        # Check if the input is a valid integer
        try:
            number = int(number)
        except ValueError:
            return jsonify({
                "number": number,
                "error": True
            }), 400

    # Calculate properties for the number
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
        "is_prime": is_prime(abs(number)),  # Handle negative numbers
        "is_perfect": is_perfect(abs(number)),  # Handle negative numbers
        "properties": properties,
        "digit_sum": digit_sum(number),
        "fun_fact": get_fun_fact(number)
    }

    return jsonify(response)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)