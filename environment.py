import gym
from gym import spaces
import numpy as np

class StockEnvironment(gym.Env):
  """
  Environment that the models interact with

  Acroynyms: 
    sma-20: 20 day simple moving average
    sma-50: 50 day simple moving average
    sma-200: 200 day simple moving average
    macd: moving average convergence divergence
    rsi: relative strength index
    cci: commodity channel index

  State space: (balance, shares, sma-20, sma-50, sma-200, macd, rsi, cci)
  
  Action space: There are 9 discrete actions choices, which slightly differ 
  between the two models and each of them result in some fraction of currently
  held stock being sold or a fraction of the balance used to buy stock rounded
  down to the nearest integer

  Starting day is 200 to allow for sma-200 to have an actual value
  """
  def __init__(self, data_dict, indicators, stopping_day=1200, model='DQN'):
    super(StockEnvironment, self).__init__()

    self.balance = 100
    self.shares = 0
    self.day = 200
    self.stopping_day = stopping_day
    
    self.action_space = spaces.Discrete(9)
    self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(8,))

    self.indicators = indicators
    self.data = data_dict
    self.terminal = False

    if model == 'DQN':
      self.mapping = {0: -1, 1: -.5, 2:-.25, 3: -.1, 4: 0, 5: .1, 6: .25, 7: .5, 8: 1}
    else:
      self.mapping = {0: -.75, 1: -.5, 2:-.25, 3: -.1, 4: 0, 5: .1, 6: .25, 7: .5, 8: .75}
  
  def step(self, action_num):
    price = self.data['Close'][self.day]
    old_value = price * self.shares + self.balance

    if self.day == self.stopping_day:
      self.terminal = True

    action = self.mapping[action_num]

    if action > 0:
      ## buy stocks
      num_stocks = int((action * self.balance) / price)
      self.balance -= num_stocks * price
      self.shares += num_stocks
    else:
      ## sell stocks
      num_stocks = -int(action * self.shares)
      self.balance += num_stocks * price
      self.shares -= num_stocks

    self.day += 1
    
    new_price = self.data['Close'][self.day]
    new_value = new_price * self.shares + self.balance
    state = np.array([self.balance] + \
            [self.shares] + \
            [self.indicators['sma_20'][self.day]] + \
            [self.indicators['sma_50'][self.day]] + \
            [self.indicators['sma_200'][self.day]] + \
            [self.indicators['macd'][self.day]] + \
            [self.indicators['rsi'][self.day]] + \
            [self.indicators['cci'][self.day]])
    
    
    if self.balance < 0:
      raise Exception('negative balance not allowed', action, self.balance, self.shares, price)

    return state, new_value - old_value, self.terminal, {}
  
  def reset(self):
    self.balance = 100
    self.shares = 0
    self.day = 200
    self.terminal = False
    state = np.array([self.balance] + \
            [self.shares] + \
            [self.indicators['sma_20'][self.day]] + \
            [self.indicators['sma_50'][self.day]] + \
            [self.indicators['sma_200'][self.day]] + \
            [self.indicators['macd'][self.day]] + \
            [self.indicators['rsi'][self.day]] + \
            [self.indicators['cci'][self.day]])
    
    return state
  
  def render(self, mode='human', close=False):
    print('Day Number: ', self.day)
    print('Balance: ', self.balance)
    print('Shares: ', self.shares)
    print('Portfolio total value: ', self.balance + self.shares * self.data['Close'][self.day])
    print()