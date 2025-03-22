# Veterinary Clinic Management Application

A comprehensive web-based application for managing veterinary clinic operations, including patient records, prescriptions, and visit history.

## Features

- **Owner and Pet Management**: Store and retrieve owner and pet information
- **Visit Records**: Record complaints, examinations, treatments, and tests
- **Medication Management**: Suggest medications with usage tracking
- **PDF Generation**: Generate and print prescription PDFs
- **Visit History**: View and reuse previous visit data
- **Next Visit Scheduling**: Schedule and track follow-up visits

## Application Structure

The application follows a modern web architecture with:

### Backend (FastAPI)

- **Models**: SQLAlchemy ORM for database operations (SQLite)
- **Schemas**: Pydantic models for data validation
- **Routers**: API endpoints for all CRUD operations
- **Utils**: PDF generation and configuration management

### Frontend (HTML/CSS/JavaScript)

- **HTML**: Modern, responsive UI
- **CSS**: Clean, user-friendly styling
- **JavaScript**: Client-side functionality and API interaction

## Installation

1. Clone the repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python run.py
   ```

This will start the application and automatically open it in your default web browser.

## Requirements

- Python 3.8+
- FastAPI
- SQLAlchemy
- ReportLab
- Uvicorn
- SQLite3

## Usage

1. Enter owner and pet information
2. Record complaint, examination, treatment, and tests
3. Schedule next visit if needed
4. Save and print the prescription
5. View pet history for future visits

## Configuration

The application stores configuration in `vet_app_config.json`. You can change the save folder for PDFs through the application interface.

## Database

The application uses SQLite for data storage. The database file is stored in the configured save folder or the current working directory if no save folder is specified.

## License

This project is licensed under the MIT License. 