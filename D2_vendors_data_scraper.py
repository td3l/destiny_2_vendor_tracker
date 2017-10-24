#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 15:27:48 2017

@author: tom.delaubenfels@gmail.com
"""


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from html.parser import HTMLParser
from urllib.request import urlopen

url = "http://destiny-vendor-gear-tracker.com/logs" # The URL in question
html = urlopen(url)
htmlstr = html.read().decode(html.headers.get_content_charset())


# Parser for getting time stamps out of the html data
class Get_Timestamps(HTMLParser):  
    
    # init variables
    timestamps = []
    is_timestamp = False   
    
    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if attr[0] == 'colspan':  self.is_timestamp = True
            else: self.is_timestamp = False 
           
    def handle_data(self, data):
        if self.is_timestamp == True: self.timestamps.append(data)     

# Return the current time stamp data from the URL 
ts = Get_Timestamps()
ts.feed(htmlstr)
timestamps = ts.timestamps[::2]  # ts.timestamps returns \n on every other entry   


# Parser to create value lists for each vendor containing 0 or 1, 
# depending on their condition at each time stamp.
# Each vendor appears, consecutively, once per time stamp, although some will not
# appear for all time stamps.

class Fill_Vendor_Data(HTMLParser):

    # List of vendor names per the HTML file
    vendor_names = ['Lakshmi-2', 'Executor Hideo', 'Zavala', 'Shaxx', 'Devrim (MIDA Mini-Tool)', 
             'Asher Mir (Man O\'War)', 'Tyra Karn (Drang)', 'Devrim Kay', 
             'Sloane', 'Failsafe', 'Asher Mir', 'Ikora Rey', 'Benedict 99-40',
             'Arach Jalaal', 'Banshee-44']       
    
    # Init empty value lists for each vendor
    lakshmi_vals = []
    exe_hideo_vals = []
    zavala_vals = []
    shaxx_vals = []
    devrim_mida_vals = []
    asher_mow_vals = []
    devrim_vals = []
    tyra_karn_drang_vals = []
    sloane_vals = []
    failsafe_vals = []
    asher_vals = []
    ikora_vals = []
    benedict_vals = []
    arach_vals = []
    banshee_vals = []

    
    # Link the vendor's HTML text name to its respective list
    dict = {
            'Lakshmi-2': lakshmi_vals, 
            'Executor Hideo': exe_hideo_vals, 
            'Zavala': zavala_vals, 
            'Shaxx': shaxx_vals, 
            'Devrim (MIDA Mini-Tool)': devrim_mida_vals,
            'Asher Mir (Man O\'War)': asher_mow_vals, 
            'Tyra Karn (Drang)': tyra_karn_drang_vals, 
            'Devrim Kay': devrim_vals, 
            'Sloane': sloane_vals, 
            'Failsafe': failsafe_vals, 
            'Asher Mir': asher_vals, 
            'Ikora Rey': ikora_vals, 
            'Benedict 99-40': benedict_vals,
            'Arach Jalaal': arach_vals, 
            'Banshee-44': banshee_vals
            }
       
    # init variables
    is_300 = False   
    ts_count = 0
    
    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if tag=='tr' and attr[1] == 'bg-success':  self.is_300 = True
            if attr[0] == 'colspan':  self.ts_count += 1    
    
    def handle_data(self, data):
        for name in self.vendor_names:
            if data == name and self.is_300: self.dict[name].append(1)
            elif data == name: self.dict[name].append(0)
            
    def handle_endtag(self, tag):
        if tag=='tr':  self.is_300 = False      
    
    # extend all vendor lists above to the length of the total # of 
    # time stamp values, appending empty values with -1
        

# Send html data to the vendor data parser
vendor_data = Fill_Vendor_Data()
vendor_data.feed(htmlstr)

# Extract data lists
lakshmi_vals = vendor_data.lakshmi_vals
exe_hideo_vals = vendor_data.exe_hideo_vals
zavala_vals = vendor_data.zavala_vals
shaxx_vals = vendor_data.shaxx_vals
devrim_mida_vals = vendor_data.devrim_mida_vals
asher_mow_vals = vendor_data.asher_mow_vals
devrim_vals = vendor_data.devrim_vals
tyra_karn_drang_vals = vendor_data.tyra_karn_drang_vals
sloane_vals = vendor_data.sloane_vals
failsafe_vals = vendor_data.failsafe_vals
asher_vals = vendor_data.asher_vals
ikora_vals = vendor_data.ikora_vals
benedict_vals = vendor_data.benedict_vals
arach_vals = vendor_data.arach_vals
banshee_vals = vendor_data.banshee_vals


# Extend all list lengths to # of time stamps, appending with -1's:

tslen = len(timestamps)

arach_vals.extend([-1] * (tslen - len(arach_vals)))
banshee_vals.extend([-1] * (tslen - len(banshee_vals)))
benedict_vals.extend([-1] * (tslen - len(benedict_vals)))
ikora_vals.extend([-1] * (tslen - len(ikora_vals)))
asher_vals.extend([-1] * (tslen - len(asher_vals)))
lakshmi_vals.extend([-1] * (tslen - len(lakshmi_vals))  )
exe_hideo_vals.extend([-1] * (tslen - len(exe_hideo_vals)))
zavala_vals.extend([-1] * (tslen - len(zavala_vals)))
shaxx_vals.extend([-1] * (tslen - len(shaxx_vals)))
devrim_mida_vals.extend([-1] * (tslen - len(devrim_mida_vals)))
asher_mow_vals.extend([-1] * (tslen - len(asher_mow_vals)))
devrim_vals.extend([-1] * (tslen - len(devrim_vals)))
tyra_karn_drang_vals.extend([-1] * (tslen - len(tyra_karn_drang_vals)))
sloane_vals.extend([-1] * (tslen - len(sloane_vals)))
failsafe_vals.extend([-1] * (tslen - len(failsafe_vals)))


# Initialize data frames for each of the 15 vendors.
# Target value of interest is 'Is 300', which will ultimately be 0 or 1
# at each time stamp.
# If there's no data for a vendor at a given timestamp, 'Is 300' = -1.

Lakshmi_2 = pd.DataFrame({'Time Stamp': timestamps, 'Is 300': lakshmi_vals})
Executor_Hideo = pd.DataFrame({'Time Stamp': timestamps, 'Is 300': exe_hideo_vals})
Zavala = pd.DataFrame({'Time Stamp': timestamps, 'Is 300': zavala_vals})
Shaxx = pd.DataFrame({'Time Stamp': timestamps, 'Is 300': shaxx_vals})
Devrim_MIDA = pd.DataFrame({'Time Stamp': timestamps, 'Is 300': devrim_mida_vals})
Asher_Mir_MOW = pd.DataFrame({'Time Stamp': timestamps, 'Is 300': asher_mow_vals})
Tyra_Karn_Drang = pd.DataFrame({'Time Stamp': timestamps, 'Is 300': tyra_karn_drang_vals})
Devrim_Kay = pd.DataFrame({'Time Stamp': timestamps, 'Is 300': devrim_vals})
Sloane = pd.DataFrame({'Time Stamp': timestamps, 'Is 300': sloane_vals})
Failsafe = pd.DataFrame({'Time Stamp': timestamps, 'Is 300': failsafe_vals})
Asher_Mir = pd.DataFrame({'Time Stamp': timestamps, 'Is 300': asher_vals})
Ikora_Rey = pd.DataFrame({'Time Stamp': timestamps, 'Is 300': ikora_vals})
Benedict_9940 = pd.DataFrame({'Time Stamp': timestamps, 'Is 300': benedict_vals})
Arach_Jalaal = pd.DataFrame({'Time Stamp': timestamps, 'Is 300': arach_vals})
Banshee_44 = pd.DataFrame({'Time Stamp': timestamps, 'Is 300': banshee_vals})

