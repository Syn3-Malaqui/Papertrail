#!/usr/bin/env python3
"""
Sample Document Generator for Papertrail
Generates realistic sample documents for testing the classification system.
"""

import os
import random
from datetime import datetime, timedelta
from typing import List, Dict

class DocumentGenerator:
    """Generates realistic sample documents for testing."""
    
    def __init__(self, output_dir: str = "generated_documents"):
        self.output_dir = output_dir
        self.setup_data()
        
    def setup_data(self):
        """Setup data for generating realistic documents."""
        self.company_names = [
            "ABC Corporation", "TechSolutions Inc", "Global Enterprises LLC", 
            "Innovative Systems", "DataTech Solutions", "ProServices Corp",
            "NextGen Industries", "Dynamic Solutions", "Elite Consulting",
            "Premier Technologies", "Advanced Analytics", "Smart Systems Inc",
            "Digital Innovations", "Strategic Partners", "Excellence Corp",
            "Future Vision LLC", "Alpha Technologies", "Beta Solutions",
            "Gamma Enterprises", "Delta Systems", "Omega Corporation"
        ]
        
        self.person_names = [
            "John Smith", "Sarah Johnson", "Michael Brown", "Emily Davis",
            "David Wilson", "Jessica Miller", "Robert Taylor", "Ashley Anderson",
            "James Thomas", "Amanda Jackson", "Christopher White", "Jennifer Harris",
            "Matthew Martin", "Elizabeth Thompson", "Daniel Garcia", "Michelle Martinez",
            "Anthony Robinson", "Stephanie Clark", "Mark Rodriguez", "Lauren Lewis"
        ]
        
        self.departments = [
            "Human Resources", "Finance", "Marketing", "Operations", 
            "IT", "Sales", "Legal", "Administration", "Customer Service",
            "Project Management", "Quality Assurance", "Research & Development"
        ]
        
        self.services = [
            "Professional Consulting", "Software Development", "Technical Support",
            "Marketing Services", "Financial Analysis", "Legal Consultation",
            "Project Management", "Training Services", "Data Analysis",
            "System Integration", "Security Assessment", "Business Strategy"
        ]
        
        self.cities = [
            "New York, NY", "Los Angeles, CA", "Chicago, IL", "Houston, TX",
            "Phoenix, AZ", "Philadelphia, PA", "San Antonio, TX", "San Diego, CA",
            "Dallas, TX", "San Jose, CA", "Austin, TX", "Jacksonville, FL"
        ]

    def create_output_dir(self):
        """Create output directory if it doesn't exist."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"📁 Created directory: {self.output_dir}")

    def random_date(self, start_days_ago: int = 365, end_days_ago: int = 0) -> str:
        """Generate a random date within the specified range."""
        start_date = datetime.now() - timedelta(days=start_days_ago)
        end_date = datetime.now() - timedelta(days=end_days_ago)
        random_date = start_date + timedelta(
            seconds=random.randint(0, int((end_date - start_date).total_seconds()))
        )
        return random_date.strftime("%B %d, %Y")

    def random_invoice_number(self) -> str:
        """Generate a random invoice number."""
        return f"INV-{random.randint(2023, 2024)}-{random.randint(1000, 9999)}"

    def random_amount(self, min_amount: int = 500, max_amount: int = 50000) -> str:
        """Generate a random dollar amount."""
        amount = random.randint(min_amount, max_amount)
        return f"${amount:,.2f}"

    def generate_invoices(self, count: int = 15) -> List[Dict]:
        """Generate invoice documents."""
        invoices = []
        
        for i in range(count):
            invoice_num = self.random_invoice_number()
            date = self.random_date(90, 0)
            company = random.choice(self.company_names)
            service = random.choice(self.services)
            
            subtotal = random.randint(5000, 45000)
            tax_rate = random.choice([0.0825, 0.0875, 0.095, 0.0775])
            tax = subtotal * tax_rate
            total = subtotal + tax
            
            content = f"""INVOICE #{invoice_num}

Date: {date}
Bill To: {company}
{random.randint(100, 9999)} {random.choice(['Main St', 'Business Ave', 'Corporate Blvd', 'Commerce Dr'])}
{random.choice(self.cities)}

Description                              Qty    Rate        Amount
{service:<40} {random.randint(10, 100):<6} ${random.randint(50, 500)}.00   ${subtotal:,.2f}
                                                           --------
                                         Subtotal:         ${subtotal:,.2f}
                                         Tax ({tax_rate*100:.2f}%):         ${tax:,.2f}
                                         TOTAL DUE:        ${total:,.2f}

Payment Terms: Net {random.choice([15, 30, 45])} days
Please remit payment within {random.choice([15, 30, 45])} days of invoice date.
Account Number: {random.randint(100000, 999999)}"""

            invoices.append({
                'filename': f'invoice_{i+1:03d}.txt',
                'content': content
            })
        
        return invoices

    def generate_memos(self, count: int = 15) -> List[Dict]:
        """Generate memo documents."""
        memos = []
        
        memo_subjects = [
            "Quarterly Staff Meeting", "Policy Update", "Remote Work Guidelines",
            "Budget Allocation", "Training Session", "System Maintenance",
            "Holiday Schedule", "Performance Reviews", "Team Building Event",
            "Security Update", "Office Relocation", "New Hire Orientation",
            "Equipment Upgrade", "Meeting Schedule Change", "Expense Policy"
        ]
        
        for i in range(count):
            subject = random.choice(memo_subjects)
            sender = random.choice(self.person_names)
            dept = random.choice(self.departments)
            date = self.random_date(30, 0)
            
            content = f"""MEMORANDUM

TO: All {dept} Staff
FROM: {sender}, {dept} Manager
DATE: {date}
RE: {subject}

This memo serves to inform all staff members about important updates regarding {subject.lower()}.

Key Points:
1. Effective date: {self.random_date(7, 0)}
2. Implementation timeline: {random.choice(['immediate', '2 weeks', '30 days'])}
3. Required actions: {random.choice(['Review and acknowledge', 'Complete training', 'Submit forms'])}
4. Deadline for compliance: {self.random_date(0, -30)}

Additional Information:
{random.choice([
    'All employees must complete the required training by the specified deadline.',
    'Please review the attached documentation and follow new procedures.',
    'Contact your supervisor if you have any questions or concerns.',
    'Mandatory attendance is required for all scheduled sessions.'
])}

For questions or clarification, please contact {dept} at extension {random.randint(1000, 9999)}.

Best regards,
{sender}
{dept} Manager"""

            memos.append({
                'filename': f'memo_{i+1:03d}.txt',
                'content': content
            })
        
        return memos

    def generate_contracts(self, count: int = 12) -> List[Dict]:
        """Generate contract documents."""
        contracts = []
        
        contract_types = [
            "Service Agreement", "Employment Contract", "Consulting Agreement",
            "Software License Agreement", "Non-Disclosure Agreement", "Vendor Agreement"
        ]
        
        for i in range(count):
            contract_type = random.choice(contract_types)
            provider = random.choice(self.company_names)
            client = random.choice(self.company_names)
            while client == provider:
                client = random.choice(self.company_names)
            
            date = self.random_date(60, 0)
            term_months = random.choice([6, 12, 18, 24, 36])
            fee = self.random_amount(5000, 100000)
            
            content = f"""{contract_type.upper()}

This {contract_type} ("Agreement") is entered into on {date}, between {provider} ("Provider") and {client} ("Client").

1. SERVICES
Provider agrees to provide {random.choice(self.services).lower()} services as outlined in Exhibit A, attached hereto and incorporated by reference.

2. TERM
This Agreement shall commence on {self.random_date(30, -30)} and shall continue for a period of {term_months} months, unless terminated earlier in accordance with the provisions herein.

3. COMPENSATION
Client agrees to pay Provider a {random.choice(['monthly', 'quarterly', 'annual'])} fee of {fee} for the services rendered, payable within {random.choice([15, 30, 45])} days of receipt of invoice.

4. TERMINATION
Either party may terminate this Agreement with {random.choice([30, 60, 90])} days written notice.

5. CONFIDENTIALITY
Both parties agree to maintain confidentiality of all proprietary information shared during the term of this Agreement.

6. GOVERNING LAW
This Agreement shall be governed by the laws of the State of {random.choice(['California', 'New York', 'Texas', 'Florida'])}.

IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first written above.

Provider: _______________________    Client: _______________________
{provider:<32} {client}"""

            contracts.append({
                'filename': f'contract_{i+1:03d}.txt',
                'content': content
            })
        
        return contracts

    def generate_legal_documents(self, count: int = 12) -> List[Dict]:
        """Generate legal documents."""
        legal_docs = []
        
        case_types = [
            "Employment Dispute", "Contract Breach", "Intellectual Property",
            "Commercial Litigation", "Real Estate Dispute", "Partnership Dissolution"
        ]
        
        for i in range(count):
            case_type = random.choice(case_types)
            case_num = f"{random.randint(2023, 2024)}-{random.choice(['CV', 'EMP', 'IP', 'COM'])}-{random.randint(1000, 9999)}"
            plaintiff = random.choice(self.company_names)
            defendant = random.choice(self.company_names)
            while defendant == plaintiff:
                defendant = random.choice(self.company_names)
            
            damages = self.random_amount(10000, 500000)
            
            content = f"""LEGAL NOTICE

Case No.: {case_num}
Court: Superior Court of {random.choice(['Justice', 'Commerce', 'Business Affairs'])}

NOTICE OF LEGAL PROCEEDINGS

TO: {defendant}
FROM: {plaintiff}

TAKE NOTICE that a legal proceeding has been commenced against the defendant for {case_type.lower()} and associated damages.

NATURE OF CLAIM:
The plaintiff alleges {random.choice([
    'breach of contract and failure to perform agreed services',
    'violation of intellectual property rights and unauthorized use',
    'employment law violations and wrongful termination',
    'breach of fiduciary duty and misappropriation of funds'
])}.

RELIEF SOUGHT:
1. Monetary damages in the amount of {damages}
2. {random.choice(['Injunctive relief', 'Declaratory judgment', 'Specific performance'])}
3. Attorney fees and court costs
4. {random.choice(['Punitive damages', 'Interest and penalties', 'Restitution'])}

RESPONSE REQUIRED:
Any party wishing to defend this action must file a statement of defense within {random.choice([20, 30, 45])} days of service of this notice.

For more information, contact the court registry or legal counsel at {random.choice(['555-LAW-FIRM', '555-LEGAL-01', '555-ATTORNEY'])}.

DATED this {self.random_date(30, 0)}.

Attorney for Plaintiff
{random.choice(['Legal Associates LLP', 'Law Firm & Partners', 'Justice & Associates'])}"""

            legal_docs.append({
                'filename': f'legal_{i+1:03d}.txt',
                'content': content
            })
        
        return legal_docs

    def generate_reports(self, count: int = 13) -> List[Dict]:
        """Generate report documents."""
        reports = []
        
        report_types = [
            "Quarterly Performance Report", "Annual Financial Report", "Market Analysis Report",
            "Customer Satisfaction Report", "Operational Efficiency Report", "Security Assessment Report"
        ]
        
        for i in range(count):
            report_type = random.choice(report_types)
            quarter = random.choice(['Q1', 'Q2', 'Q3', 'Q4'])
            year = random.choice([2023, 2024])
            
            revenue = random.randint(1000000, 10000000)
            growth = random.randint(-5, 25)
            satisfaction = round(random.uniform(3.5, 5.0), 1)
            
            content = f"""{report_type.upper()}
{quarter} {year} Executive Summary

OVERVIEW:
This report presents the {report_type.lower()} for {quarter} {year}, highlighting key performance indicators and strategic insights.

KEY FINDINGS:
• Total Revenue: ${revenue:,}
• Growth Rate: {growth}% compared to previous period
• Customer Satisfaction Score: {satisfaction}/5.0
• Market Share: {random.randint(5, 25)}%
• Employee Satisfaction: {random.randint(70, 95)}%

FINANCIAL PERFORMANCE:
Revenue increased {'significantly' if growth > 10 else 'moderately' if growth > 0 else 'decreased'} due to {random.choice([
    'successful product launches and expanded market penetration',
    'improved operational efficiency and cost management',
    'strong customer retention and acquisition strategies',
    'market conditions and competitive positioning'
])}.

DEPARTMENTAL PERFORMANCE:
Sales: {'Exceeded' if random.random() > 0.3 else 'Met'} targets by {random.randint(5, 15)}%
Marketing: ROI improved to {random.uniform(2.5, 5.0):.1f}:1
Operations: Efficiency gains of {random.randint(3, 12)}%
Customer Service: Satisfaction score of {satisfaction}/5.0

RECOMMENDATIONS:
1. {random.choice(['Continue investment in high-performing product lines', 'Expand marketing efforts in underperforming regions'])}
2. {random.choice(['Implement cost optimization initiatives', 'Enhance customer experience programs'])}
3. {random.choice(['Invest in employee training and development', 'Strengthen competitive positioning'])}

CONCLUSION:
{quarter} {year} demonstrated {'strong' if growth > 5 else 'stable'} performance across key metrics, positioning the company well for continued growth."""

            reports.append({
                'filename': f'report_{i+1:03d}.txt',
                'content': content
            })
        
        return reports

    def generate_other_documents(self, count: int = 13) -> List[Dict]:
        """Generate miscellaneous documents."""
        other_docs = []
        
        doc_types = [
            "General Correspondence", "Meeting Notes", "Project Updates",
            "Product Specifications", "User Manual", "Technical Documentation"
        ]
        
        for i in range(count):
            doc_type = random.choice(doc_types)
            
            content = f"""{doc_type.upper()}

Document Date: {self.random_date(60, 0)}
Reference: {random.choice(['DOC', 'REF', 'MISC'])}-{random.randint(1000, 9999)}

SUBJECT: {random.choice([
    'General Information and Updates',
    'Miscellaneous Communications',
    'Reference Material and Documentation',
    'Supplementary Information Package'
])}

CONTENT:
This document contains {random.choice([
    'general information and reference material for various purposes',
    'miscellaneous communications and correspondence',
    'supplementary documentation and support materials',
    'reference data and informational content'
])}.

Key Topics Covered:
• {random.choice(['General procedures and guidelines', 'Reference information and data'])}
• {random.choice(['Communication protocols and standards', 'Documentation requirements'])}
• {random.choice(['Support materials and resources', 'General correspondence templates'])}

NOTES:
{random.choice([
    'This document serves as a general reference and may be updated periodically.',
    'Please refer to specific departmental guidelines for detailed procedures.',
    'Contact the appropriate department for additional information or clarification.',
    'This material is provided for informational purposes and general guidance.'
])}

For additional information or questions, please contact the relevant department or supervisor.

Document prepared by: {random.choice(self.person_names)}
Department: {random.choice(self.departments)}"""

            other_docs.append({
                'filename': f'other_{i+1:03d}.txt',
                'content': content
            })
        
        return other_docs

    def generate_all_documents(self):
        """Generate all document types."""
        print("🚀 Generating sample documents...")
        
        self.create_output_dir()
        
        # Generate documents by category
        all_documents = []
        all_documents.extend(self.generate_invoices(15))
        all_documents.extend(self.generate_memos(15))
        all_documents.extend(self.generate_contracts(12))
        all_documents.extend(self.generate_legal_documents(12))
        all_documents.extend(self.generate_reports(13))
        all_documents.extend(self.generate_other_documents(13))
        
        # Write documents to files
        for doc in all_documents:
            file_path = os.path.join(self.output_dir, doc['filename'])
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(doc['content'])
        
        print(f"✅ Generated {len(all_documents)} documents in '{self.output_dir}/' folder:")
        print(f"   📄 Invoices: 15")
        print(f"   📝 Memos: 15") 
        print(f"   📋 Contracts: 12")
        print(f"   ⚖️ Legal: 12")
        print(f"   📊 Reports: 13")
        print(f"   📂 Other: 13")
        print(f"   📁 Total: {len(all_documents)} documents")
        
        return len(all_documents)

def main():
    """Main function to generate sample documents."""
    generator = DocumentGenerator()
    total_docs = generator.generate_all_documents()
    
    print(f"\n🎉 Document generation complete!")
    print(f"📂 All {total_docs} documents saved to 'generated_documents/' folder")
    print(f"\n💡 To test with these documents:")
    print(f"   python main.py generated_documents")
    print(f"   python main.py --dashboard")

if __name__ == "__main__":
    main() 