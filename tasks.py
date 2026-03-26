from robocorp.tasks import task
from robocorp import browser

def accept_cookies(page):
    """Handles the cookie pop-up if it appears."""
    try:
        # Wait for max 3 seconds for the cookie banner
        cookie_button = page.locator("button:has-text('Accept'), [data-testid='cookie-consent-accept']")
        if cookie_button.is_visible(timeout=3000):
            cookie_button.click()
            print("Cookies accepted.")
    except Exception:
        print("No cookie banner found or already accepted.")

def search_trivago_hotels(destination: str, check_in_date: str, check_out_date: str):
    """Navigates Trivago to find hotels matching the criteria."""
    
    # Configure browser (Headless=False is crucial for debugging selectors)
    browser.configure(
        browser_engine="chromium",
        headless=False,
        slowmo=50, # Slows down actions slightly to mimic human behavior
    )
    
    page = browser.page()
    print(f"Opening Trivago for {destination}...")
    page.goto("https://www.trivago.com/")
    
    # 1. Handle Cookies
    accept_cookies(page)
    
    # 2. Enter Destination
    print("Typing destination...")
    search_input = page.locator("input[type='search']")
    search_input.fill(destination)
    # Wait for the dropdown to appear and select the first suggestion
    page.locator("[data-testid='search-suggestion']").first.click()
    
    # 3. Select Dates (This requires interacting with the calendar widget)
    # Note: Complex calendar widgets often require precise clicking based on dates
    print(f"Selecting dates: {check_in_date} to {check_out_date}...")
    # Example logic: click the specific date buttons
    page.locator(f"time[datetime='{check_in_date}']").click()
    page.locator(f"time[datetime='{check_out_date}']").click()
    
    # 4. Initiate Search
    page.locator("button:has-text('Search')").click()
    
    # Wait for results to load
    page.wait_for_selector("[data-testid='accommodation-list']", timeout=10000)
    
    # 5. Apply Filters (Rating 8.0+ and Free Cancellation)
    print("Applying filters...")
    # Click "Guest rating" filter
    page.locator("button:has-text('Guest rating')").click()
    page.locator("label:has-text('8.0')").click() 
    
    # Click "More filters" or "Free cancellation" directly if available
    # page.locator("label:has-text('Free cancellation')").click()
    
    print("Filters applied. Ready for data extraction.")
    
    # Keep browser open for 10 seconds to verify visually during testing
    page.wait_for_timeout(10000)

@task
def run_travel_agent_step_3():
    """Main task entry point for testing."""
    # Hardcoded test variables (These will later come from your Step 1 Excel reader)
    target_destination = "Paris"
    target_check_in = "2024-05-15" # Format depends on how Trivago's DOM stores dates
    target_check_out = "2024-05-20"
    
    search_trivago_hotels(target_destination, target_check_in, target_check_out)