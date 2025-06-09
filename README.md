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
- [Module 2: Random variables and distribution](#module-2-random-variables-and-distribution)
  - [Random variables](#random-variables)
  - [Frequency and Distribution](#frequency-and-distribution)

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


## Module 2: Random variables and distribution

### Random variables

- A random variable is a variable whose value is the result of a random event.
- Types of random variables:
  - Discrete random variable:
    - takes on a countable number of possible values.
    - examples: rolling a dice, number of heads in a coin flips, etc.
  - Continuous random variable:
    - takes on any value in a range, often is infinite & uncountable.
    - examples: stock prices, temperature, etc.
- DataFrame / Series method `sample`:
  - randomly select `n` rows from the DataFrame / Series.
  - argument `replace=True`: does sampling with replacement, meaning the **same row can be picked more than once**.
  - returns a DataFrame / Series.

### Frequency and Distribution

- **Frequency** is the count of how many times a value appears in a dataset.
- **Relative frequency** is frequency of a value divided by total number of observations.
  - tells us how likely each value is, based on our data.
- **Distribution** of a random variable:
  - tells us how likely each possible value (or a range of values) is.
  - describes the pattern of outcomes that we might expect from a random process.
  - for **discrete random variable**:
    - we get a probablity distribution which consist of:
      - a list of possible values that the variable can take.
      - and the probability of each one.
    - it's called **PMF** (*Probability Mass Function*) that assign probabilty to exact values.
  - for **continuous random variable**:
    - we get a **PDF** (*Probability Density Function*) which describes how dense the probability is in different regions.
- **Mean** of a distribution is the **expected value** or the average outcome over the long run.
  - it's like the **center** or **balance point** of the distribution.
  - denoted as $\mu$ or $E[X]$.
  - for a discrete random variable:

    $$E[X] = \mu = \sum_{i=1}^n x_ip_i$$

    $x_i, p_i$ are possible values and their pobabilities.
- **Variance** tells us **how spread out** the values are from the mean.
  - high variance => values vary a lot from the mean.
  - low variance => values are tightly clustered near the mean.
  - denoted as $\sigma^2$.
  - formula: it's average of squared differences from the mean.

    $$\sigma^2 = E[(X-\mu)^2] = \sum_{i=1}^n (x_i - \mu)^2p_i$$
  - measured in **squared units**.
  - harder to interpret intuitively.
- **Standard Deviation** is the square root of the variance.
  - denoted as $\sigma$.
  - is in the **same units** as the data.
    - much more interpretable in compare with variance, can directly compare it to data values.
    - we **report standard deviation** instead of variance because it's more understandable and in the right units.
- DataFrame / Series methods:
  - `sum` (on DataFrame): add up values along an axis.
    - `axis=0` (default): sum down columns.
    - `axis=1`: sum across rows.
    - returns a Series where each entry is the total for one column (or row).
  - `value_counts`: counts how many times each unique tuple (on DataFrame) or value (on Series) appears.
    - returns a Series.
    - gives the distribution of values.
      - indexes are **possible values**.
      - values are **frequencies** of values.
    - `normalize=True`: gives **relative frequencies** instead of frequencies.
- **Continuous Random Variable**
  - **Probability Density Function (PDF)**:
    - describes how densely packed the probability is at each point.
      - the probability at an exact point is always 0 (since nb_points $= \infty$).
      - find probabilities **over an interval** instead.
    - for a PDF, the probability that a random variable $X$ falls in an interval $[a, b]$ is:

      $$P(a \leq X \leq b) = \int_a^b f(x)dx$$
    - define the PDF based on **known distribution** or **estimated** from data.
    - there're many types of distribution: normal, exponential, uniform, gamma, beta, etc.
    - each type has its own formula of PDF. For instance, the normal distributuion

      $$f(x, \mu, \sigma) = \frac{1}{\sqrt{2\pi\sigma^2}e^{-\frac{(x-\mu)^2}{2\sigma^2}}}$$
    - estimate the PDF from a samle using:
      - histograms: basic but rough.
      - kernel density estimation (KDE): smooth, better.
  - **Histogram**:
    - is a special kind of bar plot that shows **how often** data points fall into certain ranges (called **bins**).
    - gives a **picture of the distribution** of the data.
    - **why use a histogram** to visualize distributions ?
      - data is messy. We usually have millions, billions points.
      - plotting individual points would be chaotic.
      - histogram organizes the data into a clear shape.
      - the shape of the histogram often **resembles** the underlying probablity distributiuon.
    - **how bin size affects** a histogram ?
      - small:
        - many narrow bins.
        - histogram looks very noisy.
        - hard to spot the real shape.
      - big:
        - histogram looks oversmoothed.
        - lose important features such as peak, dips, etc.
      - just right:
        - show a clear, smooth shape.
        - best for understanding distribution.
    - **rules of thumb** for choosing the number of bins: given $N$ data points.
      - Sturges' rule: nb_bins $= \log_2(N) + 1$
      - Square-root rule: nb_bins $= sqrt(N)$
  - **Kernel Density Estimate (KDE)**:
    - is a way to reconstruct a smooth guess of the probability from data using small smooth bumps around each point.
    - instead of cutting data into bins like histogram, KDE places a smooth curve over each data point, then it adds all the curves together to create a smooth overall estimate.
    - results in a smooth curve that flows nicely across the data instead of jumping in steps like histogram.
- **Cumulative Distribution Function (CDF)**:
  - tells us what is the probability that a random variable $X$ is less than or equal to a certain value $x$.

    $$F(x) = P(X \leq x)$$
  - is used for:
    - find probabilities, for instance:

      $$P(a \leq x \leq b) = F(b) - F(a)$$
    - understand distribution shape: we can see where the most of the probability is.
    - transform data: CDFs are used to normalize distributions.
  - attributes:
    - $0 \leq F(x) \leq 1 \ \forall x$
    - always non-decreasing.
    - discrete variables: jumps at each point.
    - continuous variables: smooth curve.
  - **how to compute CDF ?**
    - discrete variables:

      $$F(x) = \sum_{t \leq x} P(X=t)$$
    - continuous variables:

      $$F(x) = \int_{-\infty}^x f(t)dt$$

      where $f(x)$ is the probability density function (PDF) of the variable.
- **Normal Density Curve**:
  - is the graph of the probability density function (PDF) for the normal distribution.
  - is also known as: normal curve, bell curve, Gaussian curve.
  - key properties:
    - perfect symetric around the center (the mean $\mu$).
    - single peak, highest at the center.
    - tappers off smoothly towards both sides.
    - never touches the x-axis, but get closer and closer.
    - total area $= 1$, the whole curve covers probability $1$.
    - mean = median = mode, all in the center.
  - others:
    - the center of the curve is at $\mu$.
    - the spread (width) of the curve depends on $\sigma$.
      - big $\sigma$: wide and flat curve.
      - small $\sigma$: narrow and steep curve.
    - the curve shows **how likely values are**:
      - near $\mu$: very likely (high curve).
      - far from $\mu$: very unlikely (low curve).
- **Quantiles**:
  - answer this kind of question: at what value $x$ is a certain percentage of the data to the left ?
  - in other words, quantiles split the distribution into parts based on probability.
  - the $p$-quantile of a distribution is the value $x$ such that

    $$P(X \leq x) = p$$

    $=> x$ is the point where the CDF equals $p$.
  - quantiles are used for making decisions based on probabilities like:
    - *what's a threshold to include 95% of outcomes ?*
    - *what's the range where most of the data falls ?*
- **Value at Risk (VaR)**:
  - measures how much we could lose on an investment with a certain probability over certain time.
  - example: give a stock porfolio worth $1 million. $1-$day VaR at 95% confidence = $20k means:
    - 95% chance losing $\leq$ $20k in one day.
    - $\approx$ 5% chance losing $\geq$ $20k in one day.
  - key points

      | Aspect           | Meaning                                 |
      | :--------------- | :-------------------------------------- |
      | Confidence level | Commonly 95% or 99%                     |
      | Time horizon     | 1 day, 10 days, 1 year (depends)        |
      | Amount           | Potential loss                          |
      | Risk Measurement | Gives a single number to summarize risk |

  - ways to compute VaR:
    - historical simulation: use past data to simulate outcomes.
    - variance - covariance (parametric): assume normal distribution, then use mean $\mu$ and standard deviation $\sigma$.
    - Monte Carlo simulation: simulate thousands of random scenarios.
  - real-life example: banks and investment firms must report their VaR to regulators like Federal Reserve.

    "*Our $10-$days 99% VaR is $100m*" means only 1% chance they lose more than $100m in 10 days.
- **Log daily returns**:
  - are used in doing analysis instead of raw daily returns in real finance intuition.
  - main reasons:
    - simpler math: log returns make percentage changes addictive over time.
    - time consistency: 5 daily log returns can just be added up to get $5-$day log return.
    - better symmetry: log returns are more symmetrically distributed => look more like a normal curve (bell curve).
    - avoid negatives: prices can't go below 0, but log returns handle that cleanly.
      - when $price = 0$ => $\log(0)$ is undefined: this is consistent with reality, a stock that hits 0 is bankrupt and no longer trade.
      - negative prices are never implied as logarithm forces positive input.
      - we can't lose more than 100% and log return captures that mathematically cleanly.
    - easy modeling: many financial models assume log-normal price behavior as this respects the zero-bound.
- **$Z$-distribution**:
  - is another name for standard normal distribution, **a special case** of the normal distribution with $\mu = 0, \sigma = 1$.
  - is called $Z$ because $Z-$score is used to standardize data points.

    $$Z = \frac{X - \mu}{\sigma}$$
  - $Z-$score tells us **how far** a point is from the mean $\mu$.
- Python functions, modules:
  - `np.log`: compute logs of a Series, or liked-array values.
  - `norm` module from `scipy.stats`:
    - `norm.pdf`: returns probability density values.
    - `norm.cdf`: returns cummulative distribution values.
    - `norm.ppf`: returns $x$ value of a $p-$quantile.

      *ppf* stands for percent point function (inverse of CDF).
  - Series methods:
    - `mean`: returns the average of a Series.
    - `std`: returns the standard deviation of a Series.
      - `ddof=0`: calculate population standard deviation, used when **having the entire** population.
      - `ddof=1` (default): calculate sample standard deviation, used when **having a sample** and want to **estimate** population stats.

      *ddof* stands for degrees of freedom.
      - Population Standard Deviation:
        $$\sigma = \sqrt{\frac{1}{n} \sum_{i = 1}^n (x_i - \mu)}$$
      - Sample Standard Deviation:
        $$\sigma = \sqrt{\frac{1}{n-1} \sum_{i = 1}^n (x_i - \mu)}$$

        divide by $n-1$ instead of $n$ to correct for bias when estimating population variance from a sample (*Bassel's correction*).
    - `hist`: plots histogram.
  - Seaborn functions:
    - `histplot`: plot histogram with/without KDF curve of data points.
    - `kdeplot`: plot KDE curve of a list of data points.
- **More about VaR (Value at Risk)**:
  - VaR estimates the maximum potential loss of a porfolio, investment over a given period with a specified confidence level.
  - VaR is defined by three things:
    - time horizon: 1 day, 10 days, 1 year, etc.
    - confidence level: 95%, 99%, etc.
    - loss amount: -2.3%, $10k, etc.
  - Example: *the daily 95% VaR is $10k* means:
    - 95% confidence that won't lose more than $10k in a single day.
    - $\approx$ 5% chance that will lose more than $10k, meaning the return $\leq$ -$10k.
  - Related to quantile:
    - a quantile is a value below which a certain percentage of data falls.
    - example: the $5^{th}$ percentile ($0.05$ quantile) is the value below which 5% of observation lie.
    - VaR at 95% = the $5^{th}$ percentile ($0.05$ quantile) of returns.

      $$VaR_\alpha = Quantile_{1-\alpha}$$
  - More examples:
    - *$0.05$ quantile of return = -0.025* means:
      - 5% chance the return $\leq$ -2.5%
      - $\approx$ 95% confidence that loss $\leq$ 2.5%
      - $\Leftrightarrow$ 95% VaR = 2.5%
    - *$0.95$ quantile of return = +0.025* means:
      - 95% chance the return $\leq$ 2.5%
      - 5% chance the return $\geq$ 2.5%
      - $\approx$ 95% confidence that gain $\geq$ 2.5%
  - In statistical terms:
    - $VaR < 0 \Rightarrow$ in the left tail $\Rightarrow$ risk of loss.
    - $VaR > 0 \Rightarrow$ in the right tail $\Rightarrow$ chance of exceptional gain.
  - Disadvantages of VaR:
    - VaR doesn't say **how bad the worst outcomes** might be.
    - Example: *95% VaR = 2.5%* means:
      - 95% confidence the loss is not more than 2.5%, but how about the worst 5% ?
      - 5% chance the loss $\geq$ 2.5%, but don't know how bad it is ? 3%, 30%, or 50%, etc.
