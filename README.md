# Python and Statistics for Financial Analysis  <!-- omit in toc -->

Tuan's notes on the course [Python and Statistics for Financial Analysis](https://www.coursera.org/learn/python-statistics-financial-analysis/home/welcome) at [Coursera](https://www.coursera.org/).

- [Module 1: Visualizing and Munging Stock Data](#module-1-visualizing-and-munging-stock-data)
  - [Packages for Data Analysis](#packages-for-data-analysis)
  - [Importing data](#importing-data)
  - [Basic of DataFrame](#basic-of-dataframe)
  - [Generate new variables in DataFrame](#generate-new-variables-in-dataframe)
  - [:warning: View vs. Copy](#warning-view-vs-copy)
  - [Long one-share stock trading strategy](#long-one-share-stock-trading-strategy)
  - [Trading](#trading)
  - [Long and short concept](#long-and-short-concept)
  - [Keys takeaway](#keys-takeaway)

## Module 1: Visualizing and Munging Stock Data

### Packages for Data Analysis

- [Pandas](https://pandas.pydata.org/):
  - Excellent data structure for time series data.
  - Pre-process data easily with DataFrame.
- [Numpy](https://numpy.org/):
  - Package for numerical computing of array and matrix.
  - Provoides convinient tools for generating random numbers.
  - Helpful to shuffle data, generate a dataset with normal distribution.
- [Matplotlib](https://matplotlib.org/): produces high quality figures.
- [statsmodels](https://www.statsmodels.org/stable/index.html): contains modules for regression and time series analysis.

### Importing data

```python
import pandas as pd

df = pd.read_csv(csv_file, index_col = col name /col idx, parse_dates = col names)
```

- `csv_file`: path to CSV file to read.
- `col name`, `col idx`: name or index of column which is used as index.
- `col names`: list of column names which have data in date format.

### Basic of DataFrame

- DataFrame is a tabular structure of data consisting of:
  - rows: indexed by row labels (the index). Each row represents on record / entry / observation.
  - columns:
    - each column has a label (column name).
    - a column is a Series and has it own data type.
  - index: a label for each row. It can be integer, string, date, etc.
- DataFrame stores data column-wise, not row-wise like a database table.
  - efficiently access, slice, or process entire columns.
- Attributes:
  - `index`: returns index of DataFrame in a list-liked type.
  - `columns`: returns columns of DataFrame in a list-liked type.
  - `shape`: returns a tuple of the number of rows and the number of columns.
- Methods:
  - `head`: returns the first rows in DataFrame (`5`, by default).
  - `tail`: returns the last rows in DataFrame (`5`, by default).
  - `describe`: returns summary statistics on each column.
- Slicing:
  - `loc`: selects DataFrame (or Series, if selecting only one column) slices based on labels, returning a subset that is a **view** of the original DataFrame.
    ```python
    df.loc[start_idx:end_idx, col_name_start:col_name_end]
    ```
  - `iloc`: selects DataFrame (or Series, if selecting only one column) slices based on positions, returning a subset that is a **view** of the original DataFrame.
  ```python
  df.iloc[start_idx:end_idx, col_idx_start:col_idx_end]
  ```
- Visualizing:
  - `plot`: built-in method to visualize data.

### Generate new variables in DataFrame

- Select a single column:
  - `df[col_name]`: returns a Series that is a **view** of the original DataFrame.
  - `df[[col_name]]`: returns a DataFrame that is a **copy** of the original DataFrame.
- Select multiple columns: `df[[col_1, col_2, etc.]]`: return a DataFrame, that is a **copy** okf the original DataFrame.
- Create a new column from an old one:
  - `shift(n)`: move a whole column `n` rows upword :arrow_up: (`n < 0`) or downword :arrow_down: (if `n > 0`).
  ```python
  df["CloseTomorrow"] = df["Close"].shift(-1)
  ```
  - difference:
  ```python
  df["PriceDiff"] = df["CloseTomorrow"] - df["Close"]
  ```
  - division:
  ```python
  df["DailyReturn"] = df["PriceDiff"] / df["Close"]
  ```
  - list comprehension:
  ```python
  df["Direction"] = [
    1 if df.loc[idx, "PriceDiff"] > 0
    else -1
    for idx in df.index
  ]
  ```
  - moving average: is a widely used signal in stock trading. It smooths out noise. DataFrame `rolling` method is used to create moving average. It provides rolling window calculation like `mean`, `sum`, etc.
  ```python
  df["MA40"] = df["Close"].rolling(40).mean()
  df["MA200"] = df["Close"].rolling(200).mean()
  ```
    - `MA40` is called **fast signal** since it reflects the price over a short history.
    - `MA200` is called **slow signal** since it reflects the price over a long history.

### :warning: View vs. Copy

- **view**: is a **reference** to the original DataFrame's data. Changes to the view will affect the original.
- **copy**: is a **new object** with it own data. Changes do NOT affect the original DataFrame.
- :warning: Modifying a view can lead to unintended side effects.
- :white_check_mark: Use the `.copy()` method when modifying data if you're NOT sure whether it's a view or a copy to avoid side effects.

| Expression         | Returns   | View or Copy?                      |
| :----------------  | :-------- | :--------------------------------- |
| `df[col]`          | Series    | Usually a **view**                 |
| `df[[col]]`        | DataFrame | Always a **copy**                  |
| `df.loc[:, col]`   | Series    | Often a **view**                   |
| `df.loc[:, [col]]` | DataFrame | Usually a **view**, but not always |

### Long one-share stock trading strategy

- Buy **1** share of a stock instead of many.
- Strategy:
  - use fast & slow signals (MA10 and MA50, for instance).
  - if $fast > slow$, meaning that the recent prices are gaining => **buy**.
  - otherwise, => **do nothing**.
- Why use it ?
  - low risk: max loss = price of one share.
  - good  for beginners: test the market without big exposure.
  - hands-on learning: get to experience real price movements.

### Trading

- Calculate fast and slow signals `MA10` (fast) and `MA50` (slow).
  - If `MA10` > `MA50`: the stock price is believed that it **goes up** :arrow_up: in the next several days.
  - otherwise, the stock price is believed that it **goes down** :arrow_down: in the next several days.
- Calculate the number of shares held. `Shares` denotes whether we long or not.
```python
Shares = 1 if MA10 > MA50
         0 otherwise
```
- `Shares = 0` means we don't have stock at hand => `profit = 0`.
- Calculate daily profit: $Daily\_profit = close\_price\_of\_tomorrow - close\_price\_of\_today$.
- Generate a graph displaying daily profit and accumulated wealth.

### Long and short concept

- **long:** **buy** a stock and **expecting** the price goes up :arrow_up:.
  - **later**, when it goes up, **sell** it for a *higher price* to make a profit.
- **short:** **borrow** shares and **sell** them right away, **hoping** the price drops :arrow_down:.
  - **later**, when it drops, **buy** them back at a *lower price* to return to the lender, pocketing the difference.

| Proposition | Expect price to       | First               | Then       | Profit if price      |
| :-----------| :-------------------- | :------------------ | ---------- | -------------------- |
| long        |  go up :arrow_up:     | **buy**             | sell later | go up :arrow_up:     |
| short       |  go down :arrow_down: | **sell** (borrowed) | buy back   | go down :arrow_down: |

### Keys takeaway

- Trading terms:
  - daily profit.
  - moving average
  - fast vs. slow signal.
  - long vs. short.
- DataFrame / Series:
  - Basics:
    - Attributes: `index`, `columns`, `shape`.
    - Methods:
      - `read_csv`.
      - `head`, `tail`, `describe`, `loc`, `iloc`.
      - `plot`.
      - `set_index`, `reset_index`.
  - Advanced:
    - Methods: `shift`, `rolling`.
    - :warning: view vs. copy.
