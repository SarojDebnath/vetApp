from pydantic import BaseModel
from typing import List, Optional

# Owner schemas
class OwnerBase(BaseModel):
    name: str
    address: Optional[str] = None
    phone: Optional[str] = None

class OwnerCreate(OwnerBase):
    pass

class OwnerUpdate(OwnerBase):
    name: Optional[str] = None

class OwnerInDB(OwnerBase):
    id: int
    
    class Config:
        orm_mode = True

class Owner(OwnerInDB):
    pass

# Pet schemas
class PetBase(BaseModel):
    name: str
    species: Optional[str] = None
    breed: Optional[str] = None
    age: Optional[str] = None
    sex: Optional[str] = None

class PetCreate(PetBase):
    owner_id: int

class PetUpdate(PetBase):
    name: Optional[str] = None
    owner_id: Optional[int] = None

class PetInDB(PetBase):
    id: int
    owner_id: int
    
    class Config:
        orm_mode = True

class Pet(PetInDB):
    pass

# Visit schemas
class VisitBase(BaseModel):
    date: str
    serial_number: str
    complaint: Optional[str] = None
    examination: Optional[str] = None
    treatment: Optional[str] = None
    tests: Optional[str] = None
    next_visit: Optional[str] = None

class VisitCreate(VisitBase):
    pet_id: int

class VisitUpdate(VisitBase):
    date: Optional[str] = None
    serial_number: Optional[str] = None
    pet_id: Optional[int] = None

class VisitInDB(VisitBase):
    id: int
    pet_id: int
    
    class Config:
        orm_mode = True

class Visit(VisitInDB):
    pass

# Medication schemas
class MedicationBase(BaseModel):
    name: str
    description: Optional[str] = None
    dosage: Optional[str] = None
    usage_count: Optional[int] = 0

class MedicationCreate(MedicationBase):
    pass

class MedicationUpdate(MedicationBase):
    name: Optional[str] = None

class MedicationInDB(MedicationBase):
    id: int
    
    class Config:
        orm_mode = True

class Medication(MedicationInDB):
    pass

# Species schemas
class SpeciesBase(BaseModel):
    name: str

class SpeciesCreate(SpeciesBase):
    pass

class SpeciesUpdate(SpeciesBase):
    pass

class SpeciesInDB(SpeciesBase):
    id: int
    
    class Config:
        orm_mode = True

class Species(SpeciesInDB):
    pass

# Combined data schemas for forms
class VisitData(BaseModel):
    owner_name: str
    owner_address: Optional[str] = None
    owner_phone: Optional[str] = None
    pet_name: str
    pet_species: Optional[str] = None
    pet_breed: Optional[str] = None
    pet_age: Optional[str] = None
    pet_sex: Optional[str] = None
    complaint: Optional[str] = None
    examination: Optional[str] = None
    treatment: Optional[str] = None
    tests: Optional[str] = None
    next_visit: Optional[str] = None 