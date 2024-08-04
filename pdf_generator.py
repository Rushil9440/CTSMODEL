from fpdf import FPDF

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Medical Report', 0, 1, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln(5)

    def add_section(self, title, body):
        self.chapter_title(title)
        self.chapter_body(body)


def generate_pdf(user_record):
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)
    
    pdf.add_section("Patient Information", f"Name: {user_record['name']}\nAge:{user_record['age']}")

    report_content = {
        'Predicted Disease': user_record['disease'],
        'Description': user_record['description'],
        'Precautions': user_record['precautions'],
        'Medications': user_record['medications'],
        'Diet': user_record['diet'],
        'Workout': user_record['workout'],
        'Personalized Advice':user_record['Personalized Advice']
    }
    for title,content in report_content.items():
        pdf.add_section(title,content)
    pdf.output('medical_report.pdf')
