'''
conda env list
# conda environments:
#
base                  *  /opt/miniconda3
deepmd-cpu               /opt/miniconda3/envs/deepmd-cpu
pymatgen                 /opt/miniconda3/envs/pymatgen

conda remove --yes --name pymatgen --all
conda create --yes --name pymatgen python
source activate pymatgen  # OSX or Linux
conda install --yes --channel conda-forge pymatgen
conda install --yes numpy scipy matplotlib selenium
pip install --yes pymatgen selenium
'''

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import os

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

file_CWD = os.getcwd()

input_file_name = "input.in"
#input_file_name = "input.cif"

#chrome_driver_path = "/opt/webdriver/chromedriver"

# Specify the path to the downloaded ChromeDriver binary
service = Service("/opt/webdriver/chromedriver")  # Update with your actual path


#options = webdriver.ChromeOptions()
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--incognito')

# 啟動Chrome WebDriver
#driver = webdriver.Chrome(chrome_driver_path, options=options)
driver = webdriver.Chrome(service=service, options=options)

# 輸入檔案的路徑
input_file_path = os.path.join(os.getcwd(), input_file_name)

# 目標網站
driver.get("https://www.materialscloud.org/work/tools/qeinputgenerator")

#driver.implicitly_wait(5) #隱式等待，網頁載入分2階段，因為要等frame(0)出現而不是單純等待網頁載入所以不能用!!!
WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME,"structurefile"))) #顯式等待，把frame(0)出現並可切換當作等到條件
#------------------------------------
# 上傳結構文件
#driver.switch_to.frame(0)
#Structurefile = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[1]/div[3]/form/div/div[1]/div[2]/input").send_keys(input_file_path)#0404
Structurefile = driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/div[1]/div[3]/form/div/div[2]/div[1]/div[2]/input").send_keys(input_file_path)
driver.implicitly_wait(1)

#----------選FileformatSelect----------
fileformat = driver.find_element(By.ID, "fileformatSelect")
fileformat.click()
#fileformat_Select = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[1]/div[3]/form/div/div[2]/div[2]/select/option[1]")### Quantum ESPRESSO input [parser: qetools]
#fileformat_Select = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/form/div/div[2]/div[2]/select/option[2]")### CIF File (.cif) [parser: ase]
#fileformat_Select = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/form/div/div[2]/div[2]/select/option[3]")### CIF File (.cif) [parser: pymatgen]/html/body/div[1]/div[3]/form/div/div[2]/div[2]/select/option[3]
fileformat_Select = driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/div[1]/div[3]/form/div/div[2]/div[2]/div[2]/select/option[1]")### Quantum ESPRESSO input [parser: qetools]
fileformat_Select.click()
#------------------------------------

#----------選protocol----------
protocol = driver.find_element(By.ID, "protocolSelect")
protocol.click()
#time.sleep(10)
protocol_Select = driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/div[1]/div[3]/form/div/div[5]/div[2]/select/option[1]")#fast
protocol_Select.click()
#------------------------------------

#----------選XC_functional----------
#with open("debug_xcfunctional.html", "w", encoding="utf-8") as f:
#    f.write(driver.page_source)
xcFunctional = driver.find_element(By.ID, "xcFunctionalSelect")
xcFunctional.click()
xcFunctional_Select = driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/div[1]/div[3]/form/div/div[6]/div[2]/select/option[2]") # PBE
xcFunctional_Select.click()
#------------------------------------

#----------選MagnetizationSelect----------
Magnetization = driver.find_element(By.ID, "magnetizationSelect")
Magnetization.click()
#time.sleep(1)
#MagnetizationSelect = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/form/div/div[5]/div[2]/select/option[1]")### non-magnetic metal (fractional occupations)
#MagnetizationSelect = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/form/div/div[5]/div[2]/select/option[2]")### non-magnetic insulator (fixed occupations)
#MagnetizationSelect = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[1]/div[3]/form/div/div[5]/div[2]/select/option[3]")### magnetic (fractional occupations)
Magnetization_Select = driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/div[1]/div[3]/form/div/div[7]/div[2]/select/option[3]")### magnetic (fractional occupations)
Magnetization_Select.click()
#------------------------------------

#----------Refine_cell ----------
refineCell = driver.find_element(By.ID, "refineCellSelect")
refineCell.click()
refineCell_Select = driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/div[1]/div[3]/form/div/div[8]/div[2]/select/option[1]")#No
refineCell_Select.click()

#------------------------------------

#-------點擊Advanced_settings--------
advanced_checkbox = driver.find_element(By.ID, "accordion-toggle")
driver.execute_script("arguments[0].click();", advanced_checkbox)

#------------------------------------

#----------選PseudoSelect----------
pseudo = driver.find_element(By.ID, "pseudoSelectAdvanced")
pseudo.click()
pseudo_SelectAdvanced = driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/div[1]/div[3]/form/div/div[9]/div/div/div[1]/div[2]/select/option[2]")### SSSP 1.3: Efficiency PBE 
pseudo_SelectAdvanced.click()
#------------------------------------

#---------選KmeshSelect-----------
kmesh = driver.find_element(By.ID, "kmeshSelectAdvanced")
kmesh.click()
kmesh_SelectAdvanced = driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/div[1]/div[3]/form/div/div[9]/div/div/div[2]/div[2]/select/option[2]")### coarse (0.30 1/Å, 0.0275 Ry)
kmesh_SelectAdvanced.click()
#------------------------------------

#------------------------------------
###----------按Generate the PWscf input file----------
#Generate_the_PWscf_input_file = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[1]/div[3]/form/div/div[8]/input")
Generate_the_PWscf_input_file = driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/div[1]/div[3]/form/div/div[10]/input")
Generate_the_PWscf_input_file.click()
#------------------------------------
WebDriverWait(driver, 3)
#------------------------------------
##------有Warning按Got it!------------------
try:
    button = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[3]/div/div[4]/div/div/div[3]/button"))
    )
    do_generate_pwscf_input_file = True
except (NoSuchElementException,TimeoutException):
    do_generate_pwscf_input_file = False
if do_generate_pwscf_input_file:
    Generate_the_PWscf_input_file = driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/div[4]/div/div/div[3]/button")
    Generate_the_PWscf_input_file.click()
    
time.sleep(2)

#拿PWscf_input舊
PWscf_inputs = driver.find_element(By.ID, "qepwinput")
text = PWscf_inputs.text

# # 拿PWscf_input新
# PWscf_inputs = driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/div[2]/div[1]/div[4]/div[2]/div[2]/p/button")
# PWscf_inputs.click()
# text = pyperclip.paste()

# print(text,"\n")
# 寫入output.in
output_file_name = "output.in"
with open(output_file_name, 'w') as output_file:
    output_file.write(text)

# 關掉chrome
driver.quit()
#print("PWscf get!")
