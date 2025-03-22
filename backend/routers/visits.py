from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
import os

from backend.models.database import Visit, Owner, Pet, get_db_session
from backend.models.schemas import Visit as VisitSchema, VisitCreate, VisitUpdate, VisitData
from backend.utils.pdf_generator import PDFGenerator
from backend.utils.config import ConfigManager

router = APIRouter(
    prefix="/api/visits",
    tags=["visits"]
)

def get_pdf_generator():
    """Get PDF generator with configured save folder"""
    config_manager = ConfigManager()
    return PDFGenerator(config_manager.config.get("save_folder"))

@router.get("/", response_model=List[VisitSchema])
def get_visits(
    skip: int = 0, 
    limit: int = 100, 
    pet_id: int = None,
    db: Session = Depends(get_db_session)
):
    """Get all visits with optional filters"""
    query = db.query(Visit)
    
    if pet_id:
        query = query.filter(Visit.pet_id == pet_id)
    
    return query.offset(skip).limit(limit).all()

@router.get("/{visit_id}", response_model=VisitSchema)
def get_visit(visit_id: int, db: Session = Depends(get_db_session)):
    """Get a specific visit by ID"""
    visit = db.query(Visit).filter(Visit.id == visit_id).first()
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")
    return visit

@router.post("/", response_model=VisitSchema)
def create_visit(visit: VisitCreate, db: Session = Depends(get_db_session)):
    """Create a new visit"""
    # Ensure date is set
    if not visit.date:
        visit.date = datetime.now().strftime("%Y-%m-%d")
    
    # Ensure serial number is set
    if not visit.serial_number:
        date_prefix = datetime.now().strftime("%Y%m%d")
        # Find highest serial number for today
        last_visit = db.query(Visit).filter(
            Visit.serial_number.like(f"{date_prefix}%")
        ).order_by(Visit.serial_number.desc()).first()
        
        if last_visit and last_visit.serial_number:
            last_number = int(last_visit.serial_number[8:])
            next_number = last_number + 1
        else:
            next_number = 1
        
        visit.serial_number = f"{date_prefix}-{next_number:03d}"
    
    db_visit = Visit(**visit.dict())
    db.add(db_visit)
    db.commit()
    db.refresh(db_visit)
    return db_visit

@router.put("/{visit_id}", response_model=VisitSchema)
def update_visit(visit_id: int, visit: VisitUpdate, db: Session = Depends(get_db_session)):
    """Update an existing visit"""
    db_visit = db.query(Visit).filter(Visit.id == visit_id).first()
    if not db_visit:
        raise HTTPException(status_code=404, detail="Visit not found")
    
    for key, value in visit.dict(exclude_unset=True).items():
        setattr(db_visit, key, value)
    
    db.commit()
    db.refresh(db_visit)
    return db_visit

@router.delete("/{visit_id}")
def delete_visit(visit_id: int, db: Session = Depends(get_db_session)):
    """Delete a visit"""
    db_visit = db.query(Visit).filter(Visit.id == visit_id).first()
    if not db_visit:
        raise HTTPException(status_code=404, detail="Visit not found")
    
    db.delete(db_visit)
    db.commit()
    return {"message": "Visit deleted successfully"}

@router.post("/complete", status_code=201)
def save_complete_visit(
    visit_data: VisitData, 
    db: Session = Depends(get_db_session),
    pdf_generator: PDFGenerator = Depends(get_pdf_generator)
):
    """Save a complete visit with owner and pet information"""
    # Check if owner exists
    owner = db.query(Owner).filter(Owner.name == visit_data.owner_name).first()
    if not owner:
        # Create new owner
        owner = Owner(
            name=visit_data.owner_name,
            address=visit_data.owner_address,
            phone=visit_data.owner_phone
        )
        db.add(owner)
        db.commit()
        db.refresh(owner)
    else:
        # Update owner info if provided
        if visit_data.owner_address:
            owner.address = visit_data.owner_address
        if visit_data.owner_phone:
            owner.phone = visit_data.owner_phone
        db.commit()
    
    # Check if pet exists
    pet = db.query(Pet).filter(
        Pet.name == visit_data.pet_name,
        Pet.owner_id == owner.id
    ).first()
    
    if not pet:
        # Create new pet
        pet = Pet(
            owner_id=owner.id,
            name=visit_data.pet_name,
            species=visit_data.pet_species,
            breed=visit_data.pet_breed,
            age=visit_data.pet_age,
            sex=visit_data.pet_sex
        )
        db.add(pet)
        db.commit()
        db.refresh(pet)
    else:
        # Update pet info if provided
        if visit_data.pet_species:
            pet.species = visit_data.pet_species
        if visit_data.pet_breed:
            pet.breed = visit_data.pet_breed
        if visit_data.pet_age:
            pet.age = visit_data.pet_age
        if visit_data.pet_sex:
            pet.sex = visit_data.pet_sex
        db.commit()
    
    # Create a serial number
    date_prefix = datetime.now().strftime("%Y%m%d")
    # Find highest serial number for today
    last_visit = db.query(Visit).filter(
        Visit.serial_number.like(f"{date_prefix}%")
    ).order_by(Visit.serial_number.desc()).first()
    
    if last_visit and last_visit.serial_number:
        last_number = int(last_visit.serial_number[8:])
        next_number = last_number + 1
    else:
        next_number = 1
    
    serial_number = f"{date_prefix}-{next_number:03d}"
    
    # Create new visit
    visit = Visit(
        pet_id=pet.id,
        date=datetime.now().strftime("%Y-%m-%d"),
        serial_number=serial_number,
        complaint=visit_data.complaint,
        examination=visit_data.examination,
        treatment=visit_data.treatment,
        tests=visit_data.tests,
        next_visit=visit_data.next_visit
    )
    
    db.add(visit)
    db.commit()
    db.refresh(visit)
    
    # Generate PDF
    pdf_data = {
        "date": visit.date,
        "serial_number": visit.serial_number,
        "owner_name": owner.name,
        "owner_address": owner.address,
        "owner_phone": owner.phone,
        "pet_name": pet.name,
        "pet_species": pet.species,
        "pet_breed": pet.breed,
        "pet_age": pet.age,
        "pet_sex": pet.sex,
        "complaint": visit.complaint,
        "examination": visit.examination,
        "treatment": visit.treatment,
        "tests": visit.tests,
        "next_visit": visit.next_visit
    }
    
    pdf_path = pdf_generator.generate_prescription(pdf_data)
    
    # Return result with PDF path
    return {
        "visit_id": visit.id,
        "owner_id": owner.id,
        "pet_id": pet.id,
        "pdf_path": pdf_path
    }

@router.get("/{visit_id}/pdf")
def get_visit_pdf(
    visit_id: int, 
    db: Session = Depends(get_db_session),
    pdf_generator: PDFGenerator = Depends(get_pdf_generator)
):
    """Generate a PDF for an existing visit"""
    # Get visit
    visit = db.query(Visit).filter(Visit.id == visit_id).first()
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")
    
    # Get pet and owner
    pet = db.query(Pet).filter(Pet.id == visit.pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    
    owner = db.query(Owner).filter(Owner.id == pet.owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    
    # Generate PDF
    pdf_data = {
        "date": visit.date,
        "serial_number": visit.serial_number,
        "owner_name": owner.name,
        "owner_address": owner.address,
        "owner_phone": owner.phone,
        "pet_name": pet.name,
        "pet_species": pet.species,
        "pet_breed": pet.breed,
        "pet_age": pet.age,
        "pet_sex": pet.sex,
        "complaint": visit.complaint,
        "examination": visit.examination,
        "treatment": visit.treatment,
        "tests": visit.tests,
        "next_visit": visit.next_visit
    }
    
    pdf_path = pdf_generator.generate_prescription(pdf_data)
    
    return {"pdf_path": pdf_path} 