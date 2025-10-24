"""
Comprehensive Test Suite for All OCR Services
Tests: PoS, Term Sheet, PPA, and Invoice OCR endpoints
"""

import requests
import json
import sys
from pathlib import Path
from typing import Dict, Any
import time


class OCRTestSuite:
    """Test suite for all OCR endpoints"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results = {
            "pos": "PoS_A.pdf",
            "termsheet": "TermSheet_Valenz_eMeOH.pdf",
            "ppa": "PPA_Valenz_eMeOH.pdf",
            "invoice": "Invoice_test.pdf"
        }
    
    def print_header(self, title: str):
        """Print formatted header"""
        print("\n" + "=" * 80)
        print(f"  {title}")
        print("=" * 80)
    
    def print_section(self, title: str):
        """Print section header"""
        print(f"\n--- {title} ---")
    
    def test_health_check(self) -> bool:
        """Test API health endpoint"""
        self.print_header("HEALTH CHECK")
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                print("✅ API is healthy")
                print(f"Response: {response.json()}")
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Cannot connect to API: {e}")
            print(f"   Make sure the server is running at {self.base_url}")
            return False
    
    def test_pos_ocr(self, pdf_path: str) -> bool:
        """Test Proof of Sustainability OCR"""
        self.print_header("TESTING: PROOF OF SUSTAINABILITY (PoS) OCR")
        
        if not Path(pdf_path).exists():
            print(f"❌ File not found: {pdf_path}")
            return False
        
        print(f"📄 Processing: {pdf_path}")
        
        try:
            with open(pdf_path, 'rb') as f:
                files = {'file': (Path(pdf_path).name, f, 'application/pdf')}
                start_time = time.time()
                response = requests.post(
                    f"{self.base_url}/api/v1/ocr/pos",
                    files=files,
                    timeout=60
                )
                elapsed = time.time() - start_time
            
            print(f"⏱️  Processing time: {elapsed:.2f}s")
            print(f"📊 Status code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                self.results["pos"] = result
                
                print("\n✅ PoS OCR SUCCESSFUL")
                
                # Display extracted data
                data = result.get('data', {})
                
                self.print_section("Document Info")
                doc_info = data.get('document_info', {})
                print(f"  Type: {doc_info.get('document_type')}")
                print(f"  Unique Number: {doc_info.get('unique_number')}")
                print(f"  Issuance Date: {doc_info.get('issuance_date')}")
                print(f"  Directive: {doc_info.get('directive')}")
                
                self.print_section("Parties")
                parties = data.get('supplier_recipient', {})
                supplier = parties.get('supplier', {})
                recipient = parties.get('recipient', {})
                print(f"  Supplier: {supplier.get('name')}")
                print(f"  Recipient: {recipient.get('name')}")
                
                self.print_section("Feedstock")
                feedstock = data.get('feedstock', {})
                print(f"  Type: {feedstock.get('type')}")
                print(f"  Origin: {feedstock.get('country_of_origin')}")
                print(f"  Waste/Residue: {feedstock.get('is_waste_residue')}")
                
                self.print_section("Fuel Product")
                fuel = data.get('fuel_product', {})
                print(f"  Type: {fuel.get('type')}")
                print(f"  Quantity: {fuel.get('quantity')} {fuel.get('unit')}")
                print(f"  Energy: {fuel.get('energy_content_mj')} MJ")
                print(f"  Production: {fuel.get('country_of_production')}")
                
                self.print_section("GHG Emissions")
                ghg = data.get('ghg_emissions', {})
                print(f"  Total: {ghg.get('total_emissions_gco2eq_mj')} gCO2eq/MJ")
                print(f"  Savings: {ghg.get('emission_saving_percentage')}%")
                
                self.print_section("Compliance")
                compliance = data.get('compliance', {})
                print(f"  RED II Compliant: {compliance.get('red_ii_article_29_compliant')}")
                print(f"  Chain of Custody: {compliance.get('chain_of_custody')}")
                
                self.print_section("Processing Info")
                print(f"  LLM Refined: {data.get('llm_refined')}")
                print(f"  Has Structured Text: {'Yes' if data.get('structured_text') else 'No'}")
                
                return True
            else:
                print(f"\n❌ PoS OCR FAILED")
                print(f"Error: {response.text}")
                return False
                
        except Exception as e:
            print(f"\n❌ PoS OCR ERROR: {str(e)}")
            return False
    
    def test_termsheet_ocr(self, pdf_path: str) -> bool:
        """Test Term Sheet OCR"""
        self.print_header("TESTING: TERM SHEET OCR")
        
        if not Path(pdf_path).exists():
            print(f"❌ File not found: {pdf_path}")
            return False
        
        print(f"📄 Processing: {pdf_path}")
        
        try:
            with open(pdf_path, 'rb') as f:
                files = {'file': (Path(pdf_path).name, f, 'application/pdf')}
                start_time = time.time()
                response = requests.post(
                    f"{self.base_url}/api/v1/ocr/termsheet",
                    files=files,
                    timeout=60
                )
                elapsed = time.time() - start_time
            
            print(f"⏱️  Processing time: {elapsed:.2f}s")
            print(f"📊 Status code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                self.results["termsheet"] = result
                
                print("\n✅ TERM SHEET OCR SUCCESSFUL")
                
                data = result.get('data', {})
                
                self.print_section("Identifiers")
                identifiers = data.get('identifiers', {})
                print(f"  TS ID: {identifiers.get('ts_id')}")
                print(f"  Date: {identifiers.get('date')}")
                print(f"  Expiry: {identifiers.get('expiry')}")
                
                self.print_section("Parties")
                parties = data.get('parties', {})
                print(f"  Seller: {parties.get('seller')}")
                print(f"  Buyer: {parties.get('buyer')}")
                
                self.print_section("Commercial Terms")
                commercial = data.get('commercial', {})
                print(f"  ACQ: {commercial.get('acq')} {commercial.get('acq_unit')}")
                print(f"  Delivery: {commercial.get('delivery')}")
                print(f"  Pricing: {commercial.get('pricing')}")
                
                self.print_section("Sustainability")
                sustainability = data.get('sustainability', {})
                print(f"  CI Target: {sustainability.get('ci_target')}")
                print(f"  Scheme: {sustainability.get('scheme')}")
                
                self.print_section("Timing")
                timing = data.get('timing', {})
                print(f"  Commencement: {timing.get('commencement')}")
                print(f"  Long-Stop: {timing.get('long_stop')}")
                
                self.print_section("Processing Info")
                print(f"  LLM Refined: {data.get('llm_refined')}")
                
                return True
            else:
                print(f"\n❌ TERM SHEET OCR FAILED")
                print(f"Error: {response.text}")
                return False
                
        except Exception as e:
            print(f"\n❌ TERM SHEET OCR ERROR: {str(e)}")
            return False
    
    def test_ppa_ocr(self, pdf_path: str) -> bool:
        """Test PPA OCR"""
        self.print_header("TESTING: POWER PURCHASE AGREEMENT (PPA) OCR")
        
        if not Path(pdf_path).exists():
            print(f"❌ File not found: {pdf_path}")
            return False
        
        print(f"📄 Processing: {pdf_path}")
        
        try:
            with open(pdf_path, 'rb') as f:
                files = {'file': (Path(pdf_path).name, f, 'application/pdf')}
                start_time = time.time()
                response = requests.post(
                    f"{self.base_url}/api/v1/ocr/ppa",
                    files=files,
                    timeout=60
                )
                elapsed = time.time() - start_time
            
            print(f"⏱️  Processing time: {elapsed:.2f}s")
            print(f"📊 Status code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                self.results["ppa"] = result
                
                print("\n✅ PPA OCR SUCCESSFUL")
                
                data = result.get('data', {})
                
                self.print_section("Parties")
                parties = data.get('parties', {})
                seller = parties.get('seller', {})
                buyer = parties.get('buyer', {})
                print(f"  Seller: {seller.get('name')} ({seller.get('registration')})")
                print(f"  Buyer: {buyer.get('name')} ({buyer.get('registration')})")
                
                self.print_section("Key Terms")
                key_terms = data.get('key_terms', {})
                print(f"  Project ID: {key_terms.get('project_id')}")
                print(f"  Commodity: {key_terms.get('commodity')}")
                print(f"  Effective Date: {key_terms.get('effective_date')}")
                print(f"  Duration: {key_terms.get('duration')}")
                print(f"  ACQ: {key_terms.get('acq')} {key_terms.get('acq_unit')}")
                print(f"  Monthly Plan: {key_terms.get('monthly_plan')} t ({key_terms.get('monthly_tolerance')})")
                print(f"  Delivery: {key_terms.get('delivery')}")
                print(f"  Customs: {key_terms.get('customs')}")
                
                self.print_section("Pricing")
                pricing = data.get('pricing', {})
                print(f"  Price (Y1-Y5): {pricing.get('price_y1_y5')} {pricing.get('currency')}/t")
                
                self.print_section("Sustainability & Compliance")
                sustainability = data.get('sustainability_compliance', {})
                print(f"  CI Limit: {sustainability.get('ci_limit')}")
                print(f"  Certification: {sustainability.get('certification')}")
                print(f"  Audit Required: {sustainability.get('audit_required')}")
                print(f"  Auditor Signature: {sustainability.get('auditor_signature')}")
                
                self.print_section("Commencement")
                commencement = data.get('commencement', {})
                print(f"  Rule: {commencement.get('commencement_rule')}")
                print(f"  Long-Stop: {commencement.get('long_stop_date')}")
                
                self.print_section("Processing Info")
                print(f"  LLM Refined: {data.get('llm_refined')}")
                
                return True
            else:
                print(f"\n❌ PPA OCR FAILED")
                print(f"Error: {response.text}")
                return False
                
        except Exception as e:
            print(f"\n❌ PPA OCR ERROR: {str(e)}")
            return False
    
    def test_invoice_ocr(self, pdf_path: str) -> bool:
        """Test Invoice OCR"""
        self.print_header("TESTING: INVOICE OCR")
        
        if not Path(pdf_path).exists():
            print(f"❌ File not found: {pdf_path}")
            return False
        
        print(f"📄 Processing: {pdf_path}")
        
        try:
            with open(pdf_path, 'rb') as f:
                files = {'file': (Path(pdf_path).name, f, 'application/pdf')}
                start_time = time.time()
                response = requests.post(
                    f"{self.base_url}/api/v1/ocr/invoice",
                    files=files,
                    timeout=60
                )
                elapsed = time.time() - start_time
            
            print(f"⏱️  Processing time: {elapsed:.2f}s")
            print(f"📊 Status code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                self.results["invoice"] = result
                
                print("\n✅ INVOICE OCR SUCCESSFUL")
                
                data = result.get('data', {})
                
                self.print_section("Identifiers")
                identifiers = data.get('identifiers', {})
                print(f"  Invoice No: {identifiers.get('invoice_no')}")
                print(f"  Issue Date: {identifiers.get('issue_date')}")
                print(f"  Payment Due: {identifiers.get('payment_due')}")
                
                self.print_section("Parties")
                parties = data.get('parties', {})
                print(f"  Supplier: {parties.get('supplier')}")
                print(f"  Buyer: {parties.get('buyer')}")
                
                self.print_section("Billing Period")
                billing = data.get('billing_period', {})
                print(f"  Period: {billing.get('period_start')} → {billing.get('period_end')}")
                
                self.print_section("Product & Amount")
                product = data.get('product_amount', {})
                print(f"  Product: {product.get('product')}")
                print(f"  Quantity: {product.get('quantity')} {product.get('unit')}")
                print(f"  Unit Price: {product.get('unit_price_currency')}{product.get('unit_price')}/t")
                print(f"  Amount (excl. VAT): {product.get('amount_currency')}{product.get('amount_excl_vat')}")
                
                self.print_section("Logistics")
                logistics = data.get('logistics', {})
                print(f"  Incoterm: {logistics.get('incoterm')}")
                print(f"  Customs: {logistics.get('customs')}")
                
                self.print_section("Processing Info")
                print(f"  LLM Refined: {data.get('llm_refined')}")
                
                return True
            else:
                print(f"\n❌ INVOICE OCR FAILED")
                print(f"Error: {response.text}")
                return False
                
        except Exception as e:
            print(f"\n❌ INVOICE OCR ERROR: {str(e)}")
            return False
    
    def save_results(self, output_file: str = "ocr_test_results.json"):
        """Save all test results to JSON file"""
        self.print_header("SAVING TEST RESULTS")
        
        try:
            with open(output_file, 'w') as f:
                json.dump(self.results, f, indent=2)
            print(f"✅ Results saved to: {output_file}")
            return True
        except Exception as e:
            print(f"❌ Error saving results: {e}")
            return False
    
    def print_summary(self):
        """Print test summary"""
        self.print_header("TEST SUMMARY")
        
        summary = {
            "PoS": "✅ PASSED" if self.results.get("pos") else "❌ FAILED",
            "Term Sheet": "✅ PASSED" if self.results.get("termsheet") else "❌ FAILED",
            "PPA": "✅ PASSED" if self.results.get("ppa") else "❌ FAILED",
            "Invoice": "✅ PASSED" if self.results.get("invoice") else "❌ FAILED"
        }
        
        for doc_type, status in summary.items():
            print(f"  {doc_type:15s}: {status}")
        
        total = len(summary)
        passed = sum(1 for s in summary.values() if "PASSED" in s)
        
        print(f"\n  Total: {passed}/{total} tests passed")
        
        if passed == total:
            print("\n  🎉 ALL TESTS PASSED! 🎉")
        else:
            print(f"\n  ⚠️  {total - passed} test(s) failed")


def main():
    """Main test runner"""
    print("\n" + "=" * 80)
    print("  OCR API - COMPREHENSIVE TEST SUITE")
    print("=" * 80)
    
    # Get base URL (default: localhost:8000)
    base_url = input("\nEnter API URL (default: http://localhost:8000): ").strip()
    if not base_url:
        base_url = "http://localhost:8000"
    
    # Initialize test suite
    suite = OCRTestSuite(base_url)
    
    # Test health check first
    if not suite.test_health_check():
        print("\n⚠️  Cannot proceed without healthy API. Exiting.")
        return
    
    # Get file paths
    print("\n" + "-" * 80)
    print("  SPECIFY TEST FILES")
    print("-" * 80)
    
    pos_path = input("\nPoS PDF path (or press Enter to skip): ").strip()
    termsheet_path = input("Term Sheet PDF path (or press Enter to skip): ").strip()
    ppa_path = input("PPA PDF path (or press Enter to skip): ").strip()
    invoice_path = input("Invoice PDF path (or press Enter to skip): ").strip()
    
    # Run tests
    if pos_path:
        suite.test_pos_ocr(pos_path)
    
    if termsheet_path:
        suite.test_termsheet_ocr(termsheet_path)
    
    if ppa_path:
        suite.test_ppa_ocr(ppa_path)
    
    if invoice_path:
        suite.test_invoice_ocr(invoice_path)
    
    # Save results
    save_results = input("\nSave results to JSON? (y/n): ").strip().lower()
    if save_results == 'y':
        output_file = input("Output file name (default: ocr_test_results.json): ").strip()
        if not output_file:
            output_file = "ocr_test_results.json"
        suite.save_results(output_file)
    
    # Print summary
    suite.print_summary()


def quick_test(pos_path=None, termsheet_path=None, ppa_path=None, invoice_path=None):
    """Quick test function for programmatic use"""
    suite = OCRTestSuite()
    
    if not suite.test_health_check():
        return False
    
    results = {}
    if pos_path:
        results['pos'] = suite.test_pos_ocr(pos_path)
    if termsheet_path:
        results['termsheet'] = suite.test_termsheet_ocr(termsheet_path)
    if ppa_path:
        results['ppa'] = suite.test_ppa_ocr(ppa_path)
    if invoice_path:
        results['invoice'] = suite.test_invoice_ocr(invoice_path)
    
    suite.print_summary()
    return all(results.values())


if __name__ == "__main__":
    main()