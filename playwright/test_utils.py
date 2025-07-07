import re

CURRENCIES = {
    "USD": ["$10,000", "$25,000", "$50,000", "$100,000", "$200,000"],
    "GBP": ["£10,000", "£20,000", "£35,000", "£70,000", "£140,000"],
    "EUR": ["€10 000", "€20 000", "€40 000", "€80 000", "€160 000"],
    "CZK": ["250 000 CZK", "500 000 CZK", "1 000 000 CZK", "2 000 000 CZK", "4 000 000 CZK"],
    "CAD": ["$15,000", "$30,000", "$60,000", "$120,000", "$240,000"],
    "AUD": ["$15,000", "$30,000", "$65,000", "$130,000", "$260,000"],
    "CHF": ["10 000 CHF", "20 000 CHF", "40 000 CHF", "80 000 CHF", "160 000 CHF"]
}

COMMON_ROWS = {
    "trading-period": ["unlimited", "unlimited", "unlimited"],
    "minimum-trading-days": ["4 days", "4 days", "X"],
}

FEE_LIST = ["€89", "€250", "€345", "€540", "€1 080"]


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


def build_expected_values():
    expected = {}
    for currency, balances in CURRENCIES.items():
        for i, balance in enumerate(balances):
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
            max_daily_loss = fmt(bal_num / 20, currency)
            max_loss = fmt(bal_num / 10, currency)
            profit_1 = fmt(bal_num / 10, currency)
            profit_2 = fmt(bal_num / 20, currency)
            fee = FEE_LIST[i] if i < len(FEE_LIST) else FEE_LIST[-1]
            expected[(currency, balance)] = {
                **COMMON_ROWS,
                "maximum-daily-loss": [max_daily_loss] * 3,
                "maximum-loss": [max_loss] * 3,
                "profit-target": [profit_1, profit_2, "X"],
                "refundable-fee": [fee, "free", "refund"],
            }
    return expected
