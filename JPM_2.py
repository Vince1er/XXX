
# coding: utf-8

# In[1]:


get_ipython().magic(u'pwd')


# I chose to use Python/Pandas/Numpy for this test.

# In[2]:


import pandas as pd
import numpy as np


# Definition of sample set of data. The same as defined in the spreadsheet.

# In[3]:


stock = pd.DataFrame()


# In[4]:


data = {'TEA': ['Common', 0., np.nan, 100.],
         'POP':['Common', 8., np.nan, 100.],
         'ALE':['Common', 23., np.nan, 60.],
        'GIN': ['Preferred', 8., 2., 100.],
        'JOE': ['Common', 13., np.nan,250.]
        }


# In[5]:


data


# In[6]:


stock = pd.DataFrame.from_dict(data, orient='index')


# In[7]:


stock


# In[8]:


stock.columns = ['Type','LastDiv','FixedDiv','ParV']


# In[9]:


stock


# Above is a Pandas frame with the data

# In[10]:


stock.loc['JOE']


# In[11]:


market_price = 12.00


# In[12]:


stock.loc['JOE']['LastDiv']/market_price


# Below a first version of the computation of the dividend yield. It does note take yet into
# account the "preferred" shares.

# In[13]:


def dividend_yield_0(stock_index, market_price=None):
    dy = (stock.loc[stock_index]['LastDiv'])/market_price
    return dy


# In[14]:


dividend_yield_0('JOE',12.)


# In[15]:


dividend_yield_0('JOE',60.)


# This is the definitive version of the function computing the dividend yield.
# I suppose that the stock_index exists in the stock and corresponds to a unique row.
# (I.e. stock_index is a key). 

# **1.a.i** This is the definitive version of the function computing the dividend yield. I suppose that the stock_index exists in the stock and corresponds to a unique row. (I.e. stock_index is a key). 

# In[16]:


def dividend_yield(stock_index, market_price):
    st = stock.loc[stock_index]
    if st['Type'] == 'Preferred':
        return (st['FixedDiv']/100.)*st['ParV']/market_price
    return st['LastDiv']/market_price 


# In[17]:


dividend_yield('JOE',13.)


# In[18]:


dividend_yield('GIN',100.)


# **1.a.ii.** I understand from the given definitions that the P/E ratio is just
# **the inverse of the dividend yield**. Below is the function computing the P/E ratio.

# In[19]:


def price_earnings_ratio(stock_index, market_price):
    return 1/dividend_yield(stock_index, market_price)


# In[20]:


price_earnings_ratio('JOE',13.)


# In[21]:


price_earnings_ratio('GIN',100.)


# For the next question, I define an array (a "Pandas Frame") storing the trade records.

# In[22]:


trades = pd.DataFrame(columns = ['date','stock_index','qty','buy/sell','price'])


# In[26]:


trades


# In[23]:


trades.append({'date':'15-02-18', 'stock_index':'JOE','qty':100, 
                   'buy/sell':'sell', 'price':250.},ignore_index=True)


# In[24]:


tr = trades.append({'date':'15-03-18', 'stock_index':'GIN','qty':300, 
                   'buy/sell':'buy', 'price':30.},ignore_index=True)


# In[25]:


tr = tr.append({'date':'15-02-18', 'stock_index':'JOE','qty':100, 
                   'buy/sell':'sell', 'price':250.},ignore_index=True)


# In[26]:


tr


# A first version of the function adding a trade record to the trade list.
# Actually I should have coded an object and this function should be 
# a modifier for this object. It is not the case here. The array of data
# is just a Pandas Frame.

# In[27]:


def add_trade_0(t, date, stock_index, qty, bs_ind, price):
    t = t.append({'date':date, 'stock_index':stock_index,'qty':qty, 
                   'buy/sell':bs_ind, 'price':price},ignore_index=True)
    return t


# In[28]:


tr = add_trade_0(tr, '15-02-18', 'JOE', 100, 'sell', 250.)


# In[29]:


tr


# In[30]:


pd.Timestamp.now()


# In[31]:


pd.Timestamp(year=2017, month=1, day=1, hour=12, minute=59, second=3)


# This is a second version of the function adding trade records into the list. 
# Now the date entered should be of the type pd.Timestamp. 
# If the argument date is not given to the function then the date is set by default
# to the current date.

# In[32]:


tr = trades


# In[33]:


tr


# In[34]:


def add_trade(t, stock_index, qty, bs_ind, price, date=None):
    if (date == None):
        date = pd.Timestamp.now()
    t = t.append({'date':date, 'stock_index':stock_index,'qty':qty, 
                   'buy/sell':bs_ind, 'price':price},ignore_index=True)
    return t


# In[35]:


tr = add_trade(tr, 'JOE', 100, 'sell', 250.)


# In[36]:


tr = add_trade(tr, 'JOE', 100, 'sell', 250.)
tr = add_trade(tr, 'JOE', 100, 'buy', 250.)
tr = add_trade(tr, 'GIN', 200, 'buy', 50.)
tr = add_trade(tr, 'ALE', 200, 'buy', 150.)


# In[37]:


tr


# In[38]:


tr = add_trade(tr, 'ALE', 200, 'sell', 150., 
               pd.Timestamp(year=2017, month=1, day=1, hour=12, minute=59, second=3))


# In[39]:


tr = add_trade(tr, 'ALE', 150, 'sell', 50.)
tr = add_trade(tr, 'ALE', 300, 'sell', 100.)


# In[40]:


tr


# For question 1.iv the stock has to be in the trade list of trades not older 
# than 15 minutes.

# In[41]:


time_now = pd.Timestamp.now()


# In[42]:


min_delta = '360 min'


# In[43]:


time_delta = pd.Timedelta(min_delta)


# In[44]:


time_delta


# In[45]:


tr.date


# In[46]:


lt_recent= tr[( time_now - tr.date < time_delta ) & (tr.stock_index == 'JOE')]


# In[47]:


lt_recent


# **1.a.iv.** The function computing the Volume Weighted Stock Price. It takes as arguments the trading list tr_l (a Pandas Frame as defined above), the stock index, a parameter of the time delay for considering trades in the list, by default: 15 minutes.

# In[74]:


def  volume_weighted_stock_price(tr_l , stock, min_delta='15 min'):
    time_now = pd.Timestamp.now()
    # print time_now
    time_delta = pd.Timedelta(min_delta)
    # print time_delta
    t_rec = tr_l[(time_now - tr_l.date < time_delta) & (tr_l.stock_index == stock)]
    # print t_rec
    if t_rec.empty:
        #print 'zero'
        return np.nan
    num = (t_rec['price']*t_rec['qty']).sum()
    #print num
    den = t_rec['qty'].sum()
    #print den
    if den == 0:
        #print 'denominator null'
        return np.nan
    vwsp = num/den
    return vwsp


# In[49]:


volume_weighted_stock_price(tr , 'JOE')


# In[50]:


volume_weighted_stock_price(tr , 'JOE', min_delta='360 min')


# In[51]:


volume_weighted_stock_price(tr , 'ALE', min_delta='360 min')


# **Question b.**

# For the geometric average I did the average of the logarithms and applied 
# the exponentiation. 
# If the number of values in the list is 0 the value returned is 1. 
# Values should be strictly positive.

# In[52]:


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


# In[53]:


geometric_mean([1])


# In[54]:


geometric_mean([])


# In[55]:


geometric_mean([1,2])


# In[227]:


geometric_mean([1,2,4])


# In[56]:


geometric_mean([34., 56., 76., 23., 45., 22.,67.])


# I am not sure that I understand question b. and the definition of the GBCE All Share Index.

# I can simply compute the geometric means of all stocks (their prices being
# given by a.iv.). But I admit that this figure does make much sense to me.                                                        

# **I am not sure that I understand question b. and the definition of the GBCE All Share Index.**
# I can simply compute the geometric means of all stocks (their prices being given by a.iv.). 
# But I admit that this figure does make much sense to me.

# In[66]:


stock.index


# In[72]:


stock_indexes = stock.index.values


# In[78]:


stock_indexes


# In[76]:


arr2 = [volume_weighted_stock_price(tr , stock_index, min_delta='360 min') for stock_index in stock_indexes]


# In[77]:


geometric_mean(arr2)


# In[79]:


tr = add_trade(tr, 'GIN', 200, 'sell', 75.)
tr = add_trade(tr, 'TEA', 300, 'sell', 125.)
tr = add_trade(tr, 'POP', 300, 'sell', 300.)


# In[80]:


tr


# A function computing the geometric mean of all stock prices...

# In[84]:


def GBCE(stock_list,trade_list):
    stock_indexes = stock_list.index.values
    arr = [volume_weighted_stock_price(trade_list , i, min_delta='360 min') for i in stock_indexes]
    return geometric_mean(arr)


# In[85]:


GBCE(stock,tr)

