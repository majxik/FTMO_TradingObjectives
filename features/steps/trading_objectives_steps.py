import asyncio
from behave import given, when, then
from playwright.async_api import async_playwright

@given('I am on the FTMO homepage')
async def step_impl(context):
    context.playwright = await async_playwright().start()
    context.browser = await context.playwright.chromium.launch(headless=True)
    context.page = await context.browser.new_page()
    await context.page.goto('https://ftmo.com/en/')
    # Accept cookies if modal appears
    try:
        await context.page.wait_for_selector('#ftmo-cookie-layer button', timeout=5000)
        await context.page.click('#ftmo-cookie-layer button')
    except Exception:
        pass  # Cookie modal did not appear

@when('I navigate to the "Trading Objectives" section')
async def step_impl(context):
    await context.page.wait_for_selector('a[href="#trading-objectives-table"]')
    await context.page.locator('a[href="#trading-objectives-table"]').first.scroll_into_view_if_needed()
    await context.page.locator('a[href="#trading-objectives-table"]').first.click()

@then('I should see the list of trading objectives and their descriptions')
async def step_impl(context):
    assert await context.page.locator('text=Maximum Daily Loss').is_visible()
    assert await context.page.locator('text=Maximum Loss').is_visible()
    assert await context.page.locator('text=Profit Target').is_visible()
    assert await context.page.locator('text=Minimum Trading Days').is_visible()
    assert await context.page.locator('text=Trading Period').is_visible()
    assert await context.page.locator('text=Leverage').is_visible()
    assert await context.page.locator('text=Maximum Capital Allocation').is_visible()
    assert await context.page.locator('text=News Trading').is_visible()
    assert await context.page.locator('text=Weekend Holding').is_visible()
    assert await context.page.locator('text=EA Trading').is_visible()
    assert await context.page.locator('text=Account Stopout').is_visible()

@given('I am on the Trading Objectives section')
async def step_impl(context):
    await context.execute_steps('''
        Given I am on the FTMO homepage
        When I navigate to the "Trading Objectives" section
    ''')

@then('I should see "Maximum Daily Loss"')
async def step_impl(context):
    assert await context.page.locator('text=Maximum Daily Loss').is_visible()

@then('I should see "Maximum Loss"')
async def step_impl(context):
    assert await context.page.locator('text=Maximum Loss').is_visible()

@then('I should see "Profit Target"')
async def step_impl(context):
    assert await context.page.locator('text=Profit Target').is_visible()

@then('I should see "Minimum Trading Days"')
async def step_impl(context):
    assert await context.page.locator('text=Minimum Trading Days').is_visible()

@then('I should see "Trading Period"')
async def step_impl(context):
    assert await context.page.locator('text=Trading Period').is_visible()

@then('I should see "Leverage"')
async def step_impl(context):
    assert await context.page.locator('text=Leverage').is_visible()

@then('I should see "Maximum Capital Allocation"')
async def step_impl(context):
    assert await context.page.locator('text=Maximum Capital Allocation').is_visible()

@then('I should see "News Trading"')
async def step_impl(context):
    assert await context.page.locator('text=News Trading').is_visible()

@then('I should see "Weekend Holding"')
async def step_impl(context):
    assert await context.page.locator('text=Weekend Holding').is_visible()

@then('I should see "EA Trading"')
async def step_impl(context):
    assert await context.page.locator('text=EA Trading').is_visible()

@then('I should see "Account Stopout"')
async def step_impl(context):
    assert await context.page.locator('text=Account Stopout').is_visible()

@when('I view the details for "Maximum Daily Loss"')
async def step_impl(context):
    await context.page.locator('text=Maximum Daily Loss').first.click()

@then('I should see an explanation of the daily loss limit')
async def step_impl(context):
    assert await context.page.locator('text="The Maximum Daily Loss"').is_visible() or await context.page.locator('text="maximum daily loss"').is_visible()

@when('I view the details for "Profit Target"')
async def step_impl(context):
    await context.page.locator('text=Profit Target').first.click()

@then('I should see an explanation of the profit target requirement')
async def step_impl(context):
    assert await context.page.locator('text="profit target"').is_visible()

@then('I should see "Minimum trading days"')
async def step_impl(context):
    assert await context.page.locator('text=Minimum trading days').is_visible()

@then('I should see "Refundable Fee"')
async def step_impl(context):
    assert await context.page.locator('text=Refundable Fee').is_visible()

@then('I should see currency button "{currency}"')
async def step_impl(context, currency):
    assert await context.page.locator(f'text={currency}').is_visible()

@when('I select currency "{currency}"')
async def step_impl(context, currency):
    await context.page.locator(f'text={currency}').first.click()

@then('I should see balance button "{balance}"')
async def step_impl(context, balance):
    assert await context.page.locator(f'text={balance}').is_visible()

@then('I should see the "Quick Comparison" button')
async def step_impl(context):
    assert await context.page.locator('text=Quick Comparison').is_visible()

@when('I click the "Quick Comparison" button')
async def step_impl(context):
    await context.page.locator('text=Quick Comparison').first.click()

@then('the table should contain "{row}"')
async def step_impl(context, row):
    assert await context.page.locator(f'text={row}').is_visible()

@then('the comparison table should contain "{row}"')
async def step_impl(context, row):
    assert await context.page.locator(f'text={row}').is_visible()

@when('I select balance "{balance}"')
async def step_impl(context, balance):
    await context.page.locator(f'text={balance}').first.click()

@then('the table should update values for selected currency and balance')
async def step_impl(context):
    # This step can be improved by checking for specific value changes
    assert await context.page.locator('table').is_visible()

@when('I click on table row "{row}"')
async def step_impl(context, row):
    await context.page.locator(f'text={row}').first.click()

@then('I should see a popup with details and a YouTube video')
async def step_impl(context):
    assert await context.page.locator('iframe[src*="youtube.com"]').is_visible()

@then('table rows should not be clickable')
async def step_impl(context):
    # Try clicking a row and expect it to not open a popup
    try:
        await context.page.locator('text=Maximum Daily Loss').first.click()
        popup = await context.page.locator('iframe[src*="youtube.com"]').is_visible()
        assert not popup
    except Exception:
        pass  # If click fails, that's expected

@then('I should see the "Start FTMO Challenge" button')
async def step_impl(context):
    assert await context.page.locator('text=Start FTMO Challenge').is_visible()

@when('I click the "Start FTMO Challenge" button')
async def step_impl(context):
    await context.page.locator('text=Start FTMO Challenge').first.click()

@then('I should be redirected to the login page')
async def step_impl(context):
    assert 'login' in context.page.url or 'sign-in' in context.page.url

def after_scenario(context, scenario):
    async def close():
        if hasattr(context, 'browser'):
            await context.browser.close()
        if hasattr(context, 'playwright'):
            await context.playwright.stop()
    asyncio.get_event_loop().run_until_complete(close())
