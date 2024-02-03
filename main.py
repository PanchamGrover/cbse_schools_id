# installing libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import re
import math
import os

url = "https://saras.cbse.gov.in/saras/AffiliatedList/ListOfSchdirReport"


# defining functions
def get_table_data():

    global table_no
    table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "myTable")))

    rows = table.find_elements(By.TAG_NAME, "tr")
    data = []
    for row in rows[1:]:
        cells = row.find_elements(By.TAG_NAME, "td")
        row_data = [cell.text for cell in cells]
        data.append(row_data)
    table_data = pd.DataFrame(data)
    filename = f"table_data_{table_no}.csv"
    filepath = os.path.join(folder_name, filename)
    table_data.to_csv(filepath, index=False)



def next_button():
    # next = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME,"paginate_button next")))
    # next = driver.find_element(By.ID, "Button1")
    next = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "myTable_next")))

    driver.execute_script("arguments[0].scrollIntoView(true);", next)
    time.sleep(4)
    next.click()


def no_of_entry():
    element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//select[@name="myTable_length" and @aria-controls="myTable"]')))
    # creating a select element
    entries = Select(element)
    entries.select_by_index(3)


state_list = ['ANDAMAN & NICOBAR', 'ANDHRA PRADESH', 'ARUNACHAL PRADESH', 'ASSAM', 'BIHAR', 'CHANDIGARH',
              'CHHATTISGARH', 'DADRA & NAGAR HAVELI', 'DAMAN & DIU', 'DELHI', 'GOA', 'GUJARAT', 'HARYANA',
              'HIMACHAL PRADESH','JAMMU & KASHMIR', 'JHARKHAND', 'KARNATAKA', 'KERALA', 'LAKSHADWEEP', 'MADHYA PRADESH',
              'MAHARASHTRA', 'MANIPUR', 'MEGHALAYA', 'MIZORAM', 'NAGALAND', 'ODISHA', 'PUDUCHERRY', 'PUNJAB',
              'RAJASTHAN', 'SIKKIM', 'TAMIL NADU', 'TELANGANA', 'TRIPURA', 'UTTAR PRADESH', 'UTTARAKHAND',
              'WEST BENGAL']

# MAKING A FOR LOOP FOR EACH STATE
for state in state_list:
    driver = webdriver.Chrome()
    driver.get(url=url)
    time.sleep(4)

    state_wise = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "SearchMainRadioState_wise")))

    state_wise.click()
    time.sleep(4)

    state_dropdown = Select(driver.find_element(By.ID, "State"))
    state_to_select = state
    state_dropdown.select_by_visible_text(state_to_select)
    time.sleep(3)

    search = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//input[@class="btn btn-primary actionBtn"]')))
    search.click()

# the no of times Code should run
    table_info =WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "myTable_info")))

    info = table_info.text
    # Use regular expression to extract the number
    matches = re.findall(r'\b\d+\b', info)
    print(matches)
    if len(matches) == 3:
        no_of_entries = matches[2]

    else:
        # Combine the last two entries into one string
        no_of_entries = matches[2] + matches[3]

    no = int(no_of_entries)/100
    if int(no_of_entries) % 100 == 0:
        code_run_times = int(no)
    else:
        code_run_times = math.ceil(no)

    print(code_run_times)

    table_no = 1

    # Making a folder with the state name
    folder_name = f"{state_to_select}_data"
    # Create the folder if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    while table_no != (code_run_times+1):
        time.sleep(4)
        no_of_entry()
        get_table_data()
        next_button()
        table_no += 1

    driver.quit()

