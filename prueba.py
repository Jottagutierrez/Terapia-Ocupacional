import xlrd
from xlrd import open_workbook

import openpyxl
import googlemaps
import simplejson
import json

api_key='AIzaSyA6y7X_-xTRUTV8FWl5vO-aVEBrxz6vT_4'
gmaps = googlemaps.Client(key=api_key)

book = xlrd.open_workbook("centros.xlsx")
sheet = book.sheet_by_index(0) 

origins = []


for row in range(0, 43): #start from 1, to leave out row 0
    origins.append(sheet.cell(row, 3))

 print(origins)

my_distance = gmaps.distance_matrix(origins,origins)

print (my_distance)