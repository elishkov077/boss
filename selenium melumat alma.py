from selenium import webdriver
from selenium.webdriver.firefox.service import Service  # Firefox için doğru Service sınıfı
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pandas as pd

class BOSS:
    def __init__(self):
        path = r'C:\Users\BAKU\Desktop\geckodriver-v0.35.0-win64\geckodriver.exe'
        service = Service(executable_path=path)  # Doğru Service sınıfı kullanıldı
        self.driver = webdriver.Firefox(service=service)  # options parametresi de eklendi
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver,20)
        self.liste = []
        self.max_page = 4

    def sayt (self,url):
        self.url = url
        self.driver.get(self.url)

    def scrapy(self):
        baslangic = 0
        while baslangic < self.max_page:
            databes = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,".results-i")))
            for veri in databes:
                basliq = veri.find_element(By.CSS_SELECTOR,".results-i-title").text
                maas = veri.find_element(By.CSS_SELECTOR,".results-i-salary.salary").text
                self.liste.append((basliq,maas))
                print(basliq,maas)

            try:
                nextt = self.wait.until(EC.element_to_be_clickable((By.XPATH,"//a[@rel = 'next']")))
                sleep(1)
                nextt.click()
                baslangic += 1
            except Exception as inner_e:
                print(inner_e)
                break

    def save(self,fay_adi):
        df = pd.DataFrame(self.liste,columns=["ELAN","MAAS"])
        df.to_excel(fay_adi,sheet_name="elan",index=False)
        print("Fayl Yuklenildi.....")

    def quit(self):
        self.driver.quit()
                    

    
if __name__ == "__main__":
    view = BOSS()
    view.sayt("https://boss.az/vacancies?search%5Bcategory_id%5D=133")
    view.scrapy()
    view.save("test.xlsx")
    view.quit()

