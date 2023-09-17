from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pytesseract
import pandas as pd
import csv

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

def scraper(url):
    """
    Scrapes data from a web page and extracts a table.

    Parameters:
        url (str): The URL of the web page to scrape.

    Returns:
        pd.DataFrame: A DataFrame containing the scraped data.
    """
    driver.get(url)
    
    #select year: 2023
    year_number = driver.find_element(By.ID, "dbselect")
    year_dropdown = Select(year_number) 
    year_dropdown.select_by_index(30)
    time.sleep(5)   #waits for 5 seconds to emulate human behaviour

    #select District: मुंबई उपनगर
    district_name = driver.find_element(By.ID, "district_id")
    district_dropdown = Select(district_name)
    district_dropdown.select_by_value(str(37))
    time.sleep(5)

    #select Taluka: अंधेरी
    taluka_name = driver.find_element(By.ID, "taluka_id")
    taluka_dropdown = Select(taluka_name)
    taluka_dropdown.select_by_value(str(1))
    time.sleep(5)

    #select Village: बांद्रा
    village_name = driver.find_element(By.ID,  "village_id")
    village_dropdown = Select(village_name)
    village_dropdown.select_by_value(str(57))
    time.sleep(5)

    #Enter Doc/Property/CTS/Survey no/Reg. Year: 2023
    search = driver.find_element(By.ID,"free_text")
    search.send_keys("2023")
    search.send_keys(Keys.RETURN)
    time.sleep(5)

    #CAPTCHA Automation 
    # captcha_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'captchacode')))

    # # prepare captcha image for OCR
    # captcha_element.screenshot("./image.png")
    # image = Image.open("./image.png")
    # pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

    # # Perform OCR on the CAPTCHA image and extract text
    # text = pytesseract.image_to_string(image).strip()

    # captcha_box = driver.find_element(By.ID, 'cpatchaTextBox')
    # captcha_box.send_keys(text)
    
    # #click on search button  
    # search_button = driver.find_element(By.ID, 'submit')
    # search_button.click()
   

    #Select number of entries: 50   
    number_of_entries = driver.find_element(By.NAME, "tableparty_length")
    entries_dropdown = Select(number_of_entries)
    entries_dropdown.select_by_value(str(50))

    time.sleep(60) #allow additional time for Google Translate extension to translate the webpage

    #extracting data from table
    table = driver.find_element(By.XPATH, "//table[@id='tableparty']")
    table_headers = table.find_elements(By.TAG_NAME, "th")
    header_list = [header.text for header in table_headers]

    data_rows = []
    links=[]
    table_rows = table.find_elements(By.TAG_NAME, "tr")[1:]
    button_elements = table.find_elements(By.CSS_SELECTOR, "tr td:last-child a")   #extract link from button in last column of table
    for i,row in enumerate(table_rows):
        row_data = [cell.text for cell in row.find_elements(By.TAG_NAME, "td")]  
        data_rows.append(row_data)
        link = button_elements[i].get_attribute("href")  # Extract the link from the corresponding button
        links.append(link)
        row_data.append(link)  # Add the link to the row data
        data_rows.append(row_data)

    df = pd.DataFrame(data_rows, columns=header_list + ["Link"])
    return df

if __name__ == "__main__":
    data=scraper("https://pay2igr.igrmaharashtra.gov.in/eDisplay/Propertydetails/index")
    print(data)
    driver.quit()
    file_path=  'C:/Users/Kartik/Desktop/PropReturns Task/mumbai_realestate.csv'
    data.to_csv(file_path, index=False)
