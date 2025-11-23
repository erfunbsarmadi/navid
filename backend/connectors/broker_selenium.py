# connectors/broker_selenium.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time




def fetch_holdings(username, password, login_url, holdings_url):
opts = Options()
opts.add_argument('--headless=new')
driver = webdriver.Chrome(options=opts)
try:
driver.get(login_url)
driver.find_element(By.ID, 'username').send_keys(username)
driver.find_element(By.ID, 'password').send_keys(password)
driver.find_element(By.ID, 'loginBtn').click()
# TODO: implement robust explicit waits & 2FA handling
time.sleep(4)
driver.get(holdings_url)
rows = driver.find_elements(By.CSS_SELECTOR, '.holdings-row')
holdings = []
for r in rows:
ticker = r.find_element(By.CSS_SELECTOR, '.ticker').text
qty = float(r.find_element(By.CSS_SELECTOR, '.qty').text.replace(',',''))
price = float(r.find_element(By.CSS_SELECTOR, '.price').text.replace(',',''))
holdings.append({'ticker': ticker, 'qty': qty, 'price': price})
return holdings
finally:
driver.quit()
