class TradingObjectivesPage:
    def __init__(self, page):
        self.page = page

    async def select_currency(self, currency):
        currency_divs = self.page.locator('div._btn_u4t34_18')
        count = await currency_divs.count()
        for i in range(count):
            div = currency_divs.nth(i)
            div_text = (await div.inner_text()).strip().lower()
            if div_text == currency.lower():
                await div.click()
                return True
        return False

    async def select_balance(self, balance):
        locator = self.page.get_by_role("button", name=balance)
        await locator.wait_for(state="visible", timeout=5000)
        await locator.click()

    async def get_table_cell(self, row_id, col_idx):
        row = self.page.locator(f'div[id="{row_id}"]')
        cell = row.locator(f'div._column_9hsjp_41:nth-child({col_idx+1}) div._cell_9hsjp_44:last-child')
        return (await cell.inner_text()).strip().lower()

    async def row_is_visible(self, row_id):
        row = self.page.locator(f'div[id="{row_id}"]')
        return await row.is_visible()
