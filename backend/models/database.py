from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import os

Base = declarative_base()

class Owner(Base):
    __tablename__ = "owners"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String)
    phone = Column(String)
    
    pets = relationship("Pet", back_populates="owner", cascade="all, delete-orphan")

class Pet(Base):
    __tablename__ = "pets"
    
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("owners.id"))
    name = Column(String, nullable=False)
    species = Column(String)
    breed = Column(String)
    age = Column(String)
    sex = Column(String)
    
    owner = relationship("Owner", back_populates="pets")
    visits = relationship("Visit", back_populates="pet", cascade="all, delete-orphan")

class Visit(Base):
    __tablename__ = "visits"
    
    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey("pets.id"))
    date = Column(String)
    serial_number = Column(String)
    complaint = Column(Text)
    examination = Column(Text)
    treatment = Column(Text)
    tests = Column(Text)
    next_visit = Column(String)
    
    pet = relationship("Pet", back_populates="visits")

class Medication(Base):
    __tablename__ = "medications"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(Text)
    dosage = Column(String)
    usage_count = Column(Integer, default=0)

class Species(Base):
    __tablename__ = "species"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

def get_db_session(db_path="vet_app.db"):
    # Ensure parent directory exists
    if not os.path.exists(os.path.dirname(db_path)) and os.path.dirname(db_path):
        os.makedirs(os.path.dirname(db_path))
        
    # Create engine and session
    engine = create_engine(f"sqlite:///{db_path}")
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    return SessionLocal()

def add_default_data(db_session):
    # Add default medications if they don't exist
    default_medications = [
        {"name": "Amoxicillin", "description": "Antibiotic", "dosage": "10-20 mg/kg q12h"},
        {"name": "Carprofen", "description": "NSAID", "dosage": "2-4 mg/kg q24h"},
        {"name": "Prednisone", "description": "Corticosteroid", "dosage": "0.5-1 mg/kg q24h"},
        {"name": "Metronidazole", "description": "Antiprotozoal", "dosage": "10-15 mg/kg q12h"},
        {"name": "Doxycycline", "description": "Antibiotic", "dosage": "5 mg/kg q12h"}
    ]
    
    for med_data in default_medications:
        medication = db_session.query(Medication).filter_by(name=med_data["name"]).first()
        if not medication:
            medication = Medication(**med_data)
            db_session.add(medication)
    
    # Add default species if they don't exist
    default_species = ["Dog", "Cat", "Bird", "Rabbit", "Hamster", "Guinea Pig", "Ferret", "Reptile"]
    
    for species_name in default_species:
        species = db_session.query(Species).filter_by(name=species_name).first()
        if not species:
            species = Species(name=species_name)
            db_session.add(species)
    
    db_session.commit() 