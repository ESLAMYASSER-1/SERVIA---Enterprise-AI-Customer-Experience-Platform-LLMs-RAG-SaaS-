from logging import getLogger
import pandas as pd
import json
import re
import requests
from urllib.parse import urlparse, parse_qs

from .BaseController import BaseController

logger = getLogger(__name__)

class DataController(BaseController):
    def __init__(self):
        super().__init__()
        
    
    def get_csv_url(self, sheet_url):
        """Convert Google Sheet URL to CSV export URL"""
        
        if sheet_url.endswith('.csv') or 'export?format=csv' in sheet_url:
            return sheet_url
        
        parsed = urlparse(sheet_url)
        
        if '/spreadsheets/d/' in sheet_url:
            doc_id = sheet_url.split('/spreadsheets/d/')[1].split('/')[0]
        elif '/d/' in sheet_url:
            doc_id = sheet_url.split('/d/')[1].split('/')[0]
        else:
            doc_id = None
        
        if not doc_id:
            raise ValueError("Could not extract document ID from the URL")
        
        csv_url = f"https://docs.google.com/spreadsheets/d/{doc_id}/export?format=csv"
        
        if 'gid=' in sheet_url:
            gid = sheet_url.split('gid=')[1].split('&')[0].split('#')[0]
            csv_url += f"&gid={gid}"
        
        return csv_url
    
    def get_data_from_GoogleForm(self, csv_path: str, sheet_url:str):
        try:
            # Get the proper CSV URL
            csv_url = self.get_csv_url(sheet_url)
            
            
            
            # Method 1: Try pandas first
            try:
                df = pd.read_csv(csv_url)
            except Exception as e:
                logger.error(f"❌ failed to read the data with pandas: {e}")
                logger.info("trying with request...")                
                # Method 2: Use requests with proper headers
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                response = requests.get(csv_url, headers=headers)
                response.raise_for_status()
                
                # Load the CSV content into pandas
                from io import StringIO
                df = pd.read_csv(StringIO(response.text))
                logger.info("✅ Successfully loaded with requests")
            
            if len(df) > 0:
                pass
            else:
                logger.error("⚠️  No data found in the sheet")
            
            # Save files
            df.to_csv(csv_path, index=False, encoding="utf-8")
            logger.info(f"✅ DATA CSV FILE Updated({csv_path})...")

            return True
        except Exception as e:
            logger.error(f"❌ Error: {e}")

            return False

    def csv_to_structured_json(self, csv_path: str, company_name: str, output_path: str = None):
        """
        Convert a single company's data from CSV into structured JSON format.
        
        Args:
            csv_path (str): Path to the CSV file.
            company_name (str): The exact company name to search for.
            output_path (str, optional): Path to save the generated JSON file.

        Returns:
            dict: Structured company data as a JSON-like dictionary.
        """

        df = pd.read_csv(csv_path)

        name_col = [c for c in df.columns if "company name" in c.lower()]
        if not name_col:
            raise ValueError("No column found for company name.")
        name_col = name_col[0]

        company_row = df[df[name_col].str.strip().str.lower() == company_name.strip().lower()]
        if company_row.empty:
            raise ValueError(f"Company '{company_name}' not found in CSV.")

        row = company_row.iloc[0]

        def get(col):
            match = [c for c in df.columns if col.lower() in c.lower()]
            if not match:
                return None
            val = str(row[match[0]]).strip()
            return None if val.lower() in ["nan", "none", ""] else val

        # Parse branches text into structured list
        branches_text = get("branches addresses and location")
        branches = []
        if branches_text:
            for part in re.split(r";|\n", branches_text):
                part = part.strip()
                if not part:
                    continue
                match = re.match(r"(.*?):\s*(.*)", part)
                if match:
                    city = match.group(1).strip()
                    address = match.group(2).strip()
                    branch_type = "main" if "main" in city.lower() else None
                    city = re.sub(r"\(.*?\)", "", city).strip()
                    branches.append({
                        "city": city,
                        "address": address,
                        **({"type": branch_type} if branch_type else {})
                    })

        # Build structured JSON
        company_json = {
            "company_name": get("company name"),
            "industry": get("industry/sector"),
            "vision": get("vision"),
            "offerings": get("provide or offer"),
            "description": get("brief about your company"),
            "branch_count": get("how many branch") or '',
            "main_branch": get("main branch"),
            "branches": branches,
            "working_hours": get("working ours and days"),
            "offers": {
                "seasonal": get("seasonal offers") ,
                "yearly": get("yearly offers") ,
                "coupons": get("coupons") ,
                "max_discount": get("maximum limits for offers"),
                "platform": get("preferred platform for offers"),
            },
            "payment_methods": {
                "national": get("best national payment methods"),
                "international": get("best international payment methods"),
                "installments": get("installment systems"),
            },
            "delivery": {
                "available": get("provide delivery"),
                "express": get("express delivery") ,
                "methods": get("delivery distinction"),
                "countries": [c.strip() for c in (get("countries do you provide delivery") or "").split(",") if c.strip()],
                "special_cases": get("special cases delivery") ,
                "offers": get("offers for delivery"),
            },
            "social_media": {},
            "social_activity": get("social media updates periods"),
            "customer_service": get("reach human customer service"),
            "available_platforms": [p.strip() for p in (get("available platforms") or "").split(",") if p.strip()],
        }

        # Parse social media links
        sm_text = get("social media links")
        if sm_text:
            for part in re.split(r"[\n,]+", sm_text):
                if ":" in part:
                    platform, link = part.split(":", 1)
                    company_json["social_media"][platform.strip().lower()] = link.strip()

        # Save to file if requested
        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(company_json, f, ensure_ascii=False, indent=2)

        return company_json


    def json_to_chunks(self, data):
        chunks = []

        chunks.append(f"{data['company_name']} operates in {data['industry']}. "
                    f"Vision: {data['vision']} "
                    f"They offer {data['offerings']} and are described as {data['description']}.")

        branches_text = "They have branches in: " + "; ".join(
            [f"{b['city']} ({b.get('address', 'No address provided')})" for b in data['branches']]
        )
        chunks.append(branches_text)

        offers = data['offers']
        chunks.append(f"Offers: Seasonal={offers['seasonal']}, Yearly={offers['yearly']}, "
                    f"Coupons={offers['coupons']}, Max discount={offers['max_discount']}.")

        chunks.append(f"Payment options include {data['payment_methods']['national']} "
                    f"and international options like {data['payment_methods']['international']}.")

        chunks.append(f"Delivery is available to {', '.join(data['delivery']['countries'])}. "
                    f"Methods: {data['delivery']['methods']}. Offers: {data['delivery']['offers']}.")

        chunks.append("Social Media: " + ", ".join([f"{k}: {v}" for k, v in data['social_media'].items()]))

        chunks.append(f"Customer service through {data['customer_service']}.")
        chunks.append(f"Available platforms: {', '.join(data['available_platforms'])}.")

        return chunks


    def get_company_chunks(self, google_sheet_url:str, company_name: str, output_path: str = None):
        csv_path = self.get_row_data_path()
        logger.info("start updating data file....")
        if self.get_data_from_GoogleForm(csv_path, google_sheet_url):
            logger.info("data has been downloaded from google sheets")
        else:
            raise ReferenceError("Google Sheet URL does not exist!!")


        data = self.csv_to_structured_json(csv_path, company_name, output_path)
        chunks = self.json_to_chunks(data)
        logger.info(f"🏢 got chunks for company: {company_name}")

        if chunks ==[] or chunks is None:
            logger.error(f"can't get company:{company_name} chunks!! ")
            return None 
        
        return chunks
