import time as true_time
import pprint
import pathlib
import operator
import pandas as pd

from datetime import datetime
from datetime import timedelta
from configparser import ConfigParser

from trading_robot.bot import TradeBot #TradeBot as PyRobot
from trading_robot.indicator import Indicators

# grab config files
config = ConfigParser()
config.read('configs/config.ini')

CLIENT_ID = config.get('main', 'CLIENT_ID')
REDIRECT_URI = config.get('main', 'REDIRECT_URI')
CREDENTIALS_PATH = config.get('main', 'JSON_PATH')
ACCOUNT_NUMBER = config.get('main', 'ACCOUNT_NUMBER')

# initialize robot
trading_robot = TradeBot(
    client_id=CLIENT_ID,
    redirect_uri=REDIRECT_URI,
    credentials_path=CREDENTIALS_PATH,
    trading_account=ACCOUNT_NUMBER,
    paper_trading=True
)

# create new portolio
trading_robot_portfolio = trading_robot.create_portfolio()

# add positions to portfolio
multi_position = [
    {
        'asset_type': 'equity',
        'quantity': 2,
        'purchase_price': 4.00,
        'symbol': 'TSLA',
        'purchase_date': '2020-01-31'
    },
    {
        'asset_type': 'equity',
        'quantity': 2,
        'purchase_price': 4.00,
        'symbol': 'SQ',
        'purchase_date': '2020-01-31'
    }
]

# add positions to portfolio
new_positions = trading_robot.portfolio.add_positions(positions=multi_position)
# pprint.pprint(new_positions)

# add a single position
trading_robot.portfolio.add_position(
    symbol='MSFT',
    quantity=10,
    purchase_price=10.00,
    asset_type='equity',
    purchase_date='2020-04-01'
)

if trading_robot.regular_market_open:
    print('Regular Market Open')
else:
    print('Regular Market Not Open')

if trading_robot.pre_market_open:
    print('Pre Market Open')
else:
    print('Pre Market Not Open')

if trading_robot.post_market_open:
    print('Post Market Open')
else:
    print('Post Market Not Open')

# grab current quotes in portfolio
current_quotes = trading_robot.grab_current_quotes()
#pprint.pprint(current_quotes)

# define date range
end_date = datetime.today()
start_date = end_date - timedelta(days=30)

# grab historical prices
historical_prices = trading_robot.grab_historical_prices(
    start=start_date,
    end=end_date,
    bar_size=1,
    bar_type='minute'
)

stock_frame = trading_robot.create_stock_frame(data=historical_prices['aggregated'])

pprint.pprint(stock_frame.frame.head(n=20))

new_trade = trading_robot.create_trade(
    trade_id='long _msft',
    enter_or_exit='enter',
    long_or_short='long',
    order_type='lmt',
    price=150.00
)

new_trade.good_till_cancel(cancel_time=datetime.now() + timedelta(minutes=90))

new_trade.modify_session(session='am')

new_trade.instrument(
    symbol='MSFT',
    quantity=2,
    asset_type='EQUITY'
)

new_trade.add_stop_loss(
    stop_size=.10,
    percentage=False
)