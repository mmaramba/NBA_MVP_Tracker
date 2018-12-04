# NBA_MVP_Tracker

NBA MVP Tracker using Python3 and BS4.
Scrapes data from bbref and stores as CSV files.
Converts data into Pandas dataframes and trains RF model on scraped data.
Makes predictions on current NBA MVP.

Dependencies: BeautifulSoup 4, Pandas, NumPy, Pydotplus, scikit-learn

To run:
 
python3 Scrape.py (to scrape bbref data and store in csv)

python3 Predict.py (to train model and make predictions)
