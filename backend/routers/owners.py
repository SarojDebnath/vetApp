from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from backend.models.database import Owner, get_db_session
from backend.models.schemas import Owner as OwnerSchema, OwnerCreate, OwnerUpdate

router = APIRouter(
    prefix="/api/owners",
    tags=["owners"]
)

@router.get("/", response_model=List[OwnerSchema])
def get_owners(
    skip: int = 0, 
    limit: int = 100, 
    search: str = None,
    db: Session = Depends(get_db_session)
):
    """Get all owners with optional search"""
    query = db.query(Owner)
    
    if search:
        query = query.filter(Owner.name.like(f"%{search}%"))
    
    return query.offset(skip).limit(limit).all()

@router.get("/{owner_id}", response_model=OwnerSchema)
def get_owner(owner_id: int, db: Session = Depends(get_db_session)):
    """Get a specific owner by ID"""
    owner = db.query(Owner).filter(Owner.id == owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    return owner

@router.post("/", response_model=OwnerSchema)
def create_owner(owner: OwnerCreate, db: Session = Depends(get_db_session)):
    """Create a new owner"""
    db_owner = Owner(**owner.dict())
    db.add(db_owner)
    db.commit()
    db.refresh(db_owner)
    return db_owner

@router.put("/{owner_id}", response_model=OwnerSchema)
def update_owner(owner_id: int, owner: OwnerUpdate, db: Session = Depends(get_db_session)):
    """Update an existing owner"""
    db_owner = db.query(Owner).filter(Owner.id == owner_id).first()
    if not db_owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    
    for key, value in owner.dict(exclude_unset=True).items():
        setattr(db_owner, key, value)
    
    db.commit()
    db.refresh(db_owner)
    return db_owner

@router.delete("/{owner_id}")
def delete_owner(owner_id: int, db: Session = Depends(get_db_session)):
    """Delete an owner"""
    db_owner = db.query(Owner).filter(Owner.id == owner_id).first()
    if not db_owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    
    db.delete(db_owner)
    db.commit()
    return {"message": "Owner deleted successfully"} 