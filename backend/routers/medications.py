from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.models.database import Medication, get_db_session
from backend.models.schemas import Medication as MedicationSchema, MedicationCreate, MedicationUpdate

router = APIRouter(
    prefix="/api/medications",
    tags=["medications"]
)

@router.get("/", response_model=List[MedicationSchema])
def get_medications(
    skip: int = 0, 
    limit: int = 100, 
    search: str = None,
    db: Session = Depends(get_db_session)
):
    """Get all medications with optional search"""
    query = db.query(Medication)
    
    if search:
        query = query.filter(Medication.name.like(f"%{search}%"))
    
    # Sort by usage count descending
    query = query.order_by(Medication.usage_count.desc())
    
    return query.offset(skip).limit(limit).all()

@router.get("/{medication_id}", response_model=MedicationSchema)
def get_medication(medication_id: int, db: Session = Depends(get_db_session)):
    """Get a specific medication by ID"""
    medication = db.query(Medication).filter(Medication.id == medication_id).first()
    if not medication:
        raise HTTPException(status_code=404, detail="Medication not found")
    return medication

@router.post("/", response_model=MedicationSchema)
def create_medication(medication: MedicationCreate, db: Session = Depends(get_db_session)):
    """Create a new medication"""
    db_medication = Medication(**medication.dict())
    db.add(db_medication)
    db.commit()
    db.refresh(db_medication)
    return db_medication

@router.put("/{medication_id}", response_model=MedicationSchema)
def update_medication(medication_id: int, medication: MedicationUpdate, db: Session = Depends(get_db_session)):
    """Update an existing medication"""
    db_medication = db.query(Medication).filter(Medication.id == medication_id).first()
    if not db_medication:
        raise HTTPException(status_code=404, detail="Medication not found")
    
    for key, value in medication.dict(exclude_unset=True).items():
        setattr(db_medication, key, value)
    
    db.commit()
    db.refresh(db_medication)
    return db_medication

@router.delete("/{medication_id}")
def delete_medication(medication_id: int, db: Session = Depends(get_db_session)):
    """Delete a medication"""
    db_medication = db.query(Medication).filter(Medication.id == medication_id).first()
    if not db_medication:
        raise HTTPException(status_code=404, detail="Medication not found")
    
    db.delete(db_medication)
    db.commit()
    return {"message": "Medication deleted successfully"}

@router.post("/{medication_name}/use")
def increment_medication_usage(medication_name: str, db: Session = Depends(get_db_session)):
    """Increment the usage count for a medication"""
    medication = db.query(Medication).filter(Medication.name == medication_name).first()
    if not medication:
        raise HTTPException(status_code=404, detail="Medication not found")
    
    medication.usage_count += 1
    db.commit()
    
    return {"message": f"Usage count for {medication_name} increased to {medication.usage_count}"} 