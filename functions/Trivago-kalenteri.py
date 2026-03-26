from datetime import datetime
from robocorp.tasks import task
from robocorp import browser
from playwright.sync_api import Page

def muotoile_pvm(suomi_pvm: str) -> str:
    """Muuttaa 15.08.2026 -> 2026-08-15 muotoon, jota kalenteri käyttää."""
    return datetime.strptime(suomi_pvm, "%d.%m.%Y").strftime("%Y-%m-%d")

def etsi_ja_klikkaa_paiva(page: Page, haluttu_pvm: str):
    """
    Tämä on se ydinlogiikka: Etsii päivää. Jos ei näy, painaa nuolta.
    """
    trivago_muoto = muotoile_pvm(haluttu_pvm)
    print(f"Etsitään päivää {haluttu_pvm} (koodina {trivago_muoto})...")
    
    # Määritellään elementit
    paiva = page.locator(f"time[datetime='{trivago_muoto}']")
    seuraava_nuoli = page.locator("button[data-testid='calendar-button-next']")
    
    # Yritetään enintään 12 kertaa (vuosi eteenpäin)
    for yritys in range(12):
        # 1. Tarkistetaan onko päivä näkyvissä kalenterissa
        if paiva.is_visible():
            print(f"--> Päivä {haluttu_pvm} näkyy ruudulla! Klikataan...")
            # force=True varmistaa, että klikkaus menee perille
            paiva.click(force=True) 
            page.wait_for_timeout(1000) # Pieni tauko klikkauksen jälkeen
            return # Lopetetaan funktio, koska päivä löytyi
            
        # 2. Jos päivä ei näy, painetaan nuolta eteenpäin
        else:
            print("--> Päivää ei näy. Painetaan '>' nuolta eteenpäin...")
            seuraava_nuoli.click(force=True)
            # Odotetaan sekunti, jotta kalenterin animaatio ehtii vaihtaa kuukautta
            page.wait_for_timeout(1000)
            
    print(f"VIRHE: Päivää {haluttu_pvm} ei löytynyt 12 yrityksestä huolimatta.")


@task
def testaa_vain_kalenteria():
    # Hidastetaan toimintaa (1000ms viive), jotta ehdit nähdä kalenterin kelauksen
    browser.configure(browser_engine="chromium", headless=False, slowmo=1000)
    page = browser.page()
    page.goto("https://www.trivago.fi/")
    
    # 1. Kuitataan evästeet alta pois (pakotetusti)
    print("Kuitataan evästeet...")
    try:
        page.locator("button:has-text('Hyväksy kaikki')").first.click(timeout=4000, force=True)
    except:
        pass

    # 2. Avataan kalenteri painamalla "Päivämäärät" -nappia
    print("Avataan kalenteri...")
    page.get_by_text("Päivämäärät").click(force=True)
    
    # Odotetaan varmuuden vuoksi hetki, että kalenteri "pomppaa" esiin
    page.wait_for_timeout(1000)

    # 3. Testataan logiikkaa elokuun päivillä!
    tulo = "15.08.2026"
    lahto = "22.08.2026"
    
    print("--- Aloitetaan tulopäivän etsintä ---")
    etsi_ja_klikkaa_paiva(page, tulo)
    
    print("--- Aloitetaan lähtöpäivän etsintä ---")
    etsi_ja_klikkaa_paiva(page, lahto)
    
    print("Kalenteritesti suoritettu! Odotetaan 5 sekuntia...")
    page.wait_for_timeout(5000)

testaa_vain_kalenteria()