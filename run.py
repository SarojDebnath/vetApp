import uvicorn
import webbrowser
import threading
import time
import os
import sys
import socket
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("vet_app.log"),
        logging.StreamHandler()
    ]
)

def is_port_available(port):
    """Check if a port is available"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("127.0.0.1", port))
            return True
    except:
        return False

def open_browser(port):
    """Open the browser after a short delay to allow the server to start"""
    time.sleep(2)
    try:
        webbrowser.open(f'http://localhost:{port}')
        logging.info(f"Opened web browser to http://localhost:{port}")
    except Exception as e:
        logging.error(f"Failed to open browser: {e}")
        print(f"Please open your web browser and navigate to http://localhost:{port}")

def get_application_path():
    """Get the path to the application directory"""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        return os.path.dirname(sys.executable)
    else:
        # Running as script
        return os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    try:
        # Set the working directory to the application directory
        app_path = get_application_path()
        os.chdir(app_path)
        logging.info(f"Working directory set to: {app_path}")
        
        # Create necessary directories if they don't exist
        storage_path = os.path.join(app_path, "storage")
        if not os.path.exists(storage_path):
            os.makedirs(storage_path)
            logging.info(f"Created storage directory: {storage_path}")
        
        # Find an available port (try 8000 first, then look for others)
        port = 8000
        while not is_port_available(port) and port < 8020:
            port += 1
            
        if port >= 8020:
            logging.error("Could not find an available port in range 8000-8019")
            print("Could not find an available port. Please close other applications and try again.")
            input("Press Enter to exit...")
            sys.exit(1)
        
        logging.info(f"Using port: {port}")
        
        # Start browser in a separate thread
        threading.Thread(target=open_browser, args=(port,)).start()
        
        # Start the FastAPI server
        logging.info("Starting FastAPI server")
        uvicorn.run("backend.main:app", host="0.0.0.0", port=port, log_level="warning")
    
    except Exception as e:
        logging.error(f"Application failed to start: {e}")
        print(f"Application failed to start: {e}")
        input("Press Enter to exit...")
        sys.exit(1) 