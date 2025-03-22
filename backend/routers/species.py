from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.models.database import Species, get_db_session
from backend.models.schemas import Species as SpeciesSchema, SpeciesCreate, SpeciesUpdate

router = APIRouter(
    prefix="/api/species",
    tags=["species"]
)

@router.get("/", response_model=List[SpeciesSchema])
def get_all_species(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db_session)
):
    """Get all species"""
    return db.query(Species).offset(skip).limit(limit).all()

@router.get("/{species_id}", response_model=SpeciesSchema)
def get_species(species_id: int, db: Session = Depends(get_db_session)):
    """Get a specific species by ID"""
    species = db.query(Species).filter(Species.id == species_id).first()
    if not species:
        raise HTTPException(status_code=404, detail="Species not found")
    return species

@router.post("/", response_model=SpeciesSchema)
def create_species(species: SpeciesCreate, db: Session = Depends(get_db_session)):
    """Create a new species"""
    # Check if species with same name already exists
    existing_species = db.query(Species).filter(Species.name == species.name).first()
    if existing_species:
        raise HTTPException(status_code=400, detail="Species with this name already exists")
    
    db_species = Species(**species.dict())
    db.add(db_species)
    db.commit()
    db.refresh(db_species)
    return db_species

@router.put("/{species_id}", response_model=SpeciesSchema)
def update_species(species_id: int, species: SpeciesUpdate, db: Session = Depends(get_db_session)):
    """Update an existing species"""
    db_species = db.query(Species).filter(Species.id == species_id).first()
    if not db_species:
        raise HTTPException(status_code=404, detail="Species not found")
    
    # If name is being updated, check if it conflicts with existing species
    if species.name and species.name != db_species.name:
        existing_species = db.query(Species).filter(Species.name == species.name).first()
        if existing_species:
            raise HTTPException(status_code=400, detail="Species with this name already exists")
    
    for key, value in species.dict(exclude_unset=True).items():
        setattr(db_species, key, value)
    
    db.commit()
    db.refresh(db_species)
    return db_species

@router.delete("/{species_id}")
def delete_species(species_id: int, db: Session = Depends(get_db_session)):
    """Delete a species"""
    db_species = db.query(Species).filter(Species.id == species_id).first()
    if not db_species:
        raise HTTPException(status_code=404, detail="Species not found")
    
    db.delete(db_species)
    db.commit()
    return {"message": "Species deleted successfully"} 