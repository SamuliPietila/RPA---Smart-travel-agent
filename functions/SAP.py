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
from robocorp.tasks import task
from robocorp import browser

@task
def testaa_luotettavaa_hakua():
    # Slowmo (1000ms) antaa sinun nähdä mitä tapahtuu
    browser.configure(browser_engine="chromium", headless=False, slowmo=1000)
    page = browser.page()
    
    page.goto("https://www.trivago.fi/")
    
    print("Odotetaan evästeitä...")
    try:
        page.locator("button:has-text('Hyväksy kaikki')").click(timeout=4000)
    except Exception:
        print("Ei evästeikkunaa.")

    # 1. Paina "Kohde" / "Minne matka" (Käytetään lähdekoodin data-testid:tä)
    print("Vaihe 1: Klikataan kohde-kenttää")
    page.locator("[data-testid='auto-complete-wrapper']").click()
    
    # Syötetään kohde heti klikkauksen jälkeen ja painetaan Enter (valitsee ensimmäisen vaihtoehdon)
    # Lähdekoodissa kentän id on "input-auto-complete"
    kohde_kentta = page.locator("#input-auto-complete")
    kohde_kentta.fill("Pariisi")
    page.keyboard.press("Enter")

    # 2. Paina "Päivämäärät" (Käytetään lähdekoodin data-testid:tä)
    print("Vaihe 2: Klikataan 'Päivämäärät'")
    page.locator("[data-testid='search-form-calendar']").click()
    
    # 3. Valitaan päivät (Esimerkkipäivät, jotka sinun pitää muuttaa tulevaisuuteen)
    print("Vaihe 3: Valitaan kalenterista päivät")
    page.locator("time[datetime='2024-06-15']").click() # Tulopäivä (MUUTA TÄMÄ)
    page.locator("time[datetime='2024-06-20']").click() # Lähtöpäivä (MUUTA TÄMÄ)

    # 4. Paina "Asiakkaat ja huoneet"
    print("Vaihe 4: Klikataan 'Asiakkaat ja huoneet'")
    page.locator("[data-testid='search-form-guest-selector']").click()
    
    # 5. Paina "Käytä" nappia (vahvistetaan oletus 2 aik. 1 huone)
    print("Vaihe 5: Painetaan 'Käytä'")
    page.locator("button:has-text('Käytä')").click()
    
    # 6. Paina "Hae" (Käytetään lähdekoodin data-testid:tä)
    print("Vaihe 6: Painetaan 'Hae'")
    page.locator("[data-testid='search-button-with-loader']").click()

    # Odotetaan 10 sekuntia, jotta näet tulossivun
    page.wait_for_timeout(10000)
    
testaa_luotettavaa_hakua()