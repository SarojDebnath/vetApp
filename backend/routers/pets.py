from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.models.database import Pet, get_db_session
from backend.models.schemas import Pet as PetSchema, PetCreate, PetUpdate

router = APIRouter(
    prefix="/api/pets",
    tags=["pets"]
)

@router.get("/", response_model=List[PetSchema])
def get_pets(
    skip: int = 0, 
    limit: int = 100, 
    owner_id: int = None,
    search: str = None,
    db: Session = Depends(get_db_session)
):
    """Get all pets with optional filters"""
    query = db.query(Pet)
    
    if owner_id:
        query = query.filter(Pet.owner_id == owner_id)
    
    if search:
        query = query.filter(Pet.name.like(f"%{search}%"))
    
    return query.offset(skip).limit(limit).all()

@router.get("/{pet_id}", response_model=PetSchema)
def get_pet(pet_id: int, db: Session = Depends(get_db_session)):
    """Get a specific pet by ID"""
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet

@router.post("/", response_model=PetSchema)
def create_pet(pet: PetCreate, db: Session = Depends(get_db_session)):
    """Create a new pet"""
    db_pet = Pet(**pet.dict())
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return db_pet

@router.put("/{pet_id}", response_model=PetSchema)
def update_pet(pet_id: int, pet: PetUpdate, db: Session = Depends(get_db_session)):
    """Update an existing pet"""
    db_pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not db_pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    
    for key, value in pet.dict(exclude_unset=True).items():
        setattr(db_pet, key, value)
    
    db.commit()
    db.refresh(db_pet)
    return db_pet

@router.delete("/{pet_id}")
def delete_pet(pet_id: int, db: Session = Depends(get_db_session)):
    """Delete a pet"""
    db_pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not db_pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    
    db.delete(db_pet)
    db.commit()
    return {"message": "Pet deleted successfully"} 