import requests
import os
import time

print("Connection test script")
print("=====================")

# Wait for server to fully start
print("Waiting for server to start (2 seconds)...")
time.sleep(2)

# Test health endpoint
try:
    health_response = requests.get("http://localhost:8000/health")
    print(f"Health endpoint status: {health_response.status_code}")
    print(f"Response: {health_response.json()}")
except Exception as e:
    print(f"Error connecting to health endpoint: {e}")

# Test config endpoint
try:
    config_response = requests.get("http://localhost:8000/api/config")
    print(f"Config endpoint status: {config_response.status_code}")
    print(f"Response: {config_response.json()}")
except Exception as e:
    print(f"Error connecting to config endpoint: {e}")

# Test static files
try:
    static_response = requests.get("http://localhost:8000/static/js/app.js")
    print(f"Static file status: {static_response.status_code}")
    print(f"Content length: {len(static_response.text)} bytes")
except Exception as e:
    print(f"Error accessing static files: {e}")

# Check for storage directory
storage_dir = os.path.join(os.getcwd(), "frontend", "static", "storage")
if os.path.exists(storage_dir):
    print(f"Storage directory exists: {storage_dir}")
    print(f"Contents: {os.listdir(storage_dir)}")
else:
    print(f"Storage directory does not exist: {storage_dir}")
    
print("\nTest complete") 