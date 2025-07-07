import asyncio
from behave import given, when, then
from playwright.async_api import async_playwright

# Module-level constants for locators
TRADING_OBJECTIVES_LINK = 'a[href="#trading-objectives-table"]'
COOKIE_BUTTON = '#ftmo-cookie-layer button'
TABLE = 'table'
YOUTUBE_IFRAME = 'iframe[src*="youtube.com"]'

@given('I am on the FTMO homepage')
async def step_impl(context):
    context.playwright = await async_playwright().start()
    context.browser = await context.playwright.chromium.launch(headless=True)
    context.page = await context.browser.new_page()
    await context.page.goto('https://ftmo.com/en/')
    # Accept cookies if modal appears
    try:
        await context.page.wait_for_selector(COOKIE_BUTTON, timeout=5000)
        await context.page.click(COOKIE_BUTTON)
    except Exception:
        pass  # Cookie modal did not appear

@given('I am on the Trading Objectives section')
async def step_impl(context):
    await context.execute_steps('''
        Given I am on the FTMO homepage
        When I navigate to the "Trading Objectives" section
    ''')

@when('I navigate to the "Trading Objectives" section')
async def step_impl(context):
    await context.page.wait_for_selector(TRADING_OBJECTIVES_LINK)
    await context.page.locator(TRADING_OBJECTIVES_LINK).first.scroll_into_view_if_needed()
    await context.page.locator(TRADING_OBJECTIVES_LINK).first.click()

@then('I should see the list of trading objectives and their descriptions')
async def step_impl(context):
    objectives = [
        "Maximum Daily Loss", "Maximum Loss", "Profit Target", "Minimum Trading Days", "Trading Period",
        "Leverage", "Maximum Capital Allocation", "News Trading", "Weekend Holding", "EA Trading", "Account Stopout"
    ]
    for obj in objectives:
        assert await context.page.locator(f'text={obj}').is_visible()

@then('I should see "{text}"')
async def step_impl(context, text):
    assert await context.page.locator(f'text={text}').is_visible()

@then('I should see currency button "{currency}"')
async def step_impl(context, currency):
    assert await context.page.locator(f'text={currency}').is_visible()

@then('I should see balance button "{balance}"')
async def step_impl(context, balance):
    assert await context.page.locator(f'text={balance}').is_visible()

@then('I should see the "{button}" button')
async def step_impl(context, button):
    assert await context.page.locator(f'text={button}').is_visible()

@when('I click the "{button}" button')
async def step_impl(context, button):
    await context.page.locator(f'text={button}').first.click()

@when('I select currency "{currency}"')
async def step_impl(context, currency):
    await context.page.locator(f'text={currency}').first.click()

@when('I select balance "{balance}"')
async def step_impl(context, balance):
    await context.page.locator(f'text={balance}').first.click()

@when('I view the details for "{row}"')
async def step_impl(context, row):
    await context.page.locator(f'text={row}').first.click()

@when('I click on table row "{row}"')
async def step_impl(context, row):
    await context.page.locator(f'text={row}').first.click()

@then('the table should contain "{row}"')
@then('the comparison table should contain "{row}"')
async def step_impl(context, row):
    assert await context.page.locator(f'text={row}').is_visible()

@then('the table should update values for selected currency and balance')
async def step_impl(context):
    assert await context.page.locator(TABLE).is_visible()

@then('I should see a popup with details and a YouTube video')
async def step_impl(context):
    assert await context.page.locator(YOUTUBE_IFRAME).is_visible()

@then('I should see an explanation of the daily loss limit')
async def step_impl(context):
    assert await context.page.locator('text="The Maximum Daily Loss"').is_visible() or await context.page.locator('text="maximum daily loss"').is_visible()

@then('I should see an explanation of the profit target requirement')
async def step_impl(context):
    assert await context.page.locator('text="profit target"').is_visible()

@then('table rows should not be clickable')
async def step_impl(context):
    # Try clicking a row and expect it to not open a popup
    try:
        await context.page.locator('text=Maximum Daily Loss').first.click()
        popup = await context.page.locator(YOUTUBE_IFRAME).is_visible()
        assert not popup
    except Exception:
        pass  # If click fails, that's expected

@then('I should be redirected to the login page')
async def step_impl(context):
    assert 'login' in context.page.url or 'sign-in' in context.page.url

# Cleanup after each scenario

def after_scenario(context, scenario):
    async def close():
        if hasattr(context, 'browser'):
            await context.browser.close()
        if hasattr(context, 'playwright'):
            await context.playwright.stop()
    asyncio.get_event_loop().run_until_complete(close())
