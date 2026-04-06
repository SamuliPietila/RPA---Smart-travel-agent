from datetime import datetime
from robocorp import browser
from playwright.sync_api import Page
from RPA.Excel.Files import Files
from functions import EMV

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

    budget = 2000
    hotel_rating = 8.0

    page = browser.page()
    print("Asetetaan suodattimet...")
    #page.goto("https://www.trivago.fi/en-US/srl/hotels-paris-france?search=200-22235;dr-20260522-20260529;drs-40;rc-1-4")
    #evästeet()
    
    page.wait_for_timeout(2000)

    print("Painetaan filters kenttä auki")
    page.click("button[name='more_filters']")
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

    print("Järjestetään hinnan mukaan")
    page.click("button[name='sorting_selector']")
    page.wait_for_timeout(500)

    page.click("input[data-testid='sorting-index-4']")
    page.click("button[data-testid='filters-popover-apply-button']")
    page.wait_for_timeout(5000)

    print("Klikataan budjetti suodatin")
    page.click("button[name='budget']")
    page.wait_for_timeout(500)

    print("Valitaan haluttu budjetti")
    page.click("input[data-testid='radio-button-TOTAL_STAY']")

    page.type("input[data-testid='price-filter-value-max']", str(budget), delay=200)

    page.click("button[data-testid='filters-popover-apply-button']")
    page.wait_for_timeout(5000)



def tallenna_hotellit_olemassaolevaan_exceliin(keratty_hotellidata):
    if not keratty_hotellidata:
        print("Ei hotellidataa tallennettavaksi.")
        return
        
    excel = Files()
    tiedoston_nimi = "skyscanner_tulokset.xlsx"
    
    try:
        # Avataan se VANHA tiedosto, jonka Skyscanner-koodi loi
        excel.open_workbook(tiedoston_nimi)
        
        # TARKISTUS: Onko "Hotellit" jo olemassa vanhasta testistä?
        if excel.worksheet_exists("Hotellit"):
            print("Vanha Hotellit-välilehti löytyi. Poistetaan vanhat tiedot...")
            excel.remove_worksheet("Hotellit")
        
        # Luodaan uusi, puhdas välilehti (nyt se onnistuu aina)
        excel.create_worksheet("Hotellit")
        
        # Varmistetaan, että ollaan varmasti uudella välilehdellä
        excel.set_active_worksheet("Hotellit")
        
        # Lisätään hotellidata uuteen välilehteen
        excel.append_rows_to_worksheet(keratty_hotellidata, header=True)
        
        # Tallennetaan muutokset
        excel.save_workbook()
        print(f"Hotellit päivitetty onnistuneesti tiedostoon {tiedoston_nimi}!")
        
    except Exception as e:
        print(f"Virhe Excelin tallennuksessa: {e}")  

    
def hae_trivago_hotellit():
    print("Odotetaan Trivagon tuloksien latautumista...")
    page = browser.page()
    
    # Trivagossa hakutuloskortit ovat usein tällä testid:llä tai <article>-tageja.
    # Muokkaa tätä tarvittaessa DevToolsin perusteella!
    page.wait_for_selector("[data-testid='accommodation-list-element']", timeout=15000)
    kortit = page.locator("[data-testid='accommodation-list-element']").all()
    
    keratty_hotellidata = []
    maara = min(3, len(kortit))
    
    print(f"Kerätään tiedot {maara} ensimmäisestä hotellista...")
    
    for i in range(maara):
        kortti = kortit[i]
        try:
            # 1. Hotellin nimi
            # Trivagossa on usein selkeä testid nimelle
            nimi = kortti.locator("span[itemprop='name']").inner_text().strip()
            
            # 2. Hinta (päivitetty testid!)
            hinta_raaka = kortti.locator("[data-testid='recommended-price']").first.inner_text()
            
            # Siivotaan euro-merkki, tavalliset välilyönnit sekä nuo piilotetut &nbsp; (\xa0) merkit
            hinta = hinta_raaka.replace("€", "").replace("\xa0", "").replace(" ", "").strip()
            
            # 3. Arvostelu (Käytetään span-tagia ja itemprop-attribuuttia)
            try:
                arvostelu = kortti.locator("span[itemprop='ratingValue']").first.inner_text().strip()
            except:
                arvostelu = "Ei arvosanaa"
            
            # 4. UUSI VARAUSLINKKIKOODI (Klikkaa ja Nappaa)
            try:
                nappi = kortti.locator("[data-testid='champion-deal']").first
                    
                # Otetaan talteen pääsivun alkuperäinen osoite vertailua varten
                alkuperainen_url = page.url
                    
                try:
                    # Yritetään napata uusi välilehti (popup)
                    with page.expect_popup(timeout=8000) as popup_info:
                        nappi.click(force=True)
                        
                    uusi_sivu = popup_info.value
                        
                    # Odotetaan hetki, jotta Trivagon seurantakoodi ehtii muuttua oikeaksi osoitteeksi
                    uusi_sivu.wait_for_load_state("domcontentloaded", timeout=5000)
                    varauslinkki = uusi_sivu.url
                        
                    # SUOJAUS: Varmistetaan ehdottomasti, ettemme sulje pääsivua!
                    if uusi_sivu != page:
                        uusi_sivu.close()
                            
                except Exception as e:
                    # JOS popupia ei tullut (esim. TimeoutError), tarkistetaan vaihtuiko pääsivun osoite!
                    if page.url != alkuperainen_url:
                        # Trivago ohjasi meidät samassa ikkunassa eteenpäin!
                        varauslinkki = page.url
                        print("Sivu navigoi samassa ikkunassa. Pakitetaan takaisin...")
                        page.go_back(wait_until="domcontentloaded")
                    else:
                        print("Nappi ei tehnyt mitään tai lataus kesti liian kauan.")
                        varauslinkki = "Ei saatavilla"
                            
            except Exception as e:
                print(f"Koko linkin haku kaatui: {e}")
                varauslinkki = "Ei saatavilla"
            
            keratty_hotellidata.append({
                "Sija": i + 1,
                "Hotelli": nimi,
                "Hinta": hinta,
                "Arvostelu": arvostelu,
                "Linkki": varauslinkki,
                "Hakupäivä": datetime.now().strftime("%d.%m.%Y")
            })
            print(f"Löytyi: {nimi} - {hinta} € (Arvosana: {arvostelu})")
            
        except Exception as e:
            print(f"Virhe hotellin {i+1} keräämisessä: {e}")

    # Tallennetaan olemassa olevaan Exceliin!
    tallenna_hotellit_olemassaolevaan_exceliin(keratty_hotellidata)