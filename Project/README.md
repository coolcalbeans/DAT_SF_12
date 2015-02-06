Problem Statement:
Given a stock ticker, find the nearest set of tickers using significant attributes from a set of ticker attributes. Use the nearest neighbors, to predict P/E values for a given ticker. Solution can be broken down as
	
1) Collect:
Ticker data from Sharadar.com ~2900 US Equity Tickers
Use Ticker Data to scrape for fundamentals from FinViz ~2750 US Equity Tickers to get ~70 Fundamental Attributes of tickers.
The final data set should include ~190,000 Data points

2) Clean/Parse:
Change attribute data types
Decide or come up with logic on how to handle NaNs
Drop outliers? Have to explore this.

3) Explore/Model:
Check if Market Cap has significant dependency on any of the 71 attributes.
Use maybe Linear Regression to decide on significant attributes from the set of 71 attributes.
Use the subset of the ~70 attributes in a KNN to figure out a nearest neighbor to a given ticker.
If no significant variables, Project is screwed and I would need help. Or maybe I can use all the ~70 attributes :)?

4) Predict:
Given a stock ticker, predict their P/E
Provide a Confidence Range for the P/E using yearly Equity volatility.
Use the confidence range to say whether the equity is Over-valued / Under-valued / Fairly-valued 

5) Inference/Visualize:
Visualize the significant variables
