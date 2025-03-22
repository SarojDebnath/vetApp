# Veterinary Clinic Management - Standalone Application

This document provides instructions for deploying and using the standalone version of the Veterinary Clinic Management application.

## Deployment Instructions

### Building the Standalone Application

1. Install the required Python dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the build script:
   ```
   python build.py
   ```

3. The standalone application will be created in the `dist/VeterinaryClinic` directory.

### Deploying to Another PC

1. Copy the entire `VeterinaryClinic` folder from the `dist` directory to the target PC.
2. (Optional) Create a shortcut to `VeterinaryClinic.exe` on the desktop or Start Menu.

## Using the Application

1. On the target PC, double-click `VeterinaryClinic.exe` to start the application.
2. The application will automatically open in the default web browser.
3. If the browser doesn't open automatically, navigate to `http://localhost:8000` in any web browser.

## Important Notes

- The application runs a local web server on port 8000. This port must be available.
- All data is stored locally in a SQLite database file (`vet_app.db`) within the application directory.
- PDF prescriptions are saved in the `storage` directory within the application folder.
- No internet connection is required - everything runs locally on the PC.

## Troubleshooting

- If the application doesn't start, check that no other program is using port 8000.
- If the browser doesn't open automatically, try manually navigating to `http://localhost:8000`.
- The application creates log files in the same directory. Check these for any error information. 