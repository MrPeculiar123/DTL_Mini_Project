import os
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import date

# Import your DB logic to save results automatically
from backend.src.db.session import SessionLocal
from backend.src.models.rfp import RFPModel
from backend.src.services.pdf_service import extract_text_from_pdf

# Configuration
MOCK_PORTAL_URL = "http://localhost:8080"
DOWNLOAD_DIR = "backend/data/uploads"

def run_scraper():
    print(f"🕵️  Scraper searching {MOCK_PORTAL_URL}...")
    
    # Setup Headless Chrome (doesn't open a visible window)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless") 
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(MOCK_PORTAL_URL)
        time.sleep(2) # Wait for page load

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        tenders = soup.find_all('div', class_='tender-row')

        db = SessionLocal()

        for tender in tenders:
            title = tender.find('h2').text
            due_date_str = tender.find('span', class_='due-date').text
            link = tender.find('a', class_='download-link')['href']
            
            # Check if we already have this RFP
            exists = db.query(RFPModel).filter(RFPModel.title == title).first()
            if exists:
                print(f"⚠️  Skipping existing RFP: {title}")
                continue

            print(f"⬇️  Found new RFP: {title}. Downloading...")
            
            # Download the PDF
            pdf_url = f"{MOCK_PORTAL_URL}/{link}"
            response = requests.get(pdf_url)
            
            filename = f"scraped_{int(time.time())}.pdf"
            file_path = os.path.join(DOWNLOAD_DIR, filename)
            
            with open(file_path, 'wb') as f:
                f.write(response.content)

            # Auto-Extract Text (Your Phase 2 logic)
            extracted_text = extract_text_from_pdf(file_path)

            # Save to Database
            new_rfp = RFPModel(
                title=title,
                portal="Mock Gov Portal",
                due_date=date.fromisoformat(due_date_str),
                status="NEW",
                filename=filename,
                file_path=file_path,
                extracted_text=extracted_text
            )
            db.add(new_rfp)
            db.commit()
            print(f"✅ Saved to DB: {title}")

    except Exception as e:
        print(f"❌ Scraping Error: {e}")
    finally:
        driver.quit()
        db.close()

if __name__ == "__main__":
    # Ensure upload directory exists
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    run_scraper()