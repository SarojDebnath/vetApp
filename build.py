import PyInstaller.__main__
import os
import shutil

# Create output directory if it doesn't exist
if not os.path.exists('dist'):
    os.makedirs('dist')

# Define application icon
icon_path = 'logo.ico'

# Run PyInstaller
PyInstaller.__main__.run([
    'run.py',                      # Script to package
    '--name=VeterinaryClinic',     # Name of the application
    '--onedir',                    # Create a directory with the executable
    '--windowed',                  # Run without console window (for Windows)
    f'--icon={icon_path}',         # Application icon
    '--add-data=frontend:frontend',# Include frontend files
    '--hidden-import=uvicorn.logging',
    '--hidden-import=uvicorn.lifespan.on',
    '--hidden-import=uvicorn.lifespan',
    '--hidden-import=uvicorn.protocols.http.auto',
    '--collect-all=backend',       # Include all backend modules
])

# Define dist directory
dist_dir = os.path.join('dist', 'VeterinaryClinic')

# Copy SQLite database if it exists
if os.path.exists('vet_app.db'):
    shutil.copy('vet_app.db', os.path.join(dist_dir, 'vet_app.db'))
    print("Copied database file")

# Copy configuration if it exists
if os.path.exists('vet_app_config.json'):
    shutil.copy('vet_app_config.json', os.path.join(dist_dir, 'vet_app_config.json'))
    print("Copied configuration file")

# Copy shortcut creation script
shutil.copy('create_shortcut.bat', os.path.join(dist_dir, 'create_shortcut.bat'))
print("Copied shortcut creation script")

# Copy distribution documentation
shutil.copy('DISTRIBUTION.md', os.path.join(dist_dir, 'README.md'))
print("Copied distribution documentation")

# Create storage directory in dist
storage_dir = os.path.join(dist_dir, 'storage')
if not os.path.exists(storage_dir):
    os.makedirs(storage_dir)
    print("Created storage directory")

print("\nBuild completed successfully!")
print(f"The standalone application is in the '{dist_dir}' directory.")
print("To deploy to another PC, copy the entire VeterinaryClinic folder.")
print("On the target PC, run 'create_shortcut.bat' to create a desktop shortcut.") 