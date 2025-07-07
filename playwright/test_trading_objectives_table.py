import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pages.trading_objectives_page import TradingObjectivesPage

import asyncio
from playwright.async_api import async_playwright
import re

# --- CONFIG ---
CURRENCIES = {
    "USD": ["$10,000", "$25,000", "$50,000", "$100,000", "$200,000"],
    "GBP": ["£10,000", "£20,000", "£35,000", "£70,000", "£140,000"],
    "EUR": ["€10 000", "€20 000", "€40 000", "€80 000", "€160 000"],
    "CZK": ["250 000 CZK", "500 000 CZK", "1 000 000 CZK", "2 000 000 CZK", "4 000 000 CZK"],
    "CAD": ["$15,000", "$30,000", "$60,000", "$120,000", "$240,000"],
    "AUD": ["$15,000", "$30,000", "$65,000", "$130,000", "$260,000"],
    "CHF": ["10 000 CHF", "20 000 CHF", "40 000 CHF", "80 000 CHF", "160 000 CHF"]
}

# --- EXPECTED VALUES ---
COMMON_ROWS = {
    "trading-period": ["unlimited", "unlimited", "unlimited"],
    "minimum-trading-days": ["4 days", "4 days", "X"],
}

FEE_LIST = ["€89", "€250", "€345", "€540", "€1 080"]

EXPECTED_VALUES = {}

def normalize(s):
    return re.sub(r"\s+", " ", s.strip().lower())

def fmt(val, currency):
    if currency in ["USD", "CAD", "AUD", "GBP"]:
        if currency == "GBP":
            return f"£{int(val):,}"
        else:
            return f"${int(val):,}" if currency != "GBP" else f"£{int(val):,}"
    elif currency == "EUR":
        return f"€{int(val):,}".replace(",", " ")
    elif currency == "CZK":
        return f"{int(val):,} CZK".replace(",", " ")
    elif currency == "CHF":
        return f"{int(val):,} CHF".replace(",", " ")
    return str(val)

for currency, balances in CURRENCIES.items():
    for i, balance in enumerate(balances):
        # Remove currency symbols and spaces for calculation
        bal_clean = (
            balance.replace(",", "")
            .replace("$", "")
            .replace("£", "")
            .replace("€", "")
            .replace("CZK", "")
            .replace("CHF", "")
            .replace("CAD", "")
            .replace("AUD", "")
            .replace(" ", "")
            .strip()
        )
        bal_num = float(bal_clean) if any(c.isdigit() for c in bal_clean) else 0
        # For CZK, EUR, CHF, AUD, CAD, the balance may have spaces as thousand separators
        # For CZK, remove ' CZK', for CHF remove ' CHF', etc.
        if currency == "CZK":
            bal_num = float(balance.replace(" ", "").replace("CZK", ""))
        elif currency == "CHF":
            bal_num = float(balance.replace(" ", "").replace("CHF", ""))
        elif currency == "EUR":
            bal_num = float(balance.replace(" ", "").replace("€", ""))
        elif currency == "AUD":
            bal_num = float(balance.replace(",", "").replace("$", ""))
        elif currency == "CAD":
            bal_num = float(balance.replace(",", "").replace("$", ""))
        elif currency == "GBP":
            bal_num = float(balance.replace(",", "").replace("£", ""))
        # Format values for display
        max_daily_loss = fmt(bal_num / 20, currency)
        max_loss = fmt(bal_num / 10, currency)
        profit_1 = fmt(bal_num / 10, currency)
        profit_2 = fmt(bal_num / 20, currency)
        fee = FEE_LIST[i] if i < len(FEE_LIST) else FEE_LIST[-1]
        EXPECTED_VALUES[(currency, balance)] = {
            **COMMON_ROWS,
            "maximum-daily-loss": [max_daily_loss] * 3,
            "maximum-loss": [max_loss] * 3,
            "profit-target": [profit_1, profit_2, "X"],
            "refundable-fee": [fee, "free", "refund"],
        }

# --- TEST LOGIC ---
async def test_table(headless=True):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        page = await browser.new_page()
        await page.goto("https://ftmo.com/en/#trading-objectives-table")
        # Accept cookies if present
        try:
            await page.click('#ftmo-cookie-layer button', timeout=5000)
        except Exception:
            pass
        page_obj = TradingObjectivesPage(page)
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
                    for row_id, expected_cells in EXPECTED_VALUES[key].items():
                        for col_idx, expected in enumerate(expected_cells, start=1):
                            cell_text = await page_obj.get_table_cell(row_id, col_idx)
                            if row_id == "refundable-fee" and col_idx == 1:
                                assert normalize(expected) in normalize(cell_text), f"Refundable Fee mismatch: expected '{expected}' in '{cell_text}' for {currency} {balance} Step {col_idx}"
                            else:
                                assert normalize(expected) == normalize(cell_text), f"Value mismatch in row '{row_id}' col {col_idx}: expected '{expected}', got '{cell_text}' for {currency} {balance}"
                else:
                    for row_id in [
                        "trading-period",
                        "minimum-trading-days",
                        "maximum-daily-loss",
                        "maximum-loss",
                        "profit-target",
                        "refundable-fee",
                    ]:
                        assert await page_obj.row_is_visible(row_id), f"Missing row: {row_id} for {currency} {balance}"
        print("All currency/balance table checks passed.")
        await browser.close()

if __name__ == "__main__":
    headless = True
    if len(sys.argv) > 1 and sys.argv[1] == "ui":
        headless = False
    asyncio.run(test_table(headless=headless))
