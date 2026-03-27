from datetime import datetime
from robocorp import browser
from playwright.sync_api import Page

"""
def starting_questions():
    Departure_location = str(input("Enter the departure city: "))
    target_location = str(input("Enter the target city: "))
    budget = int(input("Enter your budget: "))
    people = int(input("Enter the number of people: "))
    departure_date = str(input("Enter the departure date (DD:MM): "))
    return_date = str(input("Enter the return date (DD:MM): "))
    hotel_rating = float(input("Enter the minimum desired hotel rating (7.0-10.0): "))
    return Departure_location, target_location, budget, people, departure_date, return_date, hotel_rating

starting_questions()
"""
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
            page.wait_for_timeout(500) # Pieni tauko klikkauksen jälkeen
            return # Lopetetaan funktio, koska päivä löytyi
            
        # 2. Jos päivä ei näy, painetaan nuolta eteenpäin
        else:
            print("--> Päivää ei näy. Painetaan '>' nuolta eteenpäin...")
            seuraava_nuoli.click(force=True)
            # Odotetaan sekunti, jotta kalenterin animaatio ehtii vaihtaa kuukautta
            page.wait_for_timeout(500)
            
    print(f"VIRHE: Päivää {haluttu_pvm} ei löytynyt 12 yrityksestä huolimatta.")


def testaa_vain_kalenteria():
    #browser.configure(browser_engine="chromium", headless=False, slowmo=1000)
    page = browser.page()
    #page.goto("https://www.trivago.fi/")
    # Hidastetaan toimintaa (1000ms viive), jotta ehdit nähdä kalenterin kelauksen
    
    # 1. Kuitataan evästeet alta pois (pakotetusti)
    #evästeet()


    # 2. Avataan kalenteri painamalla "Päivämäärät" -nappia
    print("Avataan kalenteri...")
    #page.get_by_text("Päivämäärät").click(force=True)
    
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

def aseta_henkilömäärä():
    page = browser.page()
    print("Asetetaan henkilömäärä...")

    page.type("input[data-testid='adults-amount']", "4", delay=200)
    
    page.click("button[data-testid='guest-selector-apply']")
    
    page.wait_for_timeout(5000)

def matkakohde():
    browser.configure(browser_engine="chromium", headless=False, slowmo=1000)
    page = browser.page()
    page.goto("https://www.trivago.fi/")
    #print("Kuitataan evästeet...")
    evästeet()

    print("Typing destination...")
    search_input = page.locator("input[type='search']")
    search_input.fill("paris")
    # Wait for the dropdown to appear and select the first suggestion
    page.wait_for_timeout(500)
    page.click("span[data-testid='suggestion-title']")

    #page.wait_for_timeout(5000)

def evästeet():
    page = browser.page()
    
    print("Kuitataan evästeet...")
    try:
        page.locator("button:has-text('Hyväksy kaikki')").first.click(timeout=4000, force=True)
    except:
        pass

def filters():
    page = browser.page()
    print("Asetetaan suodattimet...")
    page.goto("https://www.trivago.fi/en-US/srl/hotels-paris-france?search=200-22235;dr-20260522-20260529;drs-40;rc-1-4")
    page.wait_for_timeout(2000)

    print("Painetaan filters kenttä auki")
    page.click("span[class='oTKan8 jrrkOG']")
    page.wait_for_timeout(1000)

    print("Asetetaan property type = hotelli")
    page.click("input[data-testid='property-type-checkbox-312/1-input']")
    page.wait_for_timeout(1000)

    if hotel_rating >= 8.0:
        print("Asetetaan rating suodatin 8.5+")
        page.click("input[data-testid='radio-button-106/1324']")
    elif hotel_rating >= 7.5:
        print("Asetetaan rating suodatin 8.0+")
        page.click("input[data-testid='radio-button-106/1527']")

    elif hotel_rating > 7.0:
        print("Asetetaan rating suodatin 7.5+")
        page.click("input[data-testid='radio-button-106/2007']")

    elif hotel_rating == 7.0:
        print("Asetetaan rating suodatin 7.0+")
        page.click("input[data-testid='radio-button-106/2555']")

    else:
        print("Rating ei määritelty.")
        page.click("input[data-testid='radio-button-null']")

    page.wait_for_timeout(1000)

    print("Klikataan apply filters")
    page.click("button[data-testid='filters-popover-apply-button']")

    page.wait_for_timeout(5000)

    
