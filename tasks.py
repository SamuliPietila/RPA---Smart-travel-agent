from datetime import datetime
from robocorp.tasks import task
from robocorp import browser
from playwright.sync_api import Page

def muotoile_pvm(suomi_pvm: str) -> str:
    """Muuttaa esim. 26.4.2026 -> 2026-04-26 robotille sopivaksi."""
    return datetime.strptime(suomi_pvm, "%d.%m.%Y").strftime("%Y-%m-%d")

def etsi_ja_klikkaa_paiva(page: Page, kohde_pvm: str):
    """Kelaa kalenteria nuolella, kunnes oikea päivä löytyy ja klikkaa."""
    trivago_pvm = muotoile_pvm(kohde_pvm)
    print(f"Etsitään kalenterista päivää: {kohde_pvm}")
    
    paiva_elementti = page.locator(f"time[datetime='{trivago_pvm}']")
    seuraava_nuoli = page.locator("button[data-testid='calendar-button-next']")
    
    for _ in range(12):
        if paiva_elementti.is_visible():
            paiva_elementti.click(force=True)
            print(f"-> Päivä {kohde_pvm} klikattu!")
            page.wait_for_timeout(500)
            return
        
        if seuraava_nuoli.is_visible():
            seuraava_nuoli.click(force=True)
            page.wait_for_timeout(800)
        else:
            break
    print(f"-> VIRHE: Päivämäärää {kohde_pvm} ei löytynyt!")

def aseta_henkilomaara_aktivoimalla(page: Page, aikuiset: int):
    """Tuplaklikkaa aikuisten tekstikentän aktiiviseksi ja kirjoittaa uuden luvun."""
    print(f"Asetetaan henkilömääräksi {aikuiset} aikuista...")
    try:
        page.locator("[data-testid='search-form-guest-selector']").click(force=True)
        page.wait_for_timeout(1000)
    except Exception:
        pass # Valikko saattoi olla jo auki

    try:
        aikuiset_rivi = page.locator("div").filter(has_text="Aikuiset").last
        input_kentta = aikuiset_rivi.locator("input")
        
        print("-> Tuplaklikataan kenttä aktiiviseksi...")
        input_kentta.click(click_count=2, force=True)
        page.wait_for_timeout(500)
        
        print(f"-> Näppäillään luku {aikuiset}...")
        page.keyboard.type(str(aikuiset), delay=200)
        page.wait_for_timeout(500)
        
    except Exception as e:
        print(f"-> Kentän aktivointi epäonnistui: {e}")

    print("-> Vahvistetaan painamalla 'Käytä'...")
    page.get_by_role("button", name="Käytä").first.click(force=True)


@task
def trivago_taydellinen_matkatoimisto():
    """Tästä robotti lähtee käyntiin!"""
    browser.configure(browser_engine="chromium", headless=False, slowmo=500)
    page = browser.page()
    page.goto("https://www.trivago.fi/")
    
    # 1. EVÄSTEET
    print("Vaihe 1: Evästeet")
    try:
        page.locator("button:has-text('Hyväksy kaikki')").first.click(timeout=4000, force=True)
        page.wait_for_timeout(1000)
    except Exception:
        pass

    # 2. KOHDE
    print("Vaihe 2: Matkakohde")
    try:
        page.locator("[data-testid='auto-complete-wrapper']").click(force=True)
        kohde_input = page.locator("#input-auto-complete")
        kohde_input.wait_for(state="visible", timeout=3000)
        
        # Kirjoitetaan viiveellä ja valitaan listasta
        page.keyboard.type("Pariisi", delay=150)
        ehdotus = page.locator("[data-testid='search-suggestion']").first
        ehdotus.wait_for(state="visible", timeout=5000)
        ehdotus.click(force=True)
        print("-> Kohde valittu.")
    except Exception as e:
        print(f"-> Kohteen valinta epäonnistui: {e}")

    # 3. PÄIVÄMÄÄRÄT
    print("Vaihe 3: Kalenteri")
    try:
        if not page.locator("time").first.is_visible(timeout=2000):
            page.locator("[data-testid='search-form-calendar']").click(force=True)
    except Exception:
        pass

    etsi_ja_klikkaa_paiva(page, "26.4.2026")
    etsi_ja_klikkaa_paiva(page, "30.4.2026")

    # 4. HENKILÖMÄÄRÄ
    print("Vaihe 4: Henkilömäärä")
    page.type("input[data-testid='adults-amount']", "4", delay=200)

    # 5. HAE
    print("Vaihe 5: Hae")
    try:
        page.locator("[data-testid='search-button-with-loader']").click(force=True)
    except Exception:
        page.locator("button:has-text('Hae')").first.click(force=True)
        
    print("Kaikki valmista! Odotetaan 10s...")
    page.wait_for_timeout(10000)

trivago_taydellinen_matkatoimisto()