import time
import selenium 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager



def profile_builder_agent(linkedin_url: str) -> dict:
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    profile_data = {
        "name": "",
        "about": "",
        "experience": [],
        "education": [],
        "skills": [],
        "certifications": []
    }

    try:
        driver.get(linkedin_url)
        time.sleep(5)  # allow JS to load

        # Scroll to bottom to load all sections
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        # --- Name ---
        try:
            name = driver.find_element(By.CSS_SELECTOR, "h1.text-heading-xlarge")
            profile_data["name"] = name.text.strip()
        except:
            profile_data["name"] = "N/A"

        # --- About ---
        try:
            about = driver.find_element(By.ID, "about")
            profile_data["about"] = about.text.strip()
        except:
            profile_data["about"] = "N/A"

        # --- Experience ---
        try:
            exp_section = driver.find_element(By.ID, "experience")
            jobs = exp_section.find_elements(By.XPATH, ".//li")
            for job in jobs:
                title = job.find_element(By.TAG_NAME, "h3").text
                company = job.find_element(By.CLASS_NAME, "t-14.t-normal").text
                date_loc = job.find_elements(By.CLASS_NAME, "t-14.t-normal.t-black--light")
                dates = date_loc[0].text if date_loc else ""
                description = job.text
                profile_data["experience"].append({
                    "title": title,
                    "company": company,
                    "dates": dates,
                    "description": description
                })
        except:
            pass

        # --- Education ---
        try:
            edu_section = driver.find_element(By.ID, "education")
            schools = edu_section.find_elements(By.XPATH, ".//li")
            for school in schools:
                school_name = school.find_element(By.TAG_NAME, "h3").text
                degree = school.find_element(By.CLASS_NAME, "t-14.t-normal").text
                dates = school.find_elements(By.CLASS_NAME, "t-14.t-normal.t-black--light")
                grad_year = dates[0].text if dates else ""
                profile_data["education"].append({
                    "school": school_name,
                    "degree": degree,
                    "dates": grad_year
                })
        except:
            pass

        # --- Skills ---
        try:
            driver.get(linkedin_url + "details/skills/")
            time.sleep(3)
            skills = driver.find_elements(By.CLASS_NAME, "pvs-entity__skill-name")
            profile_data["skills"] = [s.text.strip() for s in skills]
        except:
            pass

        # --- Certifications ---
        try:
            driver.get(linkedin_url + "details/licenses-certifications/")
            time.sleep(3)
            certs = driver.find_elements(By.CLASS_NAME, "pvs-entity")
            for c in certs:
                cert_name = c.find_element(By.TAG_NAME, "span").text
                profile_data["certifications"].append(cert_name)
        except:
            pass

    except Exception as e:
        profile_data["error"] = str(e)

    finally:
        driver.quit()

    return profile_data


