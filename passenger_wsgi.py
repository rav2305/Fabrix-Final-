import sys
import os

# Add application directory to the Python search path
sys.path.insert(0, os.path.dirname(__file__))

# Import the Flask application instance as 'application' (as expected by Passenger)
from app import app as application
