# FTMO Trading Objectives Automated Testing

This project provides robust automated UI and acceptance tests for the "Trading Objectives" section on [ftmo.com](https://ftmo.com/en/), using Python, Playwright, and Behave.

## Features
- **Full coverage** of all currencies and balances in the Trading Objectives table.
- **Cell-by-cell validation** of all dynamic table values, including correct formatting for each currency.
- **Behave BDD scenarios** for all key UI elements and behaviors.
- **Standalone Playwright script** for fast, headless or UI-mode regression checks.
- **Easy maintenance:** Common values and formatting are DRY and centralized.

## Project Structure
```
FTMO/
├── features/
│   ├── trading_objectives.feature           # Behave feature file (scenarios)
│   └── steps/
│       └── trading_objectives_steps.py      # Behave step definitions (async Playwright)
├── playwright/
│   └── test_trading_objectives_table.py     # Standalone Playwright test script
├── pages/
│   └── trading_objectives_page.py          # Page Object for UI interactions
├── .gitignore                              # Git ignore rules
├── requirements.txt
└── README.md
```

## Setup
1. **Clone the repository:**
   ```sh
   git clone https://github.com/majxik/FTMO_TradingObjectives.git
   cd FTMO_TradingObjectives
   ```
2. **Create and activate a virtual environment:**
   ```sh
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   playwright install
   ```
   *(If you don't have a requirements.txt, install manually:)*
   ```sh
   pip install playwright behave
   playwright install
   ```

## Usage
### Run the Playwright Table Test
- **Headless (default):**
  ```sh
  python test_trading_objectives_table.py
  ```
- **UI mode:**
  ```sh
  python test_trading_objectives_table.py ui
  ```

### Run Behave BDD Tests
```sh
behave
```

## Notes
- The test script will check all currencies and balances, and validate all table values.
- The `.gitignore` ensures you don't commit virtual environments, Playwright reports, or other generated files.
- The code is ready for CI/CD integration and further extension (e.g., Page Object Pattern).

## Contributing
Pull requests and issues are welcome!

---

*Created by majxik.*
