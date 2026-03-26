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
from playwright.sync_api import Page

def accept_cookies(page: Page):
    """Yrittää ohittaa evästeet usealla eri tunnistustavalla."""
    print("Yritetään hyväksyä evästeet...")
    try:
        # Etsitään evästenappia tekstin perusteella (huomioi sekä suomi että englanti)
        cookie_btn = page.locator("button:has-text('Hyväksy kaikki'), button:has-text('Accept all')").first
        if cookie_btn.is_visible(timeout=5000):
            cookie_btn.click()
            print("Evästeet hyväksytty.")
    except Exception as e:
        print("Evästeikkunaa ei löytynyt tai se katosi. Jatketaan...")

def search_trivago_flow(destination: str, check_in: str, check_out: str, max_price: str):
    # Avataan selain hitaammalla tahdilla (slowmo), jotta se matkii ihmistä
    browser.configure(browser_engine="chromium", headless=False, slowmo=100)
    page = browser.page()
    
    # 1. Avaa sivu
    page.goto("https://www.trivago.fi/") # Käytetään .fi jos halutaan suomeksi
    page.wait_for_load_state("networkidle")
    accept_cookies(page)
    
    # 2 & 3. Kirjoita kohde ja valitse alasvetovalikosta
    print(f"Etsitään kohdetta: {destination}")
    search_input = page.locator("input[type='search']")
    search_input.click()
    search_input.fill(destination)
    # Odotetaan alasvetovalikon ilmestymistä ja valitaan ensimmäinen
    page.locator("[data-testid='search-suggestion']").first.click()
    
    # 4. Aseta tulo- ja lähtöpäivä kalenterista
    print(f"Valitaan päivät: {check_in} - {check_out}")
    # Trivagossa kohteen valinta avaa yleensä kalenterin automaattisesti.
    # Valitaan suoraan datetime-attribuutin avulla.
    page.locator(f"time[datetime='{check_in}']").click()
    page.locator(f"time[datetime='{check_out}']").click()
    
    # 5. Aseta henkilömäärä ja huoneet
    print("Vahvistetaan henkilömäärä...")
    # Kun päivät on valittu, aukeaa yleensä "Vieraat ja huoneet" -valikko.
    # Painetaan "Käytä" (Apply) nappia vahvistaaksemme oletuksen (2 aikuista, 1 huone).
    apply_guests_btn = page.locator("button:has-text('Käytä'), button:has-text('Apply')").first
    if apply_guests_btn.is_visible():
        apply_guests_btn.click()
    
    # 6. Paina "Hae"
    print("Aloitetaan haku...")
    search_btn = page.locator("button:has-text('Hae'), button:has-text('Search')").first
    search_btn.click()
    
    # Odotetaan, että hakutulossivu latautuu
    page.wait_for_selector("[data-testid='accommodation-list']", timeout=15000)
    
    # --- SUODATTIMET ---
    print("Asetetaan suodattimet...")
    
    # 7 & 8. Arvostelu
    page.locator("button:has-text('Arvostelu'), button:has-text('Guest rating')").click()
    page.locator("label:has-text('Erittäin hyvä'), label:has-text('8.0')").first.click()
    
    # 9. Majoituspaikantyyppi: Hotellit
    page.locator("button:has-text('Majoituspaikan tyyppi'), button:has-text('Property type')").click()
    page.locator("label:has-text('Hotelli'), label:has-text('Hotel')").first.click()
    
    # 11. Lajittelu: Hinta (matalimmasta korkeimpaan)
    page.locator("button:has-text('Lajitteluperuste'), button:has-text('Sort by')").click()
    page.locator("label:has-text('Hinta ja suositukset'), label:has-text('Price only')").click() # Huom! Trivagon tekstit vaihtelevat
    
    # 12, 13, 14. Hinta (Koko majoitus ja Maksimihinta)
    print(f"Asetetaan maksimihinta: {max_price}")
    page.locator("button:has-text('Hinta'), button:has-text('Price')").click()
    # Hinnan syöttäminen voi olla liukusäädin (slider) tai tekstikenttä. 
    # Jos se on tekstikenttä, tämä toimii:
    max_price_input = page.locator("input[data-testid='price-filter-max-input']")
    if max_price_input.is_visible():
        max_price_input.fill(max_price)
    # Vahvistetaan hinta
    page.locator("button:has-text('Käytä'), button:has-text('Apply')").first.click()
    
    # 15. Kerää majoitustiedot (Odota ensin että lista päivittyy)
    page.wait_for_timeout(3000) # Lyhyt tauko, jotta sivu ehtii ladata filtteröidyt tulokset
    print("Ollaan valmiita keräämään dataa!")
    
    # Pidetään selain auki testausta varten
    page.wait_for_timeout(10000)

@task
def run_trivago_robot():
    """Tätä funktiota kutsutaan kun robotti käynnistetään."""
    kohde = "Pariisi"
    # HUOM: Varmista että päivämäärät ovat tulevaisuudessa ja oikeassa formaatissa (YYYY-MM-DD)
    tulo = "2024-06-10" 
    lahto = "2024-06-15"
    maksimibudjetti = "1000"
    
    search_trivago_flow(kohde, tulo, lahto, maksimibudjetti)