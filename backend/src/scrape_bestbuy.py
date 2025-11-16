from playwright.sync_api import Playwright, sync_playwright
import time

# issues i encountered while writing this:
# 1). akamai blocking my scraper when i sent requests via the requests python lib
        # soln: use playwright to simulate an actual browser that sends/receives actual JS, can pass TLS handshake/fingerprinting, etc
# 2). DOM pagination/lazy-load only showing a few options out of the hundreds (or more!) that should be present
        # soln: programmatically scroll down in playwright 
            # POP UP ISSUES scroll height being dynamically updated so no way to know i actually reached the bottom of the page
            # lazy loading takes forever to actually load in entries, misleading timeout periods
# 3). DOM analysis/traversal (figuring out how to navigate the DOM to get the stuff I need)
        # soln: a lot of 'inspect source'ing

def scrape_bestbuy_gpus():
    url = "https://www.bestbuy.com/site/searchpage.jsp?id=pcat17071&st=gpu"

    with sync_playwright() as p:
        gpus = []
        seen = set()

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url, timeout=30000)
        page.wait_for_selector(".sku-block-content") # dont do anything until the site fully loads


        # deal with lazy loading by scrolling until no more listings
        
         # ---------------- REAL WORKING SCROLL LOOP ----------------
        last_height = page.evaluate("document.body.scrollHeight")

        while True:
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(2000)  # give lazy-loading time to insert elements

            new_height = page.evaluate("document.body.scrollHeight")
            if new_height == last_height:
                break

            last_height = new_height
        # -----------------------------------------------------------

        # take a final snapshot of the DOM 
        items = page.query_selector_all(".sku-block-content")

        # now that we have all available listings, we can begin scraping
        for item in items:
            title = item.query_selector(".product-title")
            price = item.query_selector("[data-testid='price-block-customer-price'] span")
            link = item.query_selector(".product-list-item-link")

            link_text = link.get_attribute("href")

            if link_text not in seen:
                seen.add(link_text)
                gpus.append({
                    "name": title.inner_text().strip() if title else None,
                    "price": price.inner_text().strip() if price else None,
                    "link": link.get_attribute("href") if link else None
                })


        # print out listings
        for pairs in gpus:
            for k, v in pairs.items():
                if k == "name":
                    print("gpu-view> GPU found! : {}".format(v))
                if k == "price":
                    print("\t for {}".format(v))
                if k == "link":
                    print("\t @ {}".format(v))

        print(f"\ngpu-view> Summary -- captured {len(gpus)} GPU listings. Happy hunting!")

        browser.close()

        return gpus
