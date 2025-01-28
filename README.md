browser-useとLLMを利用したe2eテストの自動化を目的としたサンプルコードです。
テストは、Sauce Demo Webサイト (https://www.saucedemo.com) で行っています。

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install browser-use
playwright install

npm install
npx playwright install
```

* browser-useを実行するためにpythonは3.11以上が必要です

## 設定
.env.sampleを参考に.envファイルを作成してください
OPENAI_API_KEYが必要です。

```
OPENAI_API_KEY=
URL=https://www.saucedemo.com/
USER_ID=standard_user
PASSWORD=secret_sauce
SCENARIO_LANGUAGE=English
```

## 使い方
### Step1 シナリオを作成

```bash
python index.py scenario
```

`/scenario` に出力されるシナリオを確認しレビューし、必要であれば修正をしてください。

#### 出力例

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

### Step2 テストコードを生成

```bash
python index.py code
```

/tests にテストコードが生成されます。

### Step3 テストの実行

```bash
npx playwright test
```
