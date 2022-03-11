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

'''_key : the methods to encode and decode the patient information  
'''

import random
import datetime
import time
import numpy as np

from ..time import tconvert, to_timestamp, to_datetime

__author__ = 'Phil Jung <pjjung@amcg.kr>'
__all__ = ['encode', 'decode']

#---- main functions --------------------------------

def encode(patient_name, gender, birth_date, *args, **kwargs):
  '''encode patient name, gender, birth date information
  
  Parameters
  ----------
  patient_name : "str"
      patient's name
  
  gender : "str"
      patient's gender
  
  birth_date : "str"
      patient's bith date
  
  Raise
  -----
  ValueError
      1) if the input gender argument is no valid string, "man", "woman", "male", "female", 0, or 1
      2) if the input birth_data argument does not match to valid format, "%Y-%m-%d %H:%M:%S"
  
  Return : "tuple"
  ------
  fianlencoded name : "str"
      output of encoded information
  
  folder name : "str"
      output of encoded information with current date
  
  Examples
  --------
  >>> from mcgpy.key import encode
  >>> encode("phil", "male", "2222-02-22 22:22:22")
  ("a7576ae32B2566A8F16F", "a7F76ae32B2566A8F165_22221223'")
  '''
  
  #generate random number
  ramdom_number = int(15*random.random()) 
  ramdom_number2 = int(4*random.random()) 

  #determine gender code
  gender_code = _gender_checker(gender)

  #encode birth data information
  time_stamp = _birthdate_checker(birth_date)
  random_code = len(hex(time_stamp).split('0x')[-1]) - 6
  for n in range(ramdom_number2):
    random_code += 4
  encoded_time_stamp = hex(time_stamp).split('0x')[-1] + hex(random_code).split('0x')[-1]

  #encode patient name
  first_encoded_name = np.empty(0, dtype=str)
  for i, unsigned_byte in enumerate(bytearray(patient_name.encode('cp949'))):
    if i%2 == 0:
      hexadeciaml_string = hex(unsigned_byte + ramdom_number).split('0x')[-1]
      first_encoded_name = np.append(first_encoded_name, hexadeciaml_string)
    else:
      hexadeciaml_string = hex(unsigned_byte - ramdom_number).split('0x')[-1]
      first_encoded_name = np.append(first_encoded_name, hexadeciaml_string)

  for j, first_encoded_byte in enumerate(first_encoded_name):
    if j == 0:
      second_encoded_name_1 = first_encoded_byte[0]
      second_encoded_name_2 = first_encoded_byte[1]
    else:
      second_encoded_name_1 += first_encoded_byte[0]
      second_encoded_name_2 += first_encoded_byte[1]

  #get final patient information
  second_encoded_name = hex(ramdom_number).split('0x')[-1] + second_encoded_name_1 + second_encoded_name_2 + gender_code + encoded_time_stamp
  for k in range(len(second_encoded_name)): 
    if k == 0:
      if random.random() > 0.5:
        final_encoded_name = second_encoded_name[k].capitalize()
      else:
        final_encoded_name = second_encoded_name[k]
    else:
      if random.random() > 0.5:
        final_encoded_name += second_encoded_name[k].capitalize()
      else:
        final_encoded_name += second_encoded_name[k]

  #make folder name
  current_date_string = datetime.datetime.now().strftime('%Y%m%d')
  reference_index = 0
  for number in current_date_string:
    reference_index += int(number)
  reference_index = int(reference_index/(2+ramdom_number))
  if reference_index == 0:
    reference_index = 1

  encode_index = len(second_encoded_name) - reference_index
  encoded_folder_name1 = final_encoded_name[:reference_index+1] + final_encoded_name[encode_index] + final_encoded_name[reference_index+2:]
  encoded_folder_name2 = encoded_folder_name1[:encode_index] + final_encoded_name[reference_index+1] + encoded_folder_name1[encode_index+1:]

  folder_name = '{}_{}'.format(encoded_folder_name2, current_date_string)

  return final_encoded_name, folder_name

def decode(name, *args, **kwargs):
  '''decode an encoded string
  
  Parameters
  ----------
  name : "str"
      encoded string

  Raise
  -----
  NameError
      if the input string is no valid name
  
  Return : "dict"
  ------
  dict{"patient name" : decoded patient's name from an input string
       "gender" : decoded patient's gender from an input string
       "birth date" : decoded patient's birth date from an input string as "datetime.datetime" 
      }
  
  Examples
  --------
  >>> from mcgpy.key import decode
  >>> decode("a7576ae32B2566A8F16F")
  {'patient name': 'phil',
   'gender': 'Male',
   'birth date': datetime.datetime(2222, 2, 22, 22, 22, 22)}
  '''
  
  #get original encoded pattern from folder name
  if len(name.split('_')) == 2:
    encoded_folder_name, date_string = name.split('_')

    key = int(encoded_folder_name[0], 16)
    offset = len(encoded_folder_name)

    reference_index = 0
    for number in date_string:
      reference_index += int(number)
    reference_index = int(reference_index/(2+key))
    if reference_index == 0:
      reference_index = 1
    decode_index = len(encoded_folder_name) - reference_index
    decoded_pattern = encoded_folder_name[:reference_index+1] + encoded_folder_name[decode_index] + encoded_folder_name[reference_index+2:]
    original_pattern = decoded_pattern[:decode_index] + encoded_folder_name[reference_index+1] + decoded_pattern[decode_index+1:]

  elif len(name.split('_')) == 1:
    key = int(name[0], 16)
    offset = len(name)

    original_pattern = name

  else:
    raise NameError('Check the input string wheather or not it satisfies naming rules')

  #initial decoding process
  first_decoded_name = original_pattern[1:].lower()[::-1]
  decode_number = int(original_pattern[offset-1:], 16)%4 + 6

  #decode gender information
  if first_decoded_name[decode_number+1] == 'b':
    gender = 'Male'
  else:
    gender = 'Female'

  #decode birth date information
  second_decoded_name = first_decoded_name[:decode_number+1][::-1]
  birthdate_code = second_decoded_name[:decode_number][::-1]
  time_stamp = 0
  for n, code in enumerate(birthdate_code):
    time_stamp += 16**n * int(code, 16)
    
  labview_timestamp_rule = '1904-01-01 00:00:00'
  labview_timestamp = time.mktime(datetime.datetime.strptime(labview_timestamp_rule, '%Y-%m-%d %H:%M:%S').timetuple())
    
  birth_date = datetime.datetime.fromtimestamp(time_stamp+labview_timestamp)

  #decode patient name
  third_decoded_name = first_decoded_name[decode_number+1:][::-1]
  decode_number2 = int(len(third_decoded_name)/2)
  third_decoded_name_1 = third_decoded_name[:decode_number2]
  third_decoded_name_2 = third_decoded_name[decode_number2:]

  decoded_string = np.empty(0, dtype=np.int32)
  for m in range(decode_number2):
    decode_string = third_decoded_name_1[m] + third_decoded_name_2[m]
    if m%2 == 0:
      decoded_string = np.append(decoded_string, int(decode_string, 16) - key)
    else:
      decoded_string = np.append(decoded_string, int(decode_string, 16) + key)
  if np.any(decoded_string <= 20) == True:
    patient_name = ''
  else:
    patient_name = ''.join(map(chr,decoded_string)) #Here is some issues
    
  return {'patient name': patient_name, 'gender' : gender, 'birth date' : birth_date}

#---- inherent functions --------------------------------

def _gender_checker(value):
  _gender_str = ['man', 'woman', 'male', 'female']
  if (isinstance(value, str) 
      and value.lower() in _gender_str):
    if value == 'man' or value == 'male':
      return 'b'
    elif value == 'woman' or value == 'female':
      return 'a'
    else:
      raise ValueError('Value was no valid string. It must be the one of "man", "woman", "male", or "female"')
    
  elif (isinstance(value, int) and 0<= value <= 1):
    if value == 0:
      return 'b'
    elif value == 1:
      return 'a'
  else:
    raise ValueError('Value was no valid number. It must be 0 (male) or 1 (female)')
    
def _birthdate_checker(value):
  try:
    return int(to_datetime(float(value), ttype='labview'))
  except ValueError:
    try:
      return int(to_timestamp(value, ttype='labview'))
    except ValueError:
      raise ValueError('Value was no valid string. Datetime string must match format "%Y-%m-%d %H:%M:%S"')