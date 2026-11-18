import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

options = Options()
options.add_argument("-profile")
options.add_argument("/home/tnoko/.mozilla/selenium-profiili")

driver = webdriver.Firefox(options=options)
driver.get("https://play.google.com/books/reader?id=gn6aEQAAQBAJ&pg=GBS.PT1")
time.sleep(5)

tiedostonimi = "kirja_vihrea.txt"
muistissa_oleva_teksti = ""
peräkkäiset_samat = 0
maksimisivut = 500

# Tyhjennetään tai luodaan uusi tiedosto alussa
with open(tiedostonimi, "w", encoding="utf-8") as f:
    f.write("--- KIRJAN LUKU ALKAA ---\n\n")

for i in range(maksimisivut):
    driver.switch_to.default_content()
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    
    page_text = ""
    aktiivinen_frame = None
    
    for frame in iframes:
        try:
            driver.switch_to.frame(frame)
            body_element = driver.find_element(By.TAG_NAME, "body")
            body_text = body_element.text.strip()
            if len(body_text) > 40:
                page_text = body_text
                aktiivinen_frame = frame
                break
        except Exception:
            pass
        finally:
            driver.switch_to.default_content()

    # Tarkistetaan, tapahtuiko sivunvaihto
    if page_text and page_text != muistissa_oleva_teksti:
        muistissa_oleva_teksti = page_text
        peräkkäiset_samat = 0
        
        # Kirjoitetaan suoraan tiedostoon heti
        with open(tiedostonimi, "a", encoding="utf-8") as f:
            f.write(page_text + "\n\n---\n\n")
            
        print(f"Sivu kirjoitettu levykkeelle ({len(page_text)} merkkiä)")
    else:
        peräkkäiset_samat += 1
        print(f"Ei uutta tekstiä (yritys {peräkkäiset_samat}/3)")
        if peräkkäiset_samat >= 3:
            print("Kirja näyttää tulleen päätökseensä.")
            break

    # Käännetään sivua
    if aktiivinen_frame:
        driver.switch_to.frame(aktiivinen_frame)
        try:
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ARROW_RIGHT)
        except Exception:
            pass
        driver.switch_to.default_content()
    else:
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ARROW_RIGHT)

    time.sleep(2.0)

driver.quit()
print("Valmista!")
