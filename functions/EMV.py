from datetime import datetime
from robocorp import browser
from playwright.sync_api import Page
from RPA.Excel.Files import Files
from seleniumbase import Driver

def stealth_browser():
    sb = sb_cdp.Chrome()
    endpoint_url = sb.get_endpoint_url()

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(endpoint_url)
        page = browser.page()
        page.goto("https://www.skyscanner.fi/")


def evästeet():
    page = browser.page()
    
    print("Kuitataan evästeet...")
    try:
        page.locator("button:has-text('Hyväksy kaikki')").first.click(timeout=4000, force=True)
    except:
        pass



def lahtopaikka():
    
    browser.configure(browser_engine="chromium", headless=False, slowmo=1000)
    page= browser.page()
    page.goto("https://www.skyscanner.fi/")

    #page.wait_for_timeout(15000)

    evästeet()

    page.click("input[aria-label='Lisää hotelli']")
    page.wait_for_timeout(500)

    print("Asetetaan lähtöpaikka...")
    page.type("input[id='originInput-input']", "Helsinki", delay=200)
    
    page.wait_for_timeout(1000)

    page.type("input[id='destinationInput-input']", "PPariisi", delay=200)
    page.wait_for_timeout(500)

    page.keyboard.press("Enter")
    

    page.wait_for_timeout(1000)


    
def aseta_henkilömäärä():
    page = browser.page()
    #page.goto("https://www.skyscanner.fi/")
    #evästeet()

    page.click("button[data-testid='traveller-button']")
    page.wait_for_timeout(500)

    #page.click("input[id='adult-nudger']")
    #page.wait_for_timeout(500)
    #page.keyboard.press("backspace")
    #page.keyboard.press("4")
    #page.wait_for_timeout(1000)

    page.fill("input[id='adult-nudger']", "4")
    page.wait_for_timeout(10000)
    #page.click("button[data-testid='traveller-selector-apply-button']")
    #page.wait_for_timeout(1000)

    page.click("button[class='BpkButton_bpk-button__MTFkM BpkButton_bpk-button--large__Y2Q3Y BpkButton_bpk-button--featured__MDA2M _DesktopCTA_111t4_325']")
    page.wait_for_timeout(5000)


KUUKAUDET = ["tammikuuta", "helmikuuta", "maaliskuuta", "huhtikuuta", "toukokuuta", "kesäkuuta", "heinäkuuta", "elokuuta", "syyskuuta", "lokakuuta", "marraskuuta", "joulukuuta"]

def muotoile_skyscanner_pvm(suomi_pvm: str) -> str:
    """Muuttaa 15.08.2026 -> '15. elokuuta 2026' (Tämä on Skyscannerin kieli)"""
    pvm_olio = datetime.strptime(suomi_pvm, "%d.%m.%Y")
    paiva = pvm_olio.day
    kuukausi_nimi = KUUKAUDET[pvm_olio.month - 1]
    vuosi = pvm_olio.year
    
    return f"{paiva}. {kuukausi_nimi} {vuosi}"

def etsi_ja_klikkaa_paiva_skyscanner(page: Page, haluttu_pvm: str):
    """Etsii päivää Skyscannerista. Jos ei näy, painaa nuolta."""
    
    skyscanner_muoto = muotoile_skyscanner_pvm(haluttu_pvm)
    print(f"Etsitään päivää: {haluttu_pvm} (Skyscanner-muoto: '{skyscanner_muoto}')...")
    
    # Etsitään painiketta, jonka aria-label SISÄLTÄÄ (*=) kyseisen tekstin
    # (Tämä ohittaa viikonpäivän, esim. "maanantai, 15. elokuuta 2026")
    paiva = page.locator(f"button[aria-label*='{skyscanner_muoto}']")
    
    # Kuvasi HTML-koodin perusteella nuoli eteenpäin:
    # ^= tarkoittaa "alkaa sanoilla"
    seuraava_nuoli = page.locator("button[aria-label^='Seuraava kuukausi']")
    
    for yritys in range(12):
        if paiva.is_visible():
            print(f"--> Päivä {skyscanner_muoto} näkyy ruudulla! Klikataan...")
            paiva.click(force=True) 
            page.wait_for_timeout(1000) # Pieni inhimillinen tauko
            return
            
        else:
            print("--> Päivää ei näy. Painetaan Skyscannerin '>' nuolta eteenpäin...")
            if seuraava_nuoli.is_visible():
                seuraava_nuoli.click(force=True)
                page.wait_for_timeout(1000) # Odotetaan liukuanimaatiota
            else:
                print("-> Eteenpäin-nuolta ei enää löydy! Onko kalenteri auki?")
                break
                
    print(f"VIRHE: Päivää {haluttu_pvm} ei löytynyt 12 yrityksestä huolimatta.")


def testaa_skyscanner_kalenteria():
    # Hidastetaan toimintaa (1000ms viive)
    #browser.configure(browser_engine="chromium", headless=False, slowmo=1000)
    
    page = browser.page()
    #page.goto("https://www.skyscanner.fi/")
    

    print("Avataan kalenteri...")
    try:
        # Klikataan Meno-kenttää jotta kalenteri aukeaa
        page.locator("[data-testid='depart-btn']").click(timeout=3000, force=True)
    except:
        pass
    
    page.wait_for_timeout(1000)

    # Testataan taas elokuun päivillä, jotta robotti joutuu kelaamaan!
    tulo = "15.08.2026"
    lahto = "22.08.2026"
    
    print("--- Aloitetaan menopäivän etsintä ---")
    etsi_ja_klikkaa_paiva_skyscanner(page, tulo)
    
    print("--- Aloitetaan paluupäivän etsintä ---")
    etsi_ja_klikkaa_paiva_skyscanner(page, lahto)
    
    print("Skyscanner-kalenteritesti suoritettu! Odotetaan 5 sekuntia...")
    page.wait_for_timeout(5000)

""""
def skyscanner_sivuII():
    page = browser.page()
    page.goto("https://www.skyscanner.fi/liikennevalineet/lennot/hel/pari/260815/260822/?adultsv2=4&cabinclass=economy&childrenv2=&ref=home&rtn=1&preferdirects=false&outboundaltsenabled=false&inboundaltsenabled=false")

    #page.wait_for_timeout(1000)

    evästeet()
    #page.wait_for_timeout(5000)



    print("Odotetaan hakutuloksia...")
    page.wait_for_selector("div[class*='FlightsTicket_container']", timeout=30000)
        
    # 2. Haetaan kaikki hakutuloskortit
    kortit = page.locator("div[class*='FlightsTicket_container']").all()
        
    keratty_data = []
        
    # 3. Käydään läpi 3 ensimmäistä tulosta (tai vähemmän, jos tuloksia on vähän)
    maara = min(3, len(kortit))
    print(f"Kerätään tiedot {maara} ensimmäisestä tuloksesta...")
        
    for i in range(maara):
        kortti = kortit[i]
            
        # Yritetään hakea hinta ja lentoyhtiö. 
        # HUOM: Skyscannerin selektorit muuttuvat, nämä ovat esimerkkejä:
        try:

            # Etsitään linkki <a> tagista. 
            # Skyscannerin linkit näyttävät alkavan kauttaviivalla (suhteellinen polku),
            # joten liitetään siihen sivuston juuriosoite mukaan!
            suhteellinen_linkki = kortti.locator("a[class*='BookingPanelLink']").first.get_attribute("href")
            varauslinkki = f"https://www.skyscanner.fi{suhteellinen_linkki}"

            #Etsitään span-elementti, joka sisältää sanan "yhteensä"
            hinta_raaka = kortti.locator("span:has-text('yhteensä')").first.inner_text()

            hinta = hinta_raaka.replace(" yhteensä", "").strip()
            # Etsitään span, jonka luokka sisältää sanan 'LogoImage_label'
            yhtio_raaka = kortti.locator("span[class*='LogoImage_label']").first.inner_text()

            yhtio = yhtio_raaka.strip()
                
            keratty_data.append({
                "Sija": i + 1,
                "Lentoyhtiö": yhtio,
                "Hinta": hinta,
                "Varauslinkki": varauslinkki,
                "Hakupäivä": datetime.now().strftime("%d.%m.%Y")
            })
            print(f"Löytyi: {yhtio} - {hinta}")
        except Exception as e:
            print(f"Virhe rivin {i+1} keräämisessä: {e}")

    if keratty_data:
        excel = Files()
        tiedoston_nimi = "skyscanner_tulokset.xlsx"
            
        # Luodaan uusi tyhjä työkirja
        excel.create_workbook(tiedoston_nimi)
            
        # Lisätään meidän sanakirja-lista (keratty_data) suoraan taulukkoon.
        # header=True laittaa automaattisesti otsikot (Lentoyhtiö, Hinta, jne.) ylimmälle riville.
        excel.append_rows_to_worksheet(keratty_data, header=True)
            
        # Tallennetaan tiedosto
        excel.save_workbook()
            
        print(f"Tiedot tallennettu onnistuneesti Robocorpin Excel-työkalulla: {tiedoston_nimi}")
    else:
        print("Tietoja ei saatu kerättyä.")
"""

def skyscanner_sivuII():
    print("Käynnistetään selain UC-tilassa (botineston ohitus)...")
    # Käynnistetään SeleniumBase suoraan häivetilassa!
    driver = Driver(uc=True)

    try:
        # uc_open_with_reconnect on SeleniumBasen oma erikoiskomento, 
        # joka katkaisee yhteyden latauksen ajaksi hämätäkseen tutkaa.
        print("Mennään Skyscanneriin...")
        url = "https://www.skyscanner.fi/liikennevalineet/lennot/hel/pari/260815/260822/?adultsv2=4&cabinclass=economy&childrenv2=&ref=home&rtn=1&preferdirects=false&outboundaltsenabled=false&inboundaltsenabled=false"
        driver.uc_open_with_reconnect(url, reconnect_time=6)

        print("Kuitataan evästeet...")
        try:
            # Pieni tauko varmistaa, että evästeikkuna ehtii animoitua ruudulle
            driver.sleep(1.5) 
            
            # XPath etsii button-elementin, jonka tekstisisällössä on "Hyväksy kaikki".
            # contains(., 'teksti') toimii täsmälleen kuten Playwrightin has-text!
            driver.click("//button[contains(., 'Hyväksy kaikki')]", timeout=4)
            print("Evästeet kuitattu!")
        except:
            print("Evästeikkunaa ei näkynyt, jatketaan eteenpäin...")
            pass

        print("Odotetaan hakutuloksia...")
        # Odotetaan isoa laatikkoa
        driver.wait_for_element_visible("div[class*='FlightsTicket_container']", timeout=30)
            
        # Haetaan kaikki hakutuloskortit listaksi
        kortit = driver.find_elements("css selector", "div[class*='FlightsTicket_container']")
            
        keratty_data = []
            
        maara = min(3, len(kortit))
        print(f"Kerätään tiedot {maara} ensimmäisestä tuloksesta...")
            
        for i in range(maara):
            kortti = kortit[i]
            try:
                # 1. Linkki
                linkki_elem = kortti.find_element("css selector", "a[class*='BookingPanelLink']")
                suhteellinen_linkki = linkki_elem.get_attribute("href")
                varauslinkki = f"https://www.skyscanner.fi{suhteellinen_linkki}"

                # 2. Kokonaishinta (Seleniumissa käytetään XPathia tekstin etsimiseen)
                hinta_elem = kortti.find_element("xpath", ".//span[contains(text(), 'yhteensä')]")
                hinta = hinta_elem.text.replace(" yhteensä", "").strip()

                # 3. Lentoyhtiö
                yhtio_elem = kortti.find_element("css selector", "span[class*='LogoImage_label']")
                yhtio = yhtio_elem.text.strip()


                # 4. UUSI: Kellonajat
                # Etsitään kortin sisältä kaikki elementit, joiden luokka sisältää sanan 'subheading'
                aika_elementit = kortti.find_elements("css selector", "span[class*='subheading']")
                
                # Varmistetaan, että löysimme vähintään 4 kellonaikaa (kuten meno-paluussa pitäisi olla)
                if len(aika_elementit) >= 4:
                    meno_lahto = aika_elementit[0].text.strip()
                    meno_perilla = aika_elementit[1].text.strip()
                    paluu_lahto = aika_elementit[2].text.strip()
                    paluu_perilla = aika_elementit[3].text.strip()
                else:
                    meno_lahto, meno_perilla, paluu_lahto, paluu_perilla = "-", "-", "-", "-"
                    


                keratty_data.append({
                    "Sija": i + 1,
                    "Lentoyhtiö": yhtio,
                    "Meno lähtee": meno_lahto,
                    "Meno perillä": meno_perilla,
                    "Paluu lähtee": paluu_lahto,
                    "Paluu perillä": paluu_perilla,
                    "Kokonaishinta (4 hlö)": hinta,
                    "Varauslinkki": varauslinkki,
                    "Hakupäivä": datetime.now().strftime("%d.%m.%Y")
                })
                print(f"Löytyi: {yhtio} | Meno: {meno_lahto}-{meno_perilla} | Paluu: {paluu_lahto}-{paluu_perilla} | {hinta}")

            except Exception as e:
                print(f"Virhe rivin {i+1} keräämisessä: {e}")

        # Tallennus Exceliin
        if keratty_data:
            excel = Files()
            tiedoston_nimi = "skyscanner_tulokset.xlsx"
            excel.create_workbook(tiedoston_nimi)
            excel.append_rows_to_worksheet(keratty_data, header=True)
            excel.save_workbook()
            print(f"Tiedot tallennettu onnistuneesti: {tiedoston_nimi}")
        else:
            print("Tietoja ei saatu kerättyä.")
            
    finally:
        # Varmistetaan, että selain sulkeutuu aina taustalta, vaikka tulisi virhe
        driver.quit()