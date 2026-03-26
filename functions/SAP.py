""""
def starting_questions():
    Departure_location = str(input("Enter the departure city: "))
    target_location = str(input("Enter the target city: "))
    budget = int(input("Enter your budget: "))
    people = int(input("Enter the number of people: "))
    departure_date = str(input("Enter the departure date (DD:MM): "))
    return_date = str(input("Enter the return date (DD:MM): "))
    hotel_rating = float(input("Enter the minimum desired hotel rating (1.0-10.0): "))
    return Departure_location, target_location, budget, people, departure_date, return_date, hotel_rating

starting_questions()
"""
from datetime import datetime
from robocorp.tasks import task
from robocorp import browser

def valitse_paivamaara_kalenterista(page, haluttu_pvm: str):
    """
    Muuntaa suomalaisen päivän (esim. 26.4.2026) Trivagon muotoon (2026-04-26) 
    ja kelaa kalenteria eteenpäin, kunnes päivä löytyy ja klikkaa sitä.
    """
    # 1. Muutetaan päivämäärän muoto
    pvm_olio = datetime.strptime(haluttu_pvm, "%d.%m.%Y")
    trivago_pvm = pvm_olio.strftime("%Y-%m-%d")
    print(f"Etsitään kalenterista päivää: {trivago_pvm}")
    
    # Määritellään elementit, joita etsimme
    paiva_elementti = page.locator(f"time[datetime='{trivago_pvm}']")
    # Etsitään "Seuraava kuukausi" nuoli. Trivago käyttää yleensä tätä testid:tä
    seuraava_kuukausi_nuoli = page.locator("[data-testid='calendar-button-next']")
    
    # 2. Varmistetaan, että kalenteri on ladannut jotain ruudulle
    page.wait_for_selector("time", timeout=5000)
    
    # 3. Silmukka, joka etsii päivää (kokeilee maksimissaan 12 kuukautta eteenpäin)
    for yritys in range(12):
        if paiva_elementti.is_visible():
            paiva_elementti.click()
            print(f"-> Päivä {haluttu_pvm} klikattu onnistuneesti!")
            return # Lopetetaan funktio tähän, koska päivä löytyi
        else:
            print("Päivää ei näy ruudulla, painetaan '>' nuolta...")
            seuraava_kuukausi_nuoli.click()
            # Odotetaan puoli sekuntia, että kalenterin liukuanimaatio ehtii mennä ohi
            page.wait_for_timeout(500)
            
    # Jos silmukka loppuu eikä päivää löytynyt
    raise Exception(f"Päivämäärää {haluttu_pvm} ei löydetty edes selaamalla!")

@task
def trivago_alykas_kalenteri():
    browser.configure(browser_engine="chromium", headless=False, slowmo=1000)
    page = browser.page()
    page.goto("https://www.trivago.fi/")
    
    print("Ohitetaan evästeet...")
    try:
        page.get_by_text("Hyväksy kaikki", exact=False).first.click(timeout=5000)
    except Exception:
        pass

    print("Kirjoitetaan kohde...")
    page.locator("[data-testid='auto-complete-wrapper']").click()
    page.locator("#input-auto-complete").fill("Pariisi")
    page.wait_for_timeout(1500)
    page.keyboard.press("Enter")
    
    # Varmistetaan, että kalenteri on varmasti auki ennen kuin yritämme etsiä päiviä
    try:
        # Jos kalenteri ei auennut automaattisesti, avataan se
        if not page.locator("time").first.is_visible():
            page.locator("[data-testid='search-form-calendar']").click()
    except Exception:
        pass

    # TESTATAAN ÄLYKÄSTÄ KALENTERIA
    # Laitetaan tahallaan pitkälle tulevaisuuteen oleva matka, jotta näet kuinka robotti kelaa kalenteria!
    tulo = "15.08.2026"
    lahto = "22.08.2026"
    
    valitse_paivamaara_kalenterista(page, tulo)
    # Pieni tauko klikkausten välissä matkii ihmistä
    page.wait_for_timeout(500)
    valitse_paivamaara_kalenterista(page, lahto)

    # Odotetaan lopuksi 10s jotta näet tuloksen
    print("Valmista! Odotetaan 10s...")
    page.wait_for_timeout(10000)

trivago_alykas_kalenteri()