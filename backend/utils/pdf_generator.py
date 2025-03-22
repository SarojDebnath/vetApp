from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime
import os
import subprocess
import shutil

class PDFGenerator:
    def __init__(self, save_folder=None):
        """Initialize the PDF generator with a save folder"""
        # Default to the 'storage' directory in the project root
        self.save_folder = save_folder or os.path.join(os.getcwd(), 'storage')
        
        # Ensure directory exists
        if not os.path.exists(self.save_folder):
            os.makedirs(self.save_folder)
            
        # Create a folder to make the files accessible via static
        self.static_storage = os.path.join(os.getcwd(), 'frontend', 'static', 'storage')
        if not os.path.exists(self.static_storage):
            os.makedirs(self.static_storage)
        
        print(f"PDF Generator initialized with save folder: {self.save_folder}")
        print(f"Static storage path: {self.static_storage}")
    
    def generate_prescription(self, data):
        """Generate a prescription PDF from the provided data"""
        # Create unique filename for the PDF
        current_date = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"prescription_{data.get('serial_number', current_date)}.pdf"
        file_path = os.path.join(self.save_folder, filename)
        
        # Also create a copy in the static directory
        static_path = os.path.join(self.static_storage, filename)
        
        print(f"Generating PDF at: {file_path}")
        print(f"Static copy will be at: {static_path}")
        
        # Create the PDF document
        doc = SimpleDocTemplate(file_path, pagesize=letter)
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Heading1', fontSize=16, alignment=1, spaceAfter=12))
        styles.add(ParagraphStyle(name='Normal', fontSize=12, spaceAfter=6))
        styles.add(ParagraphStyle(name='Indent', fontSize=12, leftIndent=20, spaceAfter=6))
        
        # Store the flowable elements
        elements = []
        
        # Add title
        elements.append(Paragraph("Veterinary Prescription", styles["Heading1"]))
        elements.append(Spacer(1, 0.25 * inch))
        
        # Add date and serial number
        date_text = f"Date: {data.get('date', datetime.now().strftime('%Y-%m-%d'))}"
        serial_text = f"Serial Number: {data.get('serial_number', '')}"
        elements.append(Paragraph(date_text, styles["Normal"]))
        elements.append(Paragraph(serial_text, styles["Normal"]))
        elements.append(Spacer(1, 0.1 * inch))
        
        # Add owner and pet information
        owner_text = f"Owner: {data.get('owner_name', '')}"
        address_text = f"Address: {data.get('owner_address', '')}"
        phone_text = f"Phone: {data.get('owner_phone', '')}"
        
        pet_text = f"Pet: {data.get('pet_name', '')}"
        species_text = f"Species: {data.get('pet_species', '')}"
        breed_text = f"Breed: {data.get('pet_breed', '')}"
        age_text = f"Age: {data.get('pet_age', '')}"
        sex_text = f"Sex: {data.get('pet_sex', '')}"
        
        # Create owner information table
        owner_data = [
            [Paragraph(owner_text, styles["Normal"]), Paragraph(pet_text, styles["Normal"])],
            [Paragraph(address_text, styles["Normal"]), Paragraph(species_text, styles["Normal"])],
            [Paragraph(phone_text, styles["Normal"]), Paragraph(breed_text, styles["Normal"])],
            ["", Paragraph(f"{age_text}, {sex_text}", styles["Normal"])],
        ]
        
        owner_table = Table(owner_data, colWidths=[3 * inch, 3 * inch])
        owner_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ]))
        
        elements.append(owner_table)
        elements.append(Spacer(1, 0.2 * inch))
        
        # Add complaint, examination, treatment, and tests information
        sections = [
            ("Complaint", data.get('complaint', '')),
            ("Examination", data.get('examination', '')),
            ("Treatment", data.get('treatment', '')),
            ("Tests", data.get('tests', ''))
        ]
        
        for title, content in sections:
            if content:
                elements.append(Paragraph(f"<b>{title}:</b>", styles["Normal"]))
                elements.append(Paragraph(content, styles["Indent"]))
                elements.append(Spacer(1, 0.1 * inch))
        
        # Add next visit information
        next_visit = data.get('next_visit', '')
        if next_visit:
            elements.append(Paragraph("<b>Next Visit:</b>", styles["Normal"]))
            elements.append(Paragraph(next_visit, styles["Indent"]))
        
        # Build the PDF
        try:
            doc.build(elements)
            print(f"PDF created successfully at: {file_path}")
        except Exception as e:
            print(f"Error creating PDF: {e}")
            return None
        
        # Copy the file to the static directory
        try:
            if os.path.exists(file_path):
                shutil.copy2(file_path, static_path)
                print(f"PDF copied to static directory: {static_path}")
            else:
                print(f"Error: PDF file not found at {file_path}")
                return None
        except Exception as e:
            print(f"Error copying PDF to static directory: {e}")
            return None
        
        # Return the URL path for frontend access - fix the path to make it web-accessible
        web_path = static_path.replace(os.path.join(os.getcwd(), 'frontend'), '')
        web_path = web_path.replace('\\', '/')  # Convert Windows backslashes to forward slashes for URL
        
        # Ensure the path starts with /static
        if not web_path.startswith('/static'):
            web_path = '/static' + web_path
        
        print(f"Returning web path: {web_path}")
        return web_path
    
    def print_pdf(self, file_path):
        """Print a PDF file using the default system printer"""
        try:
            if os.name == 'nt':  # Windows
                os.startfile(file_path, 'print')
            elif os.name == 'posix':  # macOS, Linux
                if os.path.exists('/usr/bin/lpr'):
                    subprocess.run(['lpr', file_path])
                else:
                    return False
            return True
        except Exception as e:
            print(f"Error printing PDF: {e}")
            return False 