
# coding: utf-8

# This file was written and can be executed with **Anaconda/Jupyter**. From it, were generated the two
# files: **JPM_2.py** (with the Python code with comments) and the HTML file **JPM_2.html**.<br>
# 
# **These 3 files share the same content**<br>
# 
# One can execute JMP.py under a python interpreter with the command:<br>
# '>>> execfile('JPM_2.py')'<br>
# Nevertheless I suggest the reading of JPM_2.html in any browser if you are not using Jupyter.<br>
# The format of the Python file might be slightly less readable.<br>
# 
# The content is the following.<br>
# 
# It defines data for stocks and trades. They are global variables:<br>
# **stock** of type pd.DataFrame for the list of stocks<br>
# **trades, tr,...** of type pd.DataFrame for trade records<br>
# 
# Then functions answering the spreadsheet questions<br>
# **1.a.i) dividend_yield(...)**<br> 
# **1.a.ii) price_earnings_ratio(...)** <br>   
# **1.a.iii) add_trade(...)**<br>
# **1.a.iv) volume_weighted_stock_price(...)**<br>
# **b.** **geometric_mean(...)** and **GBCE_stock_index(...)**<br>
# These functions are **carefully commented**.<br>
# 
# Numerous data sets are also defined and executed so that the author
# hopes that it can be easy for anyone to use this script for
# executing and testing. In particular the end of file contains data
# and function calls for testing.<br>
# 
# Thanks for your attention.<br>
# Best regards.<br>
# Vincent Schmitt.

# I chose to use Python/Pandas/Numpy for this test.

# In[1]:


import pandas as pd
import numpy as np


# Definition of a sample set of data. The same as defined in the spreadsheet.

# In[2]:


stock = pd.DataFrame()


# In[3]:


data = {'TEA': ['Common', 0., np.nan, 100.],
         'POP':['Common', 8., np.nan, 100.],
         'ALE':['Common', 23., np.nan, 60.],
        'GIN': ['Preferred', 8., 2., 100.],
        'JOE': ['Common', 13., np.nan,250.]
        }


# In[4]:


data


# In[5]:


stock = pd.DataFrame.from_dict(data, orient='index')


# In[6]:


stock.columns = ['Type','LastDiv','FixedDiv','ParV']


# In[7]:


stock


# Above is the Pandas frame 'stock' with data similar to the spreadsheet.<br>
# **I will use this global variable in this test.**

# In[8]:


stock.loc['JOE']


# In[9]:


'JOE' in stock.index


# In[10]:


market_price = 12.00


# In[11]:


stock.loc['JOE']['LastDiv']/market_price


# Below a first version of the computation of the dividend yield. It does note take yet into
# account the "preferred" shares.

# In[12]:


def dividend_yield_0(stock_index, market_price=None):
    dy = (stock.loc[stock_index]['LastDiv'])/market_price
    return dy


# In[13]:


dividend_yield_0('JOE',12.)


# In[14]:


dividend_yield_0('JOE',60.)


# **1.a.i** Below is the definitive version of the function dividend_yield computing the dividend yield.<br>
# Arguments are:<br>
# stock_index: the key index for the stock. This stock should exist in the global variable 'stock'.<br> 
# stock_index corresponds there to a unique row, i.e. stock_index is a key.<br>
# market_price: a market price, that should be a strictly positive number.<br>
# 
# The stock list is the global variable 'stock'.<br>
# There are basic tests on arguments (type and range). If an argument is not valid, a vualue NAN
# is returned and a warning message is issued.

# In[15]:


# import to test number types
import numbers
#
def dividend_yield(stock_index, market_price):
    # basic tests on arguments
    # existence of the stock with index stock_index
    # market_price should be a number and strictly positive 
    if stock_index not in stock.index:
        print stock_index + ' not an existing stock index'
        return np.nan
    if not isinstance(market_price, numbers.Number):
        print market_price
        print 'market_price not a number'
        return np.nan
    if market_price <= 0:
        print market_price
        print 'market_price not a strictly positive number'
        return np.nan
    # 
    #
    st = stock.loc[stock_index]
    if st['Type'] == 'Preferred':
        return (st['FixedDiv']/100.)*st['ParV']/market_price
    return st['LastDiv']/market_price 


# In[16]:


dividend_yield('JOE',26.)


# In[17]:


dividend_yield('GIN',100.)


# In[18]:


dividend_yield('XXX',100.)


# In[19]:


dividend_yield('GIN','aaa')


# In[20]:


dividend_yield('TEA',100.)


# **1.a.ii.** I understand from the given definitions that the P/E ratio is just **the inverse of the dividend yield**. (Note: I am used to the definition P/E ratio = earnings per share/price per share, not so much dividend/price)<br>
# 
# Below is the function computing the P/E ratio.<br>
# It simply returns the inverse of the dividend yield computed in **1.a.i**. Arguments are the same as in **1.a.i**.<br>
# A NAN value is returned if its arguments are invalid, i.e. yielding a zero or undefided dividend yield.

# In[21]:


def price_earnings_ratio(stock_index, market_price):
    dy = dividend_yield(stock_index, market_price)
    # very basic tests on the value returned, that could be improved if necessary! 
    if dy == np.nan:
        return np.nan
    if dy == 0:
        return np.nan
    return 1/dy


# In[22]:


price_earnings_ratio('JOE',26.)


# In[23]:


price_earnings_ratio('GIN',100.)


# In[24]:


price_earnings_ratio('TEA',100.)


# In[25]:


price_earnings_ratio('XXX',100.)


# For the next question, I define an array (a "Pandas Frame") storing the trade records. Then I am using 
# it as a global variable.

# In[26]:


trades = pd.DataFrame(columns = ['date','stock_index','qty','buy/sell','price'])


# In[27]:


trades


# I am using Pandas Timestamp for timestamping.

# In[28]:


pd.Timestamp.now()


# In[29]:


pd.Timestamp(year=2017, month=1, day=1, hour=12, minute=59, second=3)


# **1.a.iii.** Below is the function adding a trade record into a list.<br>
# 
# It takes as input:<br>
# the list of trades t that is a Pandas Frame as defined before<br>
# the list of arguments corresponding to a peculiar trade:<br>
# stock_index: index of the stock traded, it should exist as a key in stock<br>
# qty: quantity, an integer<br>
# bs_ind: buy/sell index, values should be 'buy'/'sell'(it could have been a boolean!)<br>
# price: price per stock, a positive number<br>
# date: the date of the trade, should be a pd.Timestamp. **By default it is set to the current date**.<br>
# 
# It returns the list t in which a new trade has been recorded.<br>
# 
# **Beware: for simplicity, the implementation below does not check the argument types nor their consistency.** 
# This could be done if necessary.

# In[30]:


def add_trade(t, stock_index, qty, bs_ind, price, date=None):
    if (date == None):
        date = pd.Timestamp.now()
    t = t.append({'date':date, 'stock_index':stock_index,'qty':qty, 
                   'buy/sell':bs_ind, 'price':price},ignore_index=True)
    return t


# In[31]:


tr = trades


# In[32]:


tr


# In[33]:


tr = add_trade(tr, 'JOE', 100, 'sell', 150.)


# In[34]:


tr = add_trade(tr, 'JOE', 100, 'sell', 250.)
tr = add_trade(tr, 'JOE', 100, 'buy', 250.)
tr = add_trade(tr, 'GIN', 200, 'buy', 50.)
tr = add_trade(tr, 'ALE', 200, 'buy', 150.)
date = pd.Timestamp(year=2017, month=1, day=1, hour=12, minute=59, second=3)
tr = add_trade(tr, 'TEA', 200, 'buy', 100., date)
tr = add_trade(tr, 'GIN', 200, 'sell', 75.)
tr = add_trade(tr, 'TEA', 300, 'sell', 125.)
tr = add_trade(tr, 'POP', 300, 'sell', 300.)
tr = add_trade(tr, 'ALE', 200, 'sell', 150., 
               pd.Timestamp(year=2017, month=1, day=1, hour=12, minute=59, second=3))
tr = add_trade(tr, 'ALE', 150, 'sell', 50.)
tr = add_trade(tr, 'ALE', 300, 'sell', 100.)


# In[35]:


tr


# Question **1.a.iv**.<br>
# The stock considered should have been traded within the last 15 minutes.
# In Pandas differences of time stamps of type pd.Timestamp are of type pd.Timedelta.

# In[36]:


time_now = pd.Timestamp.now()


# In[37]:


min_delta = '360 min'


# In[38]:


time_delta = pd.Timedelta(min_delta)


# In[39]:


time_delta


# In[40]:


tr.date


# In[41]:


lt_recent= tr[( time_now - tr.date < time_delta ) & (tr.stock_index == 'JOE')]


# In[42]:


lt_recent


# **1.a.iv.** Computing the Volume Weighted Stock Price for a particular stock.<br>
# According to the given formula, I understand that **the VWSP is the average trading price of a given stock within the last 15 minutes**<br>
# 
# The function below computes this.<br>
# 
# It takes as arguments:<br>
# the trading list: tr_l (a Pandas Frame as defined above)<br>
# the stock index: st_ind<br>
# min_delta: a parameter for the time delay for considering trades in the list, **by default: 15 minutes**. 
# It is a string that should denote a delay as requested by the constructor pd.Timedelta.<br>
# 
# It returns the average trading price of the stock within the last minutes as specified by min_delta.<br>
# If there were no trades for that stock a NAN value is returned.<br>

# In[43]:


def  volume_weighted_stock_price(tr_l , st_ind, min_delta='15 min'):
    time_now = pd.Timestamp.now()
    # print time_now
    time_delta = pd.Timedelta(min_delta)
    # print time_delta
    t_rec = tr_l[(time_now - tr_l.date < time_delta) & (tr_l.stock_index == st_ind)]
    #print t_rec
    if t_rec.empty:
        #print 'zero'
        return np.nan
    num = (t_rec['price']*t_rec['qty']).sum()
    # print num
    den = t_rec['qty'].sum()
    # print den
    if den == 0:
        #print 'denominator null'
        return np.nan
    vwsp = num/den
    return vwsp


# In[44]:


volume_weighted_stock_price(tr , 'JOE')


# In[45]:


volume_weighted_stock_price(tr , 'JOE', min_delta='360 min')


# In[46]:


volume_weighted_stock_price(tr , 'ALE', min_delta='360 min')


# **Question b.**

# For the geometric average I did the average of the logarithms and applied 
# the exponentiation. 
# If the number of values in the list is 0 the value returned is 1. 
# Values should be strictly positive.

# In[47]:


import math
def  geometric_mean(arr):
    gm = 0
    n = 0
    for pr in arr:
        n = n + 1
        gm = gm + math.log(pr)
    if (n == 0):
        return 1.     
    return math.exp(gm/n)           


# In[48]:


geometric_mean([1])


# In[49]:


geometric_mean([])


# In[50]:


geometric_mean([1,2])


# In[51]:


geometric_mean([1,2,4])


# In[52]:


geometric_mean([34., 56., 76., 23., 45., 22.,67.])


# It took me some time to understand that GBCE meant "Global Beverage Corporation Exchange"! What is the "BGCE All Share Index" then? Is that just the geometric mean price for all GBCE stocks? This is what is computed next: **the geometric mean of stock prices given by the computation a.iv.**.<br>
# 
# Note: I understand that log is the good measure of price variations but considering the average **per stock** looks a strange index to me. But I am not sure that I got it correctly.

# In[53]:


stock.index


# In[54]:


stock_indexes = stock.index.values


# In[55]:


stock_indexes


# In[56]:


tr


# In[57]:


arr2 = [volume_weighted_stock_price(tr , stock_index, min_delta='360 min') for stock_index in stock_indexes]


# In[58]:


arr2


# In[59]:


geometric_mean(arr2)


# The function GBCE_stock_index below computes the geometric mean of all stock prices.
# Prices considered are the average trading prices computed by the function volume_weighted_stock_price -- see **1.a.iv.**<br>
# 
# Its inputs:<br>
# stock_list: the stock list that is a Pandas Frame as specified before<br>
# trade_list: the trade list that is a Pandas Frame as specified before<br>
# min_delta: a string denoting a time delay for considering recent trades. By default its value
# corresponds to a **15 minute delay**.

# Note: The implementation is such that if a stock has not been traded recently
# the value returned is NAN.

# In[60]:


def GBCE_stock_index(stock_list,trade_list, min_delta='15 min'):
    stock_indexes = stock_list.index.values
    arr = [volume_weighted_stock_price(trade_list , i, min_delta) for i in stock_indexes]
    # print arr
    return geometric_mean(arr)


# **MORE testing data and commands...**

# In[61]:


GBCE_stock_index(stock,tr, '360 min')


# In[62]:


trades


# In[63]:


tr2 = trades
tr2


# In[64]:


arr3 = [volume_weighted_stock_price(tr2 , stock_index, min_delta='360 min') for stock_index in stock_indexes]
arr3


# In[65]:


GBCE_stock_index(stock,tr2, '360 min')


# In[66]:


tr3 = trades
tr3 = add_trade(tr3, 'JOE', 300, 'sell', 8.)
tr3 = add_trade(tr3, 'JOE', 300, 'sell', 10.)
tr3 = add_trade(tr3, 'JOE', 300, 'sell', 12.)
tr3 = add_trade(tr3, 'GIN', 200, 'sell', 10.)
tr3 = add_trade(tr3, 'GIN', 200, 'sell', 20.)
tr3 = add_trade(tr3, 'GIN', 200, 'sell', 30.)
tr3 = add_trade(tr3, 'ALE', 300, 'sell', 20.)
tr3 = add_trade(tr3, 'ALE', 300, 'sell', 40.)
tr3 = add_trade(tr3, 'ALE', 300, 'sell', 60.)
tr3 = add_trade(tr3, 'TEA', 200, 'sell', 70.)
tr3 = add_trade(tr3, 'TEA', 200, 'sell', 80.)
tr3 = add_trade(tr3, 'TEA', 200, 'sell', 90.)
tr3 = add_trade(tr3, 'POP', 200, 'sell', 159.)
tr3 = add_trade(tr3, 'POP', 300, 'sell', 160.)
tr3 = add_trade(tr3, 'POP', 200, 'sell', 161.)
tr3


# In[67]:


volume_weighted_stock_price(tr3, 'XXX', '10 min')


# In[68]:


GBCE_stock_index(stock,tr3, '360 min')

