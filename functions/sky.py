from datetime import datetime
from robocorp import browser
from playwright.sync_api import Page

# Suomalaisten kuukausien nimet, joita Skyscanner käyttää
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
    browser.configure(browser_engine="chromium", headless=False, slowmo=1000)
    
    page = browser.page()
    page.goto("https://www.skyscanner.fi/")
    
    print("Kuitataan evästeet...")
    
    print("Kuitataan evästeet...")
    try:
        page.locator("button:has-text('Hyväksy kaikki')").first.click(timeout=4000, force=True)
    except:
        pass

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