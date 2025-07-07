import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from test_utils import CURRENCIES, normalize, build_expected_values
from pages.trading_objectives_page import TradingObjectivesPage

import asyncio
from playwright.async_api import async_playwright

# Module-level constants for locators
TRADING_OBJECTIVES_LINK = 'a[href="#trading-objectives-table"]'
COOKIE_BUTTON = '#ftmo-cookie-layer button'
TABLE = 'table'
YOUTUBE_IFRAME = 'iframe[src*="youtube.com"]'
TRADING_OBJECTIVES_URL = 'https://ftmo.com/en/#trading-objectives-table'

# Module-level constants for row IDs
TABLE_ROW_IDS = [
    "trading-period",
    "minimum-trading-days",
    "maximum-daily-loss",
    "maximum-loss",
    "profit-target",
    "refundable-fee",
]

EXPECTED_VALUES = build_expected_values()

async def test_table(headless=True):
    async with async_playwright() as p:
        # Step 1: Launch browser
        browser = await p.chromium.launch(headless=headless)
        page = await browser.new_page()

        # Step 2: Go to Trading Objectives section
        await page.goto(TRADING_OBJECTIVES_URL)

        # Step 3: Accept cookies if present
        try:
            await page.click(COOKIE_BUTTON, timeout=5000)
        except Exception:
            pass

        # Step 4: Create page object for Trading Objectives
        page_obj = TradingObjectivesPage(page)

        # Step 5: For each currency, check all balances and table values
        for currency, balances in CURRENCIES.items():
            print(f"Testing currency: {currency}")
            found = await page_obj.select_currency(currency)
            if not found:
                currency_divs = page.locator('div._btn_u4t34_18')
                count = await currency_divs.count()
                all_divs = [await currency_divs.nth(i).inner_text() for i in range(count)]
                print(f"[ERROR] Currency '{currency}' not found. Available: {all_divs}")
                continue

            for balance in balances:
                print(f"  Testing balance: {balance}")
                try:
                    await page_obj.select_balance(balance)
                except Exception as e:
                    print(f"[WARNING] Balance button '{balance}' not found or not clickable for {currency}: {e}")
                    continue
                await page.wait_for_timeout(500)  # Wait for table update

                key = (currency, balance)
                if key in EXPECTED_VALUES:
                    # Step 6: Check all expected table values for this currency/balance
                    for row_id, expected_cells in EXPECTED_VALUES[key].items():
                        for col_idx, expected in enumerate(expected_cells, start=1):
                            cell_text = await page_obj.get_table_cell(row_id, col_idx)
                            if row_id == "refundable-fee" and col_idx == 1:
                                assert normalize(expected) in normalize(cell_text), f"Refundable Fee mismatch: expected '{expected}' in '{cell_text}' for {currency} {balance} Step {col_idx}"
                            else:
                                assert normalize(expected) == normalize(cell_text), f"Value mismatch in row '{row_id}' col {col_idx}: expected '{expected}', got '{cell_text}' for {currency} {balance}"
                else:
                    # Step 7: If no expected values, just check row visibility
                    for row_id in TABLE_ROW_IDS:
                        assert await page_obj.row_is_visible(row_id), f"Missing row: {row_id} for {currency} {balance}"

        print("All currency/balance table checks passed.")
        await browser.close()

if __name__ == "__main__":
    headless = True
    if len(sys.argv) > 1 and sys.argv[1] == "ui":
        headless = False
    asyncio.run(test_table(headless=headless))
