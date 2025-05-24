#!/usr/bin/env python3
"""
Diverse Sample Document Generator for Papertrail
Creates realistic documents in PDF, TXT, and DOCX formats with proper formatting.
"""

import os
import random
import io
from datetime import datetime, timedelta
from typing import List, Dict, Tuple

# PDF generation
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

# DOCX generation
from docx import Document as DocxDocument
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

class DiverseDocumentGenerator:
    """Generates realistic documents in multiple formats with proper formatting."""
    
    def __init__(self, output_dir: str = "diverse_sample_documents"):
        self.output_dir = output_dir
        self.setup_data()
        
    def setup_data(self):
        """Setup realistic data for generating documents."""
        self.companies = [
            "TechnoGlobal Solutions Inc", "Meridian Consulting Group", "Apex Digital Systems",
            "Pinnacle Financial Services", "Innovative Research Labs", "Strategic Partners LLC",
            "NextGen Technologies Corp", "Elite Business Solutions", "ProActive Enterprises",
            "Dynamic Consulting Group", "Premier Analytics Inc", "Advanced Systems Ltd"
        ]
        
        self.people = [
            ("John", "Mitchell", "CEO"), ("Sarah", "Chen", "CFO"), ("Michael", "Rodriguez", "CTO"),
            ("Emily", "Thompson", "VP Operations"), ("David", "Kumar", "Legal Counsel"),
            ("Jessica", "Anderson", "HR Director"), ("Robert", "Williams", "Sales Manager"),
            ("Amanda", "Taylor", "Project Manager"), ("James", "Brown", "Senior Analyst"),
            ("Lauren", "Davis", "Marketing Director"), ("Christopher", "Wilson", "Finance Manager"),
            ("Michelle", "Garcia", "Operations Lead")
        ]
        
        self.addresses = [
            ("1250 Tech Park Drive", "San Jose", "CA", "95110"),
            ("890 Business Center Blvd", "Austin", "TX", "78701"),
            ("2100 Corporate Square", "New York", "NY", "10001"),
            ("555 Innovation Way", "Seattle", "WA", "98101"),
            ("1775 Professional Plaza", "Chicago", "IL", "60601"),
            ("3300 Executive Circle", "Dallas", "TX", "75201")
        ]

    def create_output_dir(self):
        """Create output directory structure."""
        os.makedirs(self.output_dir, exist_ok=True)
        for fmt in ['pdf', 'docx', 'txt']:
            os.makedirs(os.path.join(self.output_dir, fmt), exist_ok=True)

    def random_date(self, days_back: int = 365) -> datetime:
        """Generate random date."""
        return datetime.now() - timedelta(days=random.randint(0, days_back))

    def format_currency(self, amount: float) -> str:
        """Format currency amount."""
        return f"${amount:,.2f}"

    def generate_invoice_pdf(self, filename: str) -> str:
        """Generate a professional invoice PDF."""
        filepath = os.path.join(self.output_dir, 'pdf', filename)
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.darkblue
        )
        
        company = random.choice(self.companies)
        invoice_num = f"INV-{random.randint(2023, 2024)}-{random.randint(1000, 9999)}"
        date = self.random_date(90)
        client_company = random.choice([c for c in self.companies if c != company])
        
        # Header
        story.append(Paragraph(f"<b>{company}</b>", title_style))
        story.append(Paragraph("Professional Services Invoice", styles['Heading2']))
        story.append(Spacer(1, 20))
        
        # Invoice details
        details = [
            ['Invoice Number:', invoice_num],
            ['Date:', date.strftime('%B %d, %Y')],
            ['Due Date:', (date + timedelta(days=30)).strftime('%B %d, %Y')],
            ['Bill To:', client_company]
        ]
        
        details_table = Table(details, colWidths=[2*inch, 3*inch])
        details_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(details_table)
        story.append(Spacer(1, 30))
        
        # Services table
        services = [
            ['Description', 'Quantity', 'Rate', 'Amount'],
            ['Professional Consulting Services', '40 hrs', '$150.00', '$6,000.00'],
            ['Technical Documentation', '10 hrs', '$120.00', '$1,200.00'],
            ['Project Management', '20 hrs', '$130.00', '$2,600.00']
        ]
        
        subtotal = 9800.00
        tax = subtotal * 0.0875
        total = subtotal + tax
        
        services.extend([
            ['', '', 'Subtotal:', f'${subtotal:,.2f}'],
            ['', '', 'Sales Tax (8.75%):', f'${tax:,.2f}'],
            ['', '', 'TOTAL DUE:', f'${total:,.2f}']
        ])
        
        services_table = Table(services, colWidths=[3*inch, 1*inch, 1*inch, 1.5*inch])
        services_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (0, 1), (-1, 3), colors.beige),
            ('GRID', (0, 0), (-1, 3), 1, colors.black),
            ('FONTNAME', (2, -3), (-1, -1), 'Helvetica-Bold'),
            ('BACKGROUND', (2, -1), (-1, -1), colors.lightgrey)
        ]))
        
        story.append(services_table)
        story.append(Spacer(1, 30))
        
        # Payment terms
        story.append(Paragraph("<b>Payment Terms:</b> Net 30 days", styles['Normal']))
        story.append(Paragraph("Please remit payment within 30 days of invoice date.", styles['Normal']))
        story.append(Paragraph(f"Account Number: {random.randint(100000, 999999)}", styles['Normal']))
        
        doc.build(story)
        return filepath

    def generate_memo_docx(self, filename: str) -> str:
        """Generate a professional memo DOCX."""
        filepath = os.path.join(self.output_dir, 'docx', filename)
        doc = DocxDocument()
        
        # Header
        header = doc.sections[0].header
        header_para = header.paragraphs[0]
        header_para.text = random.choice(self.companies)
        header_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Title
        title = doc.add_heading('INTERNAL MEMORANDUM', 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Memo header info
        sender_name, sender_last, sender_title = random.choice(self.people)
        memo_date = self.random_date(30)
        
        memo_subjects = [
            "Updated Remote Work Policy Implementation",
            "Q4 Budget Planning and Resource Allocation", 
            "New Employee Onboarding Process Changes",
            "Annual Performance Review Procedures",
            "IT Security Protocol Updates",
            "Office Space Renovation Schedule"
        ]
        
        subject = random.choice(memo_subjects)
        
        # Add memo details
        doc.add_paragraph(f"TO: All Department Managers")
        doc.add_paragraph(f"FROM: {sender_name} {sender_last}, {sender_title}")
        doc.add_paragraph(f"DATE: {memo_date.strftime('%B %d, %Y')}")
        doc.add_paragraph(f"RE: {subject}")
        doc.add_paragraph("")  # Blank line
        
        # Body content
        body_paragraphs = [
            f"This memorandum serves to inform all department managers about important updates regarding {subject.lower()}.",
            "",
            "Key Points:",
            f"• Effective Date: {(memo_date + timedelta(days=14)).strftime('%B %d, %Y')}",
            f"• Implementation Timeline: {random.choice(['2 weeks', '30 days', 'immediate'])}",
            f"• Required Actions: {random.choice(['Complete mandatory training', 'Submit compliance forms', 'Attend briefing sessions'])}",
            f"• Compliance Deadline: {(memo_date + timedelta(days=45)).strftime('%B %d, %Y')}",
            "",
            "Additional Information:",
            random.choice([
                "All affected employees must complete the required training modules by the specified deadline. Failure to comply may result in disciplinary action.",
                "Please review the attached documentation thoroughly and ensure your team follows the new procedures outlined in this memo.",
                "Department heads are responsible for cascading this information to their respective teams and monitoring compliance.",
                "For questions or clarification regarding these changes, please contact the HR department at extension 5500."
            ]),
            "",
            f"Thank you for your attention to this matter. For additional questions, please contact {sender_title} at extension {random.randint(3000, 5999)}.",
            "",
            "Best regards,",
            f"{sender_name} {sender_last}",
            f"{sender_title}"
        ]
        
        for para_text in body_paragraphs:
            para = doc.add_paragraph(para_text)
            if para_text.startswith("•"):
                para.style = 'List Bullet'
        
        doc.save(filepath)
        return filepath

    def generate_contract_txt(self, filename: str) -> str:
        """Generate a professional contract TXT with proper formatting."""
        filepath = os.path.join(self.output_dir, 'txt', filename)
        
        contract_types = [
            "Professional Services Agreement", "Software Development Contract",
            "Consulting Services Agreement", "Non-Disclosure Agreement",
            "Employment Contract", "Vendor Services Agreement"
        ]
        
        contract_type = random.choice(contract_types)
        provider = random.choice(self.companies)
        client = random.choice([c for c in self.companies if c != provider])
        date = self.random_date(60)
        provider_addr = random.choice(self.addresses)
        client_addr = random.choice([a for a in self.addresses if a != provider_addr])
        
        content = f"""
{'='*80}
{contract_type.upper()}
{'='*80}

This {contract_type} ("Agreement") is entered into on {date.strftime('%B %d, %Y')}, 
between {provider} ("Provider") and {client} ("Client").

PROVIDER INFORMATION:
{provider}
{provider_addr[0]}
{provider_addr[1]}, {provider_addr[2]} {provider_addr[3]}

CLIENT INFORMATION:
{client}
{client_addr[0]}
{client_addr[1]}, {client_addr[2]} {client_addr[3]}

{'='*80}
TERMS AND CONDITIONS
{'='*80}

1. SCOPE OF SERVICES
   Provider agrees to provide professional {random.choice(['consulting', 'development', 'analytical', 'technical'])} 
   services as outlined in Schedule A, attached hereto and incorporated by reference.
   
   Services include but are not limited to:
   • {random.choice(['Strategic planning and analysis', 'Software development and maintenance', 'Technical consulting and support'])}
   • {random.choice(['Project management and coordination', 'Quality assurance and testing', 'Documentation and training'])}
   • {random.choice(['Risk assessment and mitigation', 'Performance optimization', 'Compliance and regulatory support'])}

2. TERM AND TERMINATION
   This Agreement shall commence on {date.strftime('%B %d, %Y')} and shall continue 
   for a period of {random.choice([12, 18, 24, 36])} months, unless terminated earlier 
   in accordance with the provisions herein.
   
   Either party may terminate this Agreement with {random.choice([30, 60, 90])} days 
   written notice to the other party.

3. COMPENSATION
   Client agrees to pay Provider a total fee of {self.format_currency(random.randint(50000, 500000))} 
   for the services rendered under this Agreement.
   
   Payment Terms:
   • {random.choice(['Monthly', 'Quarterly', 'Milestone-based'])} payments
   • Net {random.choice([15, 30, 45])} days from invoice date
   • Late payment penalty: 1.5% per month

4. INTELLECTUAL PROPERTY
   All work products, deliverables, and intellectual property created under this 
   Agreement shall be owned by {random.choice(['Client', 'Provider', 'jointly by both parties'])}.

5. CONFIDENTIALITY
   Both parties acknowledge that they may have access to confidential information. 
   Each party agrees to maintain the confidentiality of such information and not 
   to disclose it to third parties without prior written consent.

6. WARRANTIES AND REPRESENTATIONS
   Provider represents and warrants that:
   • It has the authority to enter into this Agreement
   • The services will be performed in a professional manner
   • All work will comply with applicable laws and regulations

7. LIMITATION OF LIABILITY
   In no event shall either party be liable for any indirect, incidental, special, 
   or consequential damages arising out of this Agreement.

8. GOVERNING LAW
   This Agreement shall be governed by and construed in accordance with the laws 
   of the State of {random.choice(['California', 'New York', 'Texas', 'Delaware'])}.

9. ENTIRE AGREEMENT
   This Agreement constitutes the entire agreement between the parties and supersedes 
   all prior negotiations, representations, or agreements relating to the subject matter.

{'='*80}
SIGNATURES
{'='*80}

IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first 
written above.

PROVIDER:                           CLIENT:
{provider:<35} {client}

By: _________________________      By: _________________________
Name: {random.choice(self.people)[0]} {random.choice(self.people)[1]:<22} Name: {random.choice(self.people)[0]} {random.choice(self.people)[1]}
Title: {random.choice(['CEO', 'President', 'COO']):<24} Title: {random.choice(['CEO', 'President', 'COO'])}
Date: ______________________      Date: ______________________

{'='*80}
END OF AGREEMENT
{'='*80}
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filepath

    def generate_legal_pdf(self, filename: str) -> str:
        """Generate a legal document PDF."""
        filepath = os.path.join(self.output_dir, 'pdf', filename)
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        story = []
        styles = getSampleStyleSheet()
        
        # Legal header style
        legal_style = ParagraphStyle(
            'LegalHeader',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=20,
            alignment=1,  # Center
            textColor=colors.black
        )
        
        case_types = [
            "Employment Dispute Resolution", "Breach of Contract Claim",
            "Intellectual Property Violation", "Commercial Litigation Matter",
            "Partnership Dissolution Proceeding", "Regulatory Compliance Issue"
        ]
        
        case_type = random.choice(case_types)
        case_num = f"{random.randint(2023, 2024)}-{random.choice(['CV', 'EMP', 'IP', 'COM', 'REG'])}-{random.randint(1000, 9999)}"
        plaintiff = random.choice(self.companies)
        defendant = random.choice([c for c in self.companies if c != plaintiff])
        court_date = self.random_date(90)
        
        # Document header
        story.append(Paragraph("SUPERIOR COURT OF JUSTICE", legal_style))
        story.append(Paragraph("COMMERCIAL DIVISION", styles['Heading3']))
        story.append(Spacer(1, 30))
        
        # Case information
        case_info = [
            ['Case Number:', case_num],
            ['Case Type:', case_type],
            ['Filing Date:', court_date.strftime('%B %d, %Y')],
            ['Plaintiff:', plaintiff],
            ['Defendant:', defendant]
        ]
        
        case_table = Table(case_info, colWidths=[2*inch, 4*inch])
        case_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        story.append(case_table)
        story.append(Spacer(1, 30))
        
        # Legal notice content
        story.append(Paragraph("<b>NOTICE OF LEGAL PROCEEDINGS</b>", styles['Heading2']))
        story.append(Spacer(1, 15))
        
        legal_content = f"""
TO: {defendant}

TAKE NOTICE that a legal proceeding has been commenced against you by {plaintiff} 
for {case_type.lower()} and associated claims for damages and relief.

NATURE OF CLAIM:
The plaintiff alleges that the defendant has committed the following violations:
• Breach of contractual obligations and failure to perform agreed services
• Violation of confidentiality and non-disclosure agreements  
• Misappropriation of proprietary information and trade secrets
• Interference with business relationships and competitive practices

RELIEF SOUGHT:
The plaintiff seeks the following relief from this Court:
1. Monetary damages in the amount of {self.format_currency(random.randint(100000, 2000000))}
2. Injunctive relief to prevent further violations
3. Restitution of profits and gains wrongfully obtained
4. Pre-judgment and post-judgment interest
5. Attorney fees and costs of litigation
6. Such other relief as the Court deems just and proper

RESPONSE REQUIRED:
Any party wishing to defend this action must file a Statement of Defense within 
{random.choice([20, 30, 45])} days of service of this Notice. Failure to defend may 
result in judgment being granted against you without further notice.

For more information regarding this proceeding, contact the Court Registry or 
legal counsel at the address below.

DATED this {court_date.strftime('%d')} day of {court_date.strftime('%B')}, {court_date.year}.

                                    _________________________________
                                    Registrar, Superior Court of Justice
                                    
Attorney for Plaintiff:
{random.choice(['Thompson & Associates Legal LLP', 'Mitchell, Brown & Partners', 'Sterling Legal Group'])}
{random.choice(self.addresses)[0]}
{random.choice(self.addresses)[1]}, {random.choice(self.addresses)[2]} {random.choice(self.addresses)[3]}
Tel: {random.randint(555, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}
"""
        
        # Split content into paragraphs
        for paragraph in legal_content.strip().split('\n\n'):
            if paragraph.strip():
                story.append(Paragraph(paragraph.strip(), styles['Normal']))
                story.append(Spacer(1, 12))
        
        doc.build(story)
        return filepath

    def generate_report_docx(self, filename: str) -> str:
        """Generate a business report DOCX."""
        filepath = os.path.join(self.output_dir, 'docx', filename)
        doc = DocxDocument()
        
        # Title page
        title = doc.add_heading('QUARTERLY BUSINESS PERFORMANCE REPORT', 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        quarter = random.choice(['Q1', 'Q2', 'Q3', 'Q4'])
        year = random.choice([2023, 2024])
        company = random.choice(self.companies)
        
        doc.add_paragraph(f"{quarter} {year} Executive Summary", style='Heading 1').alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_paragraph(f"{company}", style='Heading 2').alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_paragraph("")
        
        # Executive Summary
        doc.add_heading('EXECUTIVE SUMMARY', level=1)
        
        revenue = random.randint(5000000, 50000000)
        growth = random.randint(-10, 35)
        profit_margin = random.uniform(8, 25)
        
        summary_text = f"""
This report presents the comprehensive business performance analysis for {quarter} {year}, 
highlighting key financial metrics, operational achievements, and strategic initiatives.

Our organization achieved total revenue of {self.format_currency(revenue)} during this quarter, 
representing a {growth}% {'increase' if growth > 0 else 'decrease'} compared to the same period 
last year. The profit margin improved to {profit_margin:.1f}%, demonstrating effective cost 
management and operational efficiency improvements.
"""
        doc.add_paragraph(summary_text.strip())
        
        # Financial Performance
        doc.add_heading('FINANCIAL PERFORMANCE', level=1)
        
        # Create a table for financial data
        table = doc.add_table(rows=1, cols=3)
        table.style = 'Table Grid'
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Metric'
        hdr_cells[1].text = f'{quarter} {year}'
        hdr_cells[2].text = 'YoY Change'
        
        financial_data = [
            ('Total Revenue', self.format_currency(revenue), f"{growth:+.1f}%"),
            ('Operating Expenses', self.format_currency(revenue * 0.7), f"{random.randint(-5, 15):+.1f}%"),
            ('Net Profit', self.format_currency(revenue * profit_margin / 100), f"{random.randint(5, 25):+.1f}%"),
            ('Profit Margin', f"{profit_margin:.1f}%", f"{random.uniform(-2, 5):+.1f}pp")
        ]
        
        for metric, value, change in financial_data:
            row_cells = table.add_row().cells
            row_cells[0].text = metric
            row_cells[1].text = value
            row_cells[2].text = change
        
        # Operational Highlights
        doc.add_heading('OPERATIONAL HIGHLIGHTS', level=1)
        
        highlights = [
            f"Successfully launched {random.randint(2, 5)} new product initiatives",
            f"Expanded market presence in {random.randint(3, 8)} additional regions",
            f"Achieved customer satisfaction score of {random.uniform(4.2, 4.9):.1f}/5.0",
            f"Reduced operational costs by {random.uniform(3, 12):.1f}% through efficiency improvements",
            f"Increased employee retention rate to {random.uniform(85, 95):.1f}%"
        ]
        
        for highlight in highlights:
            doc.add_paragraph(highlight, style='List Bullet')
        
        # Recommendations
        doc.add_heading('STRATEGIC RECOMMENDATIONS', level=1)
        
        recommendations = [
            "Continue investment in high-performing product lines and market segments",
            "Implement advanced analytics tools to enhance decision-making capabilities", 
            "Strengthen customer relationship management and retention programs",
            "Explore strategic partnerships to accelerate market expansion",
            "Invest in employee development and training programs"
        ]
        
        for rec in recommendations:
            doc.add_paragraph(rec, style='List Number')
        
        # Conclusion
        doc.add_heading('CONCLUSION', level=1)
        conclusion = f"""
{quarter} {year} demonstrated {'strong' if growth > 10 else 'stable' if growth > 0 else 'challenging'} 
performance across key business metrics. The organization is well-positioned for continued growth 
and success in the upcoming quarters, with solid financial fundamentals and operational excellence 
driving sustainable competitive advantage.
"""
        doc.add_paragraph(conclusion.strip())
        
        doc.save(filepath)
        return filepath

    def generate_other_txt(self, filename: str) -> str:
        """Generate miscellaneous document TXT."""
        filepath = os.path.join(self.output_dir, 'txt', filename)
        
        doc_types = [
            "Technical Specification Document", "User Manual", "Meeting Minutes",
            "Project Status Update", "Training Material", "General Correspondence"
        ]
        
        doc_type = random.choice(doc_types)
        date = self.random_date(60)
        author_name, author_last, _ = random.choice(self.people)
        
        content = f"""
{doc_type.upper()}
{'='*len(doc_type.upper())}

Document Information:
- Title: {doc_type}
- Date: {date.strftime('%B %d, %Y')}
- Author: {author_name} {author_last}
- Version: {random.randint(1, 5)}.{random.randint(0, 9)}
- Reference: DOC-{random.randint(1000, 9999)}

{'='*60}
CONTENT OVERVIEW
{'='*60}

This document serves as {random.choice([
    'comprehensive reference material for various operational procedures',
    'detailed guidance for system implementation and configuration',
    'general information resource for project stakeholders',
    'supplementary documentation supporting business processes'
])}.

Key Topics Covered:
• {random.choice(['System requirements and specifications', 'Operational procedures and guidelines'])}
• {random.choice(['Implementation strategies and best practices', 'Process workflows and methodologies'])}
• {random.choice(['Quality assurance and testing protocols', 'Maintenance and support procedures'])}
• {random.choice(['Compliance requirements and standards', 'Performance metrics and evaluation criteria'])}

Technical Details:
{random.choice([
    'This section contains detailed technical specifications and configuration parameters required for proper system implementation.',
    'The following information provides comprehensive guidance for users and administrators regarding system operation.',
    'This documentation includes step-by-step procedures and troubleshooting guidelines for common scenarios.',
    'Reference material contained herein supports ongoing operations and maintenance activities.'
])}

Procedures and Guidelines:
1. Initial setup and configuration requirements
2. Standard operating procedures and workflows  
3. Quality control and validation processes
4. Documentation and reporting requirements
5. Escalation procedures and support contacts

Additional Information:
{random.choice([
    'Please refer to the appendices for detailed technical specifications and supplementary resources.',
    'For additional support or clarification, contact the appropriate department or project lead.',
    'This document should be reviewed and updated regularly to ensure accuracy and relevance.',
    'All users must familiarize themselves with the contents before proceeding with implementation.'
])}

Notes and Disclaimers:
- This document is provided for informational purposes only
- Procedures may vary based on specific system configurations
- Always follow current organizational policies and guidelines
- Contact technical support for assistance with complex scenarios

Document prepared by: {author_name} {author_last}
Department: {random.choice(['IT', 'Operations', 'Quality Assurance', 'Project Management'])}
Last Updated: {date.strftime('%B %d, %Y')}

{'='*60}
END OF DOCUMENT
{'='*60}
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filepath

    def generate_invoice_txt(self, filename: str) -> str:
        """Generate an invoice in TXT format."""
        filepath = os.path.join(self.output_dir, 'txt', filename)
        company = random.choice(self.companies)
        customer_name, customer_last, _ = random.choice(self.people)
        address = random.choice(self.addresses)
        invoice_date = self.random_date(90)
        due_date = invoice_date + timedelta(days=30)
        
        # Generate line items
        line_items = []
        subtotal = 0
        for i in range(random.randint(2, 5)):
            service = random.choice([
                'Software Development', 'Consulting Services', 'Project Management',
                'Technical Support', 'System Analysis', 'Training Services'
            ])
            hours = random.randint(10, 80)
            rate = random.choice([75, 85, 95, 105, 115, 125])
            amount = hours * rate
            subtotal += amount
            line_items.append(f"{service:<25} {hours:>6} hrs  ${rate:>6}/hr  ${amount:>8,.2f}")
        
        tax_rate = 0.0875
        tax_amount = subtotal * tax_rate
        total = subtotal + tax_amount
        
        content = f"""
================================================================================
                              INVOICE
================================================================================

{company}
{address}

Invoice To:                          Invoice Details:
{customer_name} {customer_last}      Invoice #: INV-{random.randint(10000, 99999)}
Business Client                      Date: {invoice_date.strftime('%B %d, %Y')}
                                    Due Date: {due_date.strftime('%B %d, %Y')}
                                    Terms: Net 30 Days

================================================================================
                            SERVICES PROVIDED
================================================================================

Description                    Hours    Rate      Amount
--------------------------------------------------------------------------------
{chr(10).join(line_items)}
                                              ________________
                                    Subtotal:  ${subtotal:>8,.2f}
                                        Tax:   ${tax_amount:>8,.2f}
                                              ================
                                       Total:  ${total:>8,.2f}

================================================================================
                              PAYMENT TERMS
================================================================================

Payment is due within 30 days of invoice date.
Please remit payment to the address above.
Thank you for your business!

Account Details:
- Account Number: {random.randint(100000, 999999)}
- Reference: INV-{random.randint(10000, 99999)}
- Customer ID: CUST-{random.randint(1000, 9999)}

Questions? Contact us at: billing@{company.lower().replace(' ', '').replace(',', '').replace('.', '')}.com

================================================================================
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filepath

    def generate_memo_txt(self, filename: str) -> str:
        """Generate a memo in TXT format."""
        filepath = os.path.join(self.output_dir, 'txt', filename)
        company = random.choice(self.companies)
        from_name, from_last, from_title = random.choice(self.people)
        to_name, to_last, to_title = random.choice(self.people)
        date = self.random_date(30)
        
        subjects = [
            'Policy Update - Remote Work Guidelines',
            'Quarterly Team Meeting Schedule',
            'New Safety Procedures Implementation',
            'Budget Allocation for Q4 Projects',
            'Performance Review Process Updates',
            'Holiday Schedule Announcement',
            'Training Program Requirements',
            'Office Relocation Timeline'
        ]
        
        subject = random.choice(subjects)
        
        content = f"""
================================================================================
                           INTERNAL MEMORANDUM
================================================================================

{company}

TO:      {to_name} {to_last}, {to_title}
FROM:    {from_name} {from_last}, {from_title}
DATE:    {date.strftime('%B %d, %Y')}
SUBJECT: {subject}

================================================================================

Dear Team,

{random.choice([
    'I am writing to inform you of important updates that will take effect immediately.',
    'Please be advised of the following policy changes and implementation timeline.',
    'This memo outlines new procedures that all staff members must follow.',
    'The following information requires your immediate attention and action.'
])}

Key Points:
• {random.choice(['All employees must complete the new training by month end', 'Department heads should schedule team meetings within two weeks'])}
• {random.choice(['Policy updates will be posted on the company intranet', 'Updated procedures are available in the employee handbook'])}
• {random.choice(['Questions should be directed to HR for clarification', 'Implementation begins on the first of next month'])}

Action Items:
1. Review the attached documentation carefully
2. {random.choice(['Schedule required training sessions for your team', 'Update departmental procedures accordingly'])}
3. {random.choice(['Submit compliance confirmation by the deadline', 'Coordinate with other departments as needed'])}
4. Follow up with any questions or concerns

Implementation Timeline:
- Phase 1: {random.choice(['Training completion', 'Policy review'])} - {(date + timedelta(days=14)).strftime('%B %d')}
- Phase 2: {random.choice(['Full implementation', 'Compliance verification'])} - {(date + timedelta(days=30)).strftime('%B %d')}

{random.choice([
    'Your cooperation and prompt attention to this matter is greatly appreciated.',
    'Please ensure all team members are informed of these important updates.',
    'Contact me directly if you need clarification on any of these points.',
    'Thank you for your continued dedication to our organizational excellence.'
])}

Best regards,

{from_name} {from_last}
{from_title}
{company}

================================================================================
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filepath

    def generate_legal_txt(self, filename: str) -> str:
        """Generate a legal document in TXT format."""
        filepath = os.path.join(self.output_dir, 'txt', filename)
        plaintiff_name, plaintiff_last, _ = random.choice(self.people)
        defendant_name, defendant_last, _ = random.choice(self.people)
        case_number = f"{random.randint(2020, 2024)}-CV-{random.randint(1000, 9999)}"
        date = self.random_date(60)
        
        content = f"""
================================================================================
                         SUPERIOR COURT OF JUSTICE
================================================================================

Case No: {case_number}

{plaintiff_name} {plaintiff_last}
                                                    Plaintiff
v.

{defendant_name} {defendant_last}
                                                    Defendant

================================================================================
                              LEGAL NOTICE
================================================================================

TO: {defendant_name} {defendant_last}

YOU ARE HEREBY NOTIFIED that a legal action has been commenced against you in the 
Superior Court of Justice. The nature of the claim against you is set forth in 
the Statement of Claim served with this Notice.

NATURE OF CLAIM:
{random.choice([
    'Breach of employment contract and violation of confidentiality agreement',
    'Business dispute regarding contractual obligations and damages',
    'Professional negligence and breach of fiduciary duty',
    'Violation of non-compete agreement and trade secret misappropriation'
])}

RELIEF SOUGHT:
The Plaintiff seeks monetary damages in the amount of ${random.randint(50000, 500000):,}, 
plus costs, interest, and such other relief as this Court deems just and proper.

YOU HAVE THIRTY (30) DAYS after service of this Notice to file an Answer with 
the Court. Failure to respond within the prescribed time may result in a 
default judgment being entered against you.

COURT INFORMATION:
Superior Court of Justice
Civil Division
{random.choice(self.addresses)}

ATTORNEY FOR PLAINTIFF:
{random.choice(['Law Offices of Smith & Associates', 'Johnson Legal Group', 'Williams & Partners LLP'])}
Attorney Bar No: {random.randint(100000, 999999)}
{random.choice(self.addresses)}

DATE OF SERVICE: {date.strftime('%B %d, %Y')}

IMPORTANT: If you fail to file an Answer within thirty (30) days after service 
of this Notice, judgment by default may be taken against you for the relief 
demanded in the Statement of Claim.

YOU ARE ADVISED TO SEEK LEGAL COUNSEL immediately if you have not already done so.

================================================================================

CERTIFICATE OF SERVICE

I hereby certify that a true and correct copy of the foregoing Notice was served 
upon the defendant by the following method:

[ ] Personal service
[ ] Certified mail, return receipt requested
[ ] Publication in newspaper of general circulation

Date: {date.strftime('%B %d, %Y')}

                                    _________________________
                                    Clerk of Court

================================================================================
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filepath

    def generate_report_pdf(self, filename: str) -> str:
        """Generate a report in PDF format."""
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib import colors
        
        filepath = os.path.join(self.output_dir, 'pdf', filename)
        doc = SimpleDocTemplate(filepath, pagesize=letter, topMargin=0.5*inch)
        
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=18,
            textColor=colors.darkblue,
            spaceAfter=20
        )
        
        company = random.choice(self.companies)
        quarter = random.choice(['Q1', 'Q2', 'Q3', 'Q4'])
        year = random.choice([2023, 2024])
        date = self.random_date(60)
        
        elements = []
        
        # Title
        title = Paragraph(f"{quarter} {year} Business Performance Report", title_style)
        elements.append(title)
        elements.append(Spacer(1, 0.2*inch))
        
        # Company info
        company_info = Paragraph(f"<b>{company}</b><br/>Quarterly Business Analysis", styles['Normal'])
        elements.append(company_info)
        elements.append(Spacer(1, 0.3*inch))
        
        # Executive Summary
        exec_summary = Paragraph("<b>EXECUTIVE SUMMARY</b>", styles['Heading2'])
        elements.append(exec_summary)
        
        summary_text = f"""
        This report provides a comprehensive analysis of business performance for {quarter} {year}. 
        Key metrics show {random.choice(['strong growth', 'steady improvement', 'positive trends'])} across 
        multiple operational areas. Revenue increased by {random.randint(5, 25)}% compared to the previous quarter, 
        with {random.choice(['customer satisfaction', 'operational efficiency', 'market penetration'])} reaching 
        new highs.
        """
        elements.append(Paragraph(summary_text, styles['Normal']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Financial Performance Table
        financial_header = Paragraph("<b>FINANCIAL PERFORMANCE</b>", styles['Heading2'])
        elements.append(financial_header)
        
        financial_data = [
            ['Metric', 'Current Quarter', 'Previous Quarter', 'Change'],
            ['Revenue', f'${random.randint(500, 2000)}K', f'${random.randint(400, 1800)}K', f'+{random.randint(5, 25)}%'],
            ['Profit Margin', f'{random.randint(15, 35)}%', f'{random.randint(10, 30)}%', f'+{random.randint(2, 8)}%'],
            ['Operating Costs', f'${random.randint(300, 1500)}K', f'${random.randint(350, 1600)}K', f'-{random.randint(5, 15)}%'],
            ['Customer Acquisition', f'{random.randint(150, 500)}', f'{random.randint(100, 400)}', f'+{random.randint(10, 40)}%']
        ]
        
        financial_table = Table(financial_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1*inch])
        financial_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.darkblue),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(financial_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Key Achievements
        achievements = Paragraph("<b>KEY ACHIEVEMENTS</b>", styles['Heading2'])
        elements.append(achievements)
        
        achievement_text = f"""
        • Exceeded revenue targets by {random.randint(8, 20)}%<br/>
        • Improved customer retention rate to {random.randint(85, 95)}%<br/>
        • Launched {random.randint(2, 5)} new {random.choice(['products', 'services', 'initiatives'])}<br/>
        • Reduced operational costs by {random.randint(10, 25)}%<br/>
        • Achieved {random.randint(90, 98)}% customer satisfaction rating
        """
        elements.append(Paragraph(achievement_text, styles['Normal']))
        
        doc.build(elements)
        return filepath

    def generate_contract_pdf(self, filename: str) -> str:
        """Generate a contract in PDF format."""
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib import colors
        
        filepath = os.path.join(self.output_dir, 'pdf', filename)
        doc = SimpleDocTemplate(filepath, pagesize=letter, topMargin=0.5*inch)
        
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=16,
            textColor=colors.darkblue,
            spaceAfter=20
        )
        
        company1 = random.choice(self.companies)
        company2 = random.choice([c for c in self.companies if c != company1])
        party1_name, party1_last, party1_title = random.choice(self.people)
        party2_name, party2_last, party2_title = random.choice(self.people)
        date = self.random_date(30)
        
        elements = []
        
        # Title
        title = Paragraph("PROFESSIONAL SERVICES AGREEMENT", title_style)
        elements.append(title)
        elements.append(Spacer(1, 0.3*inch))
        
        # Agreement text
        agreement_text = f"""
        This Professional Services Agreement ("Agreement") is entered into on {date.strftime('%B %d, %Y')} 
        between {company1} ("Provider") and {company2} ("Client").
        
        <b>WHEREAS</b>, Provider possesses expertise in professional consulting services; and
        
        <b>WHEREAS</b>, Client desires to engage Provider for such services;
        
        <b>NOW THEREFORE</b>, the parties agree as follows:
        
        <b>1. SERVICES</b><br/>
        Provider shall provide {random.choice(['software development', 'consulting', 'project management', 'technical support'])} 
        services as detailed in Exhibit A, which is incorporated herein by reference.
        
        <b>2. COMPENSATION</b><br/>
        Client shall pay Provider ${random.randint(50, 200):,} per month for the duration of this Agreement. 
        Payment is due within 30 days of invoice receipt.
        
        <b>3. TERM</b><br/>
        This Agreement shall commence on {date.strftime('%B %d, %Y')} and continue for a period of 
        {random.choice(['twelve (12)', 'twenty-four (24)', 'thirty-six (36)'])} months, unless terminated earlier.
        
        <b>4. CONFIDENTIALITY</b><br/>
        Both parties acknowledge that confidential information may be shared and agree to maintain 
        strict confidentiality of all proprietary information.
        
        <b>5. TERMINATION</b><br/>
        Either party may terminate this Agreement with {random.choice(['30', '60', '90'])} days written notice.
        
        <b>6. GOVERNING LAW</b><br/>
        This Agreement shall be governed by the laws of the State of {random.choice(['California', 'New York', 'Texas'])}.
        
        <b>IN WITNESS WHEREOF</b>, the parties have executed this Agreement as of the date first written above.
        """
        
        elements.append(Paragraph(agreement_text, styles['Normal']))
        elements.append(Spacer(1, 0.5*inch))
        
        # Signature blocks
        signature_text = f"""
        <b>PROVIDER:</b><br/>
        {company1}<br/><br/>
        By: _________________________<br/>
        {party1_name} {party1_last}, {party1_title}<br/>
        Date: ____________________<br/><br/>
        
        <b>CLIENT:</b><br/>
        {company2}<br/><br/>
        By: _________________________<br/>
        {party2_name} {party2_last}, {party2_title}<br/>
        Date: ____________________
        """
        
        elements.append(Paragraph(signature_text, styles['Normal']))
        
        doc.build(elements)
        return filepath

    def generate_contract_docx(self, filename: str) -> str:
        """Generate a contract in DOCX format."""
        from docx import Document
        from docx.shared import Inches
        
        filepath = os.path.join(self.output_dir, 'docx', filename)
        doc = Document()
        
        company1 = random.choice(self.companies)
        company2 = random.choice([c for c in self.companies if c != company1])
        party1_name, party1_last, party1_title = random.choice(self.people)
        party2_name, party2_last, party2_title = random.choice(self.people)
        date = self.random_date(30)
        
        # Title
        title = doc.add_heading('EMPLOYMENT CONTRACT', 0)
        title.alignment = 1  # Center alignment
        
        # Header
        doc.add_paragraph()
        header = doc.add_paragraph()
        header.add_run('Contract Number: ').bold = True
        header.add_run(f'EMP-{random.randint(10000, 99999)}')
        header.add_run('\nEffective Date: ').bold = True
        header.add_run(date.strftime('%B %d, %Y'))
        
        doc.add_paragraph()
        
        # Parties
        parties_para = doc.add_paragraph()
        parties_para.add_run('AGREEMENT BETWEEN:\n').bold = True
        parties_para.add_run(f'Employer: {company1}\n')
        parties_para.add_run(f'Employee: {party1_name} {party1_last}\n')
        
        doc.add_paragraph()
        
        # Terms
        terms = doc.add_heading('TERMS AND CONDITIONS', level=1)
        
        # Section 1
        section1 = doc.add_paragraph()
        section1.add_run('1. POSITION AND DUTIES\n').bold = True
        section1.add_run(f'Employee shall serve as {party1_title} and shall perform duties as assigned by the Employer. Employee agrees to devote full professional time and attention to the business of the Employer.')
        
        doc.add_paragraph()
        
        # Section 2
        section2 = doc.add_paragraph()
        section2.add_run('2. COMPENSATION\n').bold = True
        salary = random.randint(60000, 150000)
        section2.add_run(f'Employee shall receive an annual salary of ${salary:,}, payable in accordance with Employer\'s standard payroll practices. Employee shall be eligible for annual performance bonuses at Employer\'s discretion.')
        
        doc.add_paragraph()
        
        # Section 3
        section3 = doc.add_paragraph()
        section3.add_run('3. BENEFITS\n').bold = True
        section3.add_run('Employee shall be entitled to participate in all employee benefit plans and programs made available to employees of similar rank and tenure, subject to the terms and conditions of such plans.')
        
        doc.add_paragraph()
        
        # Section 4
        section4 = doc.add_paragraph()
        section4.add_run('4. CONFIDENTIALITY\n').bold = True
        section4.add_run('Employee acknowledges that during employment, Employee will have access to confidential information. Employee agrees to maintain strict confidentiality of all proprietary information.')
        
        doc.add_paragraph()
        
        # Section 5
        section5 = doc.add_paragraph()
        section5.add_run('5. TERMINATION\n').bold = True
        section5.add_run(f'This agreement may be terminated by either party with {random.choice(["30", "60", "90"])} days written notice. Upon termination, Employee agrees to return all company property.')
        
        doc.add_paragraph()
        
        # Signatures
        doc.add_paragraph()
        sig_para = doc.add_paragraph()
        sig_para.add_run('SIGNATURES:\n').bold = True
        sig_para.add_run(f'\nEmployer: {company1}\n\n')
        sig_para.add_run('Signature: _________________________  Date: ___________\n\n')
        sig_para.add_run(f'Employee: {party1_name} {party1_last}\n\n')
        sig_para.add_run('Signature: _________________________  Date: ___________')
        
        doc.save(filepath)
        return filepath

    def generate_other_pdf(self, filename: str) -> str:
        """Generate an 'other' document in PDF format."""
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib import colors
        
        filepath = os.path.join(self.output_dir, 'pdf', filename)
        doc = SimpleDocTemplate(filepath, pagesize=letter, topMargin=0.5*inch)
        
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=16,
            textColor=colors.darkblue,
            spaceAfter=20
        )
        
        doc_types = ['Technical Specification', 'User Manual', 'Project Proposal', 'Meeting Minutes']
        doc_type = random.choice(doc_types)
        company = random.choice(self.companies)
        author_name, author_last, author_title = random.choice(self.people)
        date = self.random_date(60)
        
        elements = []
        
        # Title
        title = Paragraph(f"{doc_type.upper()}", title_style)
        elements.append(title)
        elements.append(Spacer(1, 0.2*inch))
        
        # Header info
        header_text = f"""
        <b>Document Information:</b><br/>
        Company: {company}<br/>
        Prepared by: {author_name} {author_last}, {author_title}<br/>
        Date: {date.strftime('%B %d, %Y')}<br/>
        Version: {random.randint(1, 5)}.{random.randint(0, 9)}<br/>
        Reference: DOC-{random.randint(1000, 9999)}
        """
        elements.append(Paragraph(header_text, styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Content
        if doc_type == 'Technical Specification':
            content_text = f"""
            <b>OVERVIEW</b><br/>
            This document outlines the technical specifications for system implementation. 
            The solution addresses {random.choice(['scalability requirements', 'performance optimization', 'security compliance', 'integration needs'])} 
            while maintaining compatibility with existing infrastructure.
            
            <b>REQUIREMENTS</b><br/>
            • Minimum system requirements: {random.choice(['8GB RAM', '16GB RAM', '32GB RAM'])}, 
            {random.choice(['2.5GHz processor', '3.0GHz processor', '3.5GHz processor'])}<br/>
            • Software dependencies: {random.choice(['Java 11+', 'Python 3.8+', '.NET 6.0+'])}<br/>
            • Database: {random.choice(['PostgreSQL 13+', 'MySQL 8.0+', 'SQL Server 2019+'])}<br/>
            • Network: {random.choice(['1Gbps', '10Gbps', '100Mbps'])} minimum bandwidth
            
            <b>IMPLEMENTATION NOTES</b><br/>
            Installation should be performed during maintenance windows. 
            All configurations must be validated before production deployment.
            """
        else:
            content_text = f"""
            <b>SUMMARY</b><br/>
            This document provides {random.choice(['comprehensive guidance', 'detailed procedures', 'reference information'])} 
            for {random.choice(['project stakeholders', 'system users', 'technical teams', 'business analysts'])}.
            
            <b>KEY TOPICS</b><br/>
            • {random.choice(['System configuration and setup procedures', 'User interface and navigation guidelines'])}<br/>
            • {random.choice(['Troubleshooting and maintenance protocols', 'Best practices and recommendations'])}<br/>
            • {random.choice(['Security considerations and compliance requirements', 'Performance optimization techniques'])}
            
            <b>ADDITIONAL INFORMATION</b><br/>
            For technical support or additional questions, please contact the 
            {random.choice(['IT Help Desk', 'Project Team', 'System Administrator', 'Technical Lead'])} 
            at extension {random.randint(1000, 9999)}.
            """
        
        elements.append(Paragraph(content_text, styles['Normal']))
        
        doc.build(elements)
        return filepath

    def generate_other_docx(self, filename: str) -> str:
        """Generate an 'other' document in DOCX format."""
        from docx import Document
        
        filepath = os.path.join(self.output_dir, 'docx', filename)
        doc = Document()
        
        doc_types = ['Meeting Minutes', 'Project Proposal', 'Technical Manual', 'Policy Document']
        doc_type = random.choice(doc_types)
        company = random.choice(self.companies)
        author_name, author_last, author_title = random.choice(self.people)
        date = self.random_date(60)
        
        # Title
        title = doc.add_heading(f'{doc_type.upper()}', 0)
        title.alignment = 1
        
        # Header
        doc.add_paragraph()
        header = doc.add_paragraph()
        header.add_run('Company: ').bold = True
        header.add_run(f'{company}\n')
        header.add_run('Prepared by: ').bold = True
        header.add_run(f'{author_name} {author_last}, {author_title}\n')
        header.add_run('Date: ').bold = True
        header.add_run(date.strftime('%B %d, %Y'))
        
        doc.add_paragraph()
        
        # Content based on document type
        if doc_type == 'Meeting Minutes':
            # Meeting details
            meeting_para = doc.add_paragraph()
            meeting_para.add_run('MEETING DETAILS\n').bold = True
            meeting_para.add_run(f'Date: {date.strftime("%B %d, %Y")}\n')
            meeting_para.add_run(f'Time: {random.choice(["9:00 AM", "10:00 AM", "2:00 PM", "3:00 PM"])}\n')
            meeting_para.add_run(f'Location: {random.choice(["Conference Room A", "Virtual Meeting", "Executive Boardroom"])}\n')
            
            # Attendees
            attendees_para = doc.add_paragraph()
            attendees_para.add_run('ATTENDEES\n').bold = True
            for i in range(random.randint(3, 6)):
                name, last, title = random.choice(self.people)
                attendees_para.add_run(f'• {name} {last}, {title}\n')
            
            # Discussion points
            discussion_para = doc.add_paragraph()
            discussion_para.add_run('DISCUSSION POINTS\n').bold = True
            discussion_para.add_run('• Quarterly budget review and allocation planning\n')
            discussion_para.add_run('• Project timeline updates and milestone tracking\n')
            discussion_para.add_run('• Resource allocation and staffing requirements\n')
            discussion_para.add_run('• Process improvement initiatives and implementation\n')
            
            # Action items
            action_para = doc.add_paragraph()
            action_para.add_run('ACTION ITEMS\n').bold = True
            action_para.add_run(f'• Complete budget analysis by {(date + timedelta(days=7)).strftime("%B %d")}\n')
            action_para.add_run(f'• Schedule follow-up meetings with department heads\n')
            action_para.add_run(f'• Review and update project documentation\n')
        
        else:
            # General content
            overview_para = doc.add_paragraph()
            overview_para.add_run('OVERVIEW\n').bold = True
            overview_para.add_run(f'This {doc_type.lower()} provides {random.choice(["comprehensive information", "detailed guidance", "reference material"])} for {random.choice(["project stakeholders", "team members", "system users"])}. ')
            overview_para.add_run(f'The content addresses {random.choice(["operational requirements", "implementation procedures", "best practices", "compliance standards"])} and related considerations.')
            
            doc.add_paragraph()
            
            # Key sections
            sections_para = doc.add_paragraph()
            sections_para.add_run('KEY SECTIONS\n').bold = True
            sections_para.add_run('• System requirements and configuration guidelines\n')
            sections_para.add_run('• Implementation procedures and best practices\n')
            sections_para.add_run('• Quality assurance and testing protocols\n')
            sections_para.add_run('• Maintenance and support procedures\n')
            
            doc.add_paragraph()
            
            # Notes
            notes_para = doc.add_paragraph()
            notes_para.add_run('IMPORTANT NOTES\n').bold = True
            notes_para.add_run('Please review all sections carefully before proceeding with implementation. ')
            notes_para.add_run('Contact the project team for questions or clarification on specific procedures. ')
            notes_para.add_run('This document should be updated regularly to reflect current practices and requirements.')
        
        doc.save(filepath)
        return filepath

    def generate_all_diverse_documents(self, total_docs: int = 60) -> Dict[str, int]:
        """Generate diverse documents across all formats and categories."""
        print("🚀 Generating diverse sample documents in multiple formats...")
        
        self.create_output_dir()
        
        # Define distribution
        docs_per_category = total_docs // 6
        remainder = total_docs % 6
        
        distribution = {
            'invoice': docs_per_category + (1 if remainder > 0 else 0),
            'memo': docs_per_category + (1 if remainder > 1 else 0),
            'contract': docs_per_category + (1 if remainder > 2 else 0),
            'legal': docs_per_category + (1 if remainder > 3 else 0),
            'report': docs_per_category + (1 if remainder > 4 else 0),
            'other': docs_per_category + (1 if remainder > 5 else 0)
        }
        
        generated_files = []
        format_count = {'pdf': 0, 'docx': 0, 'txt': 0}
        
        # Generate invoices (mostly PDF)
        for i in range(distribution['invoice']):
            fmt = random.choices(['pdf', 'txt'], weights=[0.8, 0.2])[0]
            filename = f"invoice_{i+1:03d}.{fmt}"
            if fmt == 'pdf':
                self.generate_invoice_pdf(filename)
            else:
                self.generate_invoice_txt(filename.replace('.txt', '_invoice.txt'))
            format_count[fmt] += 1
            generated_files.append(filename)
        
        # Generate memos (mostly DOCX)
        for i in range(distribution['memo']):
            fmt = random.choices(['docx', 'txt'], weights=[0.7, 0.3])[0]
            filename = f"memo_{i+1:03d}.{fmt}"
            if fmt == 'docx':
                self.generate_memo_docx(filename)
            else:
                self.generate_memo_txt(filename.replace('.txt', '_memo.txt'))
            format_count[fmt] += 1
            generated_files.append(filename)
        
        # Generate contracts (mostly TXT)
        for i in range(distribution['contract']):
            fmt = random.choices(['txt', 'pdf', 'docx'], weights=[0.6, 0.2, 0.2])[0]
            filename = f"contract_{i+1:03d}.{fmt}"
            if fmt == 'txt':
                self.generate_contract_txt(filename)
            elif fmt == 'pdf':
                self.generate_contract_pdf(filename.replace('.pdf', '_contract.pdf'))
            else:
                self.generate_contract_docx(filename.replace('.docx', '_contract.docx'))
            format_count[fmt] += 1
            generated_files.append(filename)
        
        # Generate legal docs (mostly PDF)
        for i in range(distribution['legal']):
            fmt = random.choices(['pdf', 'txt'], weights=[0.8, 0.2])[0]
            filename = f"legal_{i+1:03d}.{fmt}"
            if fmt == 'pdf':
                self.generate_legal_pdf(filename)
            else:
                self.generate_legal_txt(filename.replace('.txt', '_legal.txt'))
            format_count[fmt] += 1
            generated_files.append(filename)
        
        # Generate reports (mostly DOCX)
        for i in range(distribution['report']):
            fmt = random.choices(['docx', 'pdf'], weights=[0.7, 0.3])[0]
            filename = f"report_{i+1:03d}.{fmt}"
            if fmt == 'docx':
                self.generate_report_docx(filename)
            else:
                self.generate_report_pdf(filename.replace('.pdf', '_report.pdf'))
            format_count[fmt] += 1
            generated_files.append(filename)
        
        # Generate other docs (mixed formats)
        for i in range(distribution['other']):
            fmt = random.choice(['txt', 'pdf', 'docx'])
            filename = f"other_{i+1:03d}.{fmt}"
            if fmt == 'txt':
                self.generate_other_txt(filename)
            elif fmt == 'pdf':
                self.generate_other_pdf(filename.replace('.pdf', '_other.pdf'))
            else:
                self.generate_other_docx(filename.replace('.docx', '_other.docx'))
            format_count[fmt] += 1
            generated_files.append(filename)
        
        print(f"✅ Generated {len(generated_files)} diverse documents:")
        print(f"   📄 PDFs: {format_count['pdf']}")
        print(f"   📝 DOCX: {format_count['docx']}")
        print(f"   📋 TXT: {format_count['txt']}")
        print(f"   📁 Total: {sum(format_count.values())} documents")
        print(f"\n📂 Documents organized by format in '{self.output_dir}/' folder")
        
        return format_count

def main():
    """Main function to generate diverse sample documents."""
    print("🌟 Welcome to Diverse Document Generator!")
    print("This will create realistic PDF, TXT, and DOCX files for testing.\n")
    
    try:
        num_docs = int(input("Enter number of documents to generate (default: 60): ") or "60")
    except ValueError:
        num_docs = 60
    
    generator = DiverseDocumentGenerator()
    format_counts = generator.generate_all_diverse_documents(num_docs)
    
    print(f"\n🎉 Document generation complete!")
    print(f"📂 All documents saved to 'diverse_sample_documents/' folder")
    print(f"\n💡 To test with these documents:")
    print(f"   python main.py diverse_sample_documents")
    print(f"   python main.py --dashboard")
    print(f"   python launch_dashboard.py")

if __name__ == "__main__":
    main() 