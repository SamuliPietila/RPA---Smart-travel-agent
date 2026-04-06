

#tää pitäs toimii henkilömäärä kohtaan

#page.type perusfunktio. "input" elementtikenttä html:stä. 
# data-tesid attribuutti joka täsmentää elementin. , "4" kirjoitettava arvo. delay viive.

# page.type("input[data-testid='adults-amount']", "4", delay=200)

from datetime import datetime
from robocorp.tasks import task
from robocorp import browser



def ohita_evästeet():
    browser.configure(browser_engine="chromium", headless=False, slowmo=1000)
    page = browser.page()
    page.goto("https://www.trivago.fi/")
    print("Ohitetaan evästeet...")
    try:
        page.get_by_text("Hyväksy kaikki", exact=False).first.click(timeout=5000)
    except Exception:
        pass

def aseta_henkilömäärä():
    print("Asetetaan henkilömäärä...")

    page.type("input[data-testid='adults-amount']", "4", delay=200)

