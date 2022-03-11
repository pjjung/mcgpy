# -*- coding: utf-8 -*-
# Copyright (C) Phil Jung (2022)
#
# This file is part of MCGpy.
#
# MCGpy package consists of classes and methods for studying data from magnetocardiography (MCG) 
# and is designed for what users do not care how the code works, but utilize it 
# for instrumental or medical purposes as easy-to-use.
#
# MCGpy is following the GNU General Public License version 3. Under this term, you can redistribute and/or modify it.
# See the GNU free software license for more details.

'''_tconvert : convert from datetime/timestamp to timestamp/datetime
'''

import time
import datetime

__author__ = 'Phil Jung <pjjung@amcg.kr>'
__all__ = ['tconvert', 'to_timestamp', 'to_datetime']

#---- main functions --------------------------------

def tconvert(timeinput, ttype='python'):
  '''time converter
  
  Parameters
  ----------
  timeimput : "str", "int", "float"
      input value takes timestamp, datatime, or special string
         return related timestamp

  ttype : {"python", "labview"}, optional
      the standard of timestamp, default value is "python"
      1) in case of "python", timestamp will be calculated from "1970-01-01 09:00:00.000000"
      2) in case of "labveiw", timestamp will be calculated from "1904-01-01 00:00:00.000000"
      
  Raises
  ------
  ValueError
      input datetime forat is no "%Y-%m-%d %H:%M:%S.%f"
      
  Return
  ------
      1) if input is timestamp,
         return the datetime : "str"
      2) if input is datatime,
         return timestamp : "float"
      3) if input is special string; "now", "today", "tomorrow", or "yesterday",
         return related timestamp : "float"
         
  Examples
  --------
  >>> from mcgpy.time import tconvert
  >>> tconvert(0)
  "1970-01-01 09:00:00.000000"
  >>> tconvert(0, ttype="labview")
  "1904-01-01 00:00:00.000000"
  >>> tconvert("1970-01-01 09:00:00.000000", ttype="labview")
  2082875272.0
  '''
  
  try:
    float(timeinput)    # if input value can be float, it is probably timestamp
    return to_datetime(timeinput, ttype)
  except (TypeError, ValueError):    # if it is not, we ought to covert diverse datetime formats to timestamp
    if timeinput in ['now', 'today', 'tomorrow', 'yesterday']:
      return  _to_special_timestamp(timeinput, ttype)
    else:
      return to_timestamp(timeinput, ttype)

def to_timestamp(timeinput, ttype='python', *args, **kwargs):
  '''converto datetime to timestamp
  
  Parameters
  ----------
  timeinput : "str"
      input value takes "%Y-%m-%d %H:%M:%S.%f" style datetime string,
     
  ttype : {"python", "labview"}, optional
      the standard of timestamp, default value is "python"
      1) in case of "python", timestamp will be calculated from "1970-01-01 09:00:00.000000"
      2) in case of "labveiw", timestamp will be calculated from "1904-01-01 00:00:00.000000"
      
  Raises
  ------
  ValueError
      input datetime format is no "%Y-%m-%d %H:%M:%S.%f"
  
  Return : "float"
  ------
     1) timestamp
     2) if "int" or"float" value is inserted, return input value
  
  Examples
  --------
  >>> from mcgpy.time import to_timestamp
  >>> to_timestamp("2000-01-01 00:00:00")
  946652400.0
  '''
  
  # str to datetime.datetime
  if isinstance(timeinput, str):
    try:
      float(timeinput)
    except ValueError:    # it might be datetime string, like 2000-01-01 00:00:00
      try:
        timeinput = _string2time(timeinput)
      except ValueError:
        timeinput = _string2time(timeinput)
  elif isinstance(timeinput, (int, float)):
    return timeinput

  # convert from datetime.datetime to timestamp
  if ttype == 'python':
    timeinput = time.mktime(timeinput.timetuple())
    return timeinput
  
  elif ttype == 'labview':
    labview_timestamp_rule = _string2time('1904-01-01 00:00:00')
    labview_timestamp = _datetime2timestamp(labview_timestamp_rule)
    timeinput = time.mktime(timeinput.timetuple()) - labview_timestamp
    return timeinput
  
def to_datetime(timeinput, ttype='python', *args, **kwargs):
  '''convert from timestamp to datetime
  
  Parameters
  ----------
  timeinput : "int", "float"
      the value of timestamp
     
  ttype : {"python", "labview"}, optional
      the standard of timestamp, default value is "python"
      1) in case of "python", timestamp will be calculated from "1970-01-01 09:00:00.000000"
      2) in case of "labveiw", timestamp will be calculated from "1904-01-01 00:00:00.000000"
      
  Return : "str"
  ------
     datetime string as "%Y-%m-%d %H:%M:%S.%f"
  
  Examples
  --------
  >>> from mcgpy.time import to_datetime
  >>> to_timestamp(0)
  1970-01-01 09:00:00.000000
  '''

  if ttype == 'python':
    dateoutput = datetime.datetime.fromtimestamp(timeinput).strftime('%Y-%m-%d %H:%M:%S.%f')
  elif ttype == 'labview':
    labview_timestamp_rule = _string2time('1904-01-01 00:00:00')
    labview_timestamp = _datetime2timestamp(labview_timestamp_rule)
    dateoutput = _datetime2string(timeinput+labview_timestamp)
    
  return dateoutput


#---- inherent functions --------------------------------

def _to_special_timestamp(date_string, ttype='python'):
  ## get special cases of timestamps
  if date_string == 'now':
    output = datetime.datetime.utcnow()
    
  elif date_string == 'today':
    output = datetime.datetime.today()
    
  elif date_string == 'tomorrow':
    output = datetime.datetime.today() + datetime.timedelta(days=1)
    
  elif date_string == 'yesterday':
    output = datetime.datetime.today() + datetime.timedelta(days=-1)
  
  ## convert from datetime.datetime to timestamp
  if ttype == 'python':
    return time.mktime(output.timetuple())
  
  elif ttype == 'labview':
    labview_timestamp_rule = _string2time('1904-01-01 00:00:00')
    labview_timestamp = _datetime2timestamp(labview_timestamp_rule)
    return time.mktime(output.timetuple()) - labview_timestamp

def _string2time(datestring):
  try:
    datetime_out = datetime.datetime.strptime(datestring, '%Y-%m-%d %H:%M:%S.%f')
  except ValueError:
    datetime_out = datetime.datetime.strptime(datestring, '%Y-%m-%d %H:%M:%S') 

  return datetime_out

def _datetime2timestamp(dateinput):
  return time.mktime(dateinput.timetuple())

def _datetime2string(dateinput):
  return datetime.datetime.fromtimestamp(dateinput).strftime('%Y-%m-%d %H:%M:%S.%f')