# -*- coding: utf-8 -*-
class Interpolator:
    """Linear interpolator.
    """

    @staticmethod
    def interpolate(x_list: list, y_list: list, z: float):
        """Linear interpolate.
        Parameters
        __________
        x_list : list
            x values.
        y_list: list
            y values.
        z: float
            Interpolate in that point z.
        Returns
        _______
        float
            Interpolate value.
        Raises
        ______
        ValueError
            x_list must be sorted ASC.
        """
        if x_list != sorted(x_list):
            raise ValueError('x_list must be sorted ASC')
        for index, element in enumerate(x_list):
            if z <= element:
                delta = (z - x_list[index - 1]) / (x_list[index] - x_list[index - 1])
                answer = y_list[index - 1] + (y_list[index] - y_list[index - 1]) * delta
                break
        return answer

import pandas as pd
import numpy as np
import datetime
from dateutil.relativedelta import relativedelta

def get_date(date):
  if "D" in date:
    return relativedelta(days=int(date[:-1]))
  elif "W" in date:
    return relativedelta(weeks=int(date[:-1]))
  elif "M" in date:
    return relativedelta(months=int(date[:-1]))
  elif "Y" in date:
    return relativedelta(years=int(date[:-1]))
  return relativedelta()

class Curves:
  def __init__(self):
    self.load_data()

  def load_data(self,
                rub='/content/python-pricer/data/RUB swap points.csv',
                usd='/content/python-pricer/data/USD rates.csv',
                today=datetime.date.today()):
    self.rub = pd.read_csv(rub)
    self.usd = pd.read_csv(usd)
    self.usd.loc[0,'Conv, adj'] = self.usd.loc[0,'Unnamed: 1']

    self.today = today
    self.rub['date'] = pd.to_datetime(self.rub['Term'].apply(lambda x: get_date(x) + self.today))
    self.rub['date_sec'] = self.rub['date'].apply(lambda x: x.timestamp())
    self.rub['date_day'] = self.rub['Term'].apply(lambda x: get_date(x).days)
  
  def swop_point(self, date='12/15/21'):
    date = datetime.datetime.strptime(date, '%m/%d/%y')
    #return np.interp(date.timestamp(), self.rub['date_sec'], self.rub['SW POINTS'])
    return Interpolator.interpolate(list(self.rub['date_sec']), list(self.rub['SW POINTS']), date.timestamp())
  
  def discount_factor(self, date):
    return [(i, 1) for i in date]

  def swop_point_curve(self, date):
    return list(map(lambda x: (x, self.swop_point(x)), date))

rub = pd.read_csv('/content/python-pricer/data/RUB swap points.csv')
usd = pd.read_csv('/content/python-pricer/data/USD rates.csv')
usd.loc[0,'Conv, adj'] = usd.loc[0,'Unnamed: 1']

curve = Curves()
print(curve.swop_point_curve(usd['StartDate'].values))
print(curve.discount_factor(usd['StartDate'].values))