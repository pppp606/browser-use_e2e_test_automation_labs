# Sample Code for E2E Test Automation with `browser-use` and LLM

This sample code demonstrates automating end-to-end (E2E) tests using `browser-use` and a Large Language Model (LLM). The tests are conducted on the [Sauce Demo Website](https://www.saucedemo.com), and the test code is designed to run with `jest` and `playwright`.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install browser-use
playwright install

npm install
npx playwright install
```

> **Note**: Python 3.11 or higher is required to run `browser-use`.

## Configuration

Create a `.env` file based on `.env.sample`. The `OPENAI_API_KEY` is mandatory.

Example `.env` file:

```
OPENAI_API_KEY=
URL=https://www.saucedemo.com/
USER_ID=standard_user
PASSWORD=secret_sauce
SCENARIO_LANGUAGE=English
```

## Usage

### Step 1: Generate a Scenario

Run the following command to generate a test scenario:

```bash
python index.py scenario
```

Review the scenario generated in the `/scenario` directory. Edit the scenario if necessary to ensure it matches your requirements.

#### Example Output

```
path: /inventory.html,
actions:
  - test: Select 'Name (A to Z)' from sorting dropdown,
    expect: Products sorted in ascending order by name,
  - test: Click 'Add to cart' for Sauce Labs Backpack,
    expect: Sauce Labs Backpack added to cart,
  - test: Click 'Add to cart' for Sauce Labs Bike Light,
    expect: Sauce Labs Bike Light added to cart,
  - test: Click 'Add to cart' for Sauce Labs Bolt T-Shirt,
    expect: Sauce Labs Bolt T-Shirt added to cart,
  - test: Click 'Add to cart' for Sauce Labs Fleece Jacket,
    expect: Sauce Labs Fleece Jacket added to cart,
  - test: Click 'Add to cart' for Sauce Labs Onesie,
    expect: Sauce Labs Onesie added to cart,
  - test: Click 'Add to cart' for Test.allTheThings() T-Shirt (Red),
    expect: Test.allTheThings() T-Shirt (Red) added to cart,
  - test: Click cart icon,
    expect: Redirected to the cart page with selected items listed.
```

### Step 2: Generate Test Code

Run the following command to generate test code:

```bash
python index.py code
```

The test code will be generated in the `/tests` directory.

### Step 3: Run the Tests

Execute the tests using the following command:

```bash
npx playwright test
```

## ⚠️　Notes　⚠️

- The Sauce Demo Website is a demo site.
- When testing real products, handle account credentials carefully.
- Use secure environments for running the LLM locally or services like Azure OpenAI Service to ensure data is not reused improperly.
