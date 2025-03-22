from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import os
from pydantic import BaseModel

from backend.routers import owners, pets, visits, medications, species
from backend.models.database import get_db_session, add_default_data
from backend.utils.config import ConfigManager
from backend.utils.pdf_generator import PDFGenerator

# Create FastAPI app
app = FastAPI(title="Veterinary Clinic API", 
              description="API for the Veterinary Clinic Management System",
              version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, you would restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(owners.router)
app.include_router(pets.router)
app.include_router(visits.router)
app.include_router(medications.router)
app.include_router(species.router)

# Configuration model
class ConfigUpdate(BaseModel):
    save_folder: str

@app.get("/api/config")
def get_config():
    """Get current configuration"""
    try:
        config_manager = ConfigManager()
        print(f"Retrieved config: {config_manager.config}")
        return config_manager.config
    except Exception as e:
        print(f"Error getting config: {e}")
        return {"error": f"Failed to get configuration: {str(e)}"}

@app.post("/api/config")
def update_config(config_update: ConfigUpdate):
    """Update configuration"""
    try:
        config_manager = ConfigManager()
        
        # Validate folder path
        if not os.path.exists(config_update.save_folder):
            try:
                print(f"Creating directory: {config_update.save_folder}")
                os.makedirs(config_update.save_folder)
                print(f"Directory created: {config_update.save_folder}")
            except Exception as e:
                error_msg = f"Could not create folder: {str(e)}"
                print(error_msg)
                return {"error": error_msg}
        
        # Update config
        config_manager.config.update({"save_folder": config_update.save_folder})
        config_manager.save_config()
        
        print(f"Config updated successfully: {config_manager.config}")
        return {"status": "ok", "config": config_manager.config}
    except Exception as e:
        error_msg = f"Failed to update configuration: {str(e)}"
        print(error_msg)
        return {"error": error_msg}

@app.get("/api/test-pdf")
def test_pdf_generation():
    """Test PDF generation and folder configuration"""
    try:
        # Get configuration
        config_manager = ConfigManager()
        save_folder = config_manager.config.get("save_folder")
        
        # Create PDF generator
        pdf_generator = PDFGenerator(save_folder)
        
        # Test PDF generation with sample data
        sample_data = {
            "date": "2025-03-22",
            "serial_number": "test-123",
            "owner_name": "Test Owner",
            "owner_address": "123 Test Street",
            "owner_phone": "555-1234",
            "pet_name": "Test Pet",
            "pet_species": "Dog",
            "pet_breed": "Test Breed",
            "pet_age": "2 years",
            "pet_sex": "Male",
            "complaint": "Test complaint",
            "examination": "Test examination",
            "treatment": "Test treatment",
            "tests": "Test tests",
            "next_visit": "2025-04-22"
        }
        
        pdf_path = pdf_generator.generate_prescription(sample_data)
        
        if not pdf_path:
            return {"status": "error", "message": "Failed to generate PDF"}
        
        return {
            "status": "success", 
            "pdf_path": pdf_path,
            "save_folder": save_folder,
            "static_folder": os.path.join(os.getcwd(), 'frontend', 'static', 'storage')
        }
        
    except Exception as e:
        print(f"Error testing PDF generation: {e}")
        return {"status": "error", "message": str(e)}

# Initialize default data
@app.on_event("startup")
def startup_event():
    db = get_db_session()
    add_default_data(db)

# Mount static files
if os.path.exists("frontend"):
    app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok"} 