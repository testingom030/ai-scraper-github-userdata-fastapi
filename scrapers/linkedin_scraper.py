import asyncio
from playwright.async_api import async_playwright

async def scrape_linkedin(profile_url: str) -> dict:
    """
    Scrapes a LinkedIn profile using a browser automation approach to bypass bot detection.
    
    Args:
        profile_url: The full URL of the LinkedIn profile to scrape.
        
    Returns:
        A dictionary containing the scraped profile data or an error message.
    """
    async with async_playwright() as p:
        try:
            # Launch a headless browser. Headless is faster and uses fewer resources.
            # For debugging, you can set headless=False.
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            # --- Step 1 & 2: Search on Google ---
            print(f"Navigating to Google to search for: {profile_url}")
            await page.goto("https://www.google.com/")
            # Use a realistic user agent
            await page.set_extra_http_headers({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"})
            
            # Type the search query and press Enter
            await page.locator('textarea[name="q"]').fill(f'site:linkedin.com/in/ "{profile_url}"')
            await page.locator('textarea[name="q"]').press("Enter")
            
            # --- Step 3: Find and Click the Correct Link ---
            print("Waiting for search results and finding the correct link...")
            await page.wait_for_load_state('networkidle')
            
            # Find the link that points to the profile_url
            # This locator finds an 'a' tag whose 'href' attribute contains the profile URL.
            profile_link_locator = page.locator(f'a[href*="{profile_url.split("?")[0]}"]')
            
            # Wait for the link to be visible
            await profile_link_locator.first.wait_for(timeout=10000)
            await profile_link_locator.first.click()

            # --- Step 4 & 5: Handle Pop-up and Scrape Data ---
            print("Navigated to LinkedIn profile. Waiting for pop-up...")
            # Wait for the page to settle and the pop-up to likely appear
            await page.wait_for_load_state('domcontentloaded', timeout=20000)
            await asyncio.sleep(3) # Extra wait for dynamic content

            # The pop-up is inside a modal. We find the dismiss button by its aria-label.
            # This is a robust way to find it.
            dismiss_button_selector = 'button[aria-label="Dismiss"]'
            try:
                dismiss_button = page.locator(dismiss_button_selector)
                if await dismiss_button.is_visible(timeout=5000):
                    print("Dismissing the sign-in pop-up...")
                    await dismiss_button.click()
                    await asyncio.sleep(1) # Wait a moment after dismissing
            except Exception:
                print("Pop-up dismiss button not found or not visible. Proceeding anyway.")

            print("Scraping profile data...")
            
            # --- Scrape the data ---
            # Use locators to find elements and get their text content
            name = await page.locator('h1').first.text_content()
            headline = await page.locator('div.text-body-medium.break-words').first.text_content()
            
            # Extract About section
            about_text = ""
            try:
                # This complex selector finds the "About" section's content
                about_locator = page.locator('div.display-flex.ph5.pv3 > div.display-flex.full-width > div > div > span[aria-hidden="true"]').first
                await about_locator.wait_for(timeout=5000)
                about_text = await about_locator.text_content()
            except Exception:
                about_text = "About section not found or is private."

            await browser.close()

            return {
                "name": name.strip() if name else "N/A",
                "headline": headline.strip() if headline else "N/A",
                "about": about_text.strip() if about_text else "N/A",
                "profile_url": profile_url
            }

        except Exception as e:
            print(f"An error occurred during LinkedIn scraping: {e}")
            # Ensure browser is closed on error
            if 'browser' in locals() and not browser.is_closed():
                await browser.close()
            return {"error": f"Failed to scrape LinkedIn profile. It might be private or the page structure has changed. Error: {str(e)}"}

