# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 23:20:29 2022

@author: AdrianSzałkowski
"""

from osgeo import gdal, ogr
import sys

ogr.UseExceptions()
file_name = input('Wprowadz sciezke do pliku .tif: ')
try:
    dem = gdal.Open(file_name)
except RuntimeError:
    sys.exit(f'Nie mozna otworzyc pliku \"{file_name}\".')

#dane z lewego gornego wierzcholka xmin & ymax
gt = dem.GetGeoTransform()

#koordynaty z lewego gornego rogu
xmin = gt[0]
ymax = gt[3]
resolution = gt[1]

#calkowita dlugosc rastra
xlen = resolution * dem.RasterXSize
ylen = resolution * dem.RasterYSize

#ilosc kolumn oraz wierszy z obsluga wyjatkow
while True:
    try:
        xtiles = int(input('Na ile kolumn ma byc dzielony plik? '))
        xtiles = abs(xtiles) # w razie wporwadzenia ujemnych liczb
        break
    except ValueError:
        print('Nieestety, mozesz wprowadzac jedynie dodatnie cyfry, wpisz ponownie')

while True:        
    try:
        ytiles = int(input('Na ile wierszy ma byc dzielony plik? '))
        ytiles = abs(ytiles)
        break
    except ValueError:
        print('Nieestety, mozesz wprowadzac jedynie dodatnie cyfry, wpisz ponownie')
        
output_name = input('Podaj nazwe wynikowa pliku: ')

#rozmiar pojedynczego kafla
xsize = xlen/xtiles
ysize = ylen/ytiles

#lista z koordynatami poszczegolnych kafelkow
xsteps = [xmin + xsize * i for i in range(xtiles+1)]
ysteps = [ymax - ysize * i for i in range(ytiles+1)]

#petla od minimum do maximum oraz koordynaty x oraz y
for i in range(xtiles):
    for j in range(ytiles):
        xmin = xsteps[i]
        xmax = xsteps[i+1]
        
        ymax = ysteps[j]
        ymin = ysteps[j+1]
        
        gdal.Translate(output_name+'_{:02d}_{:02d}'.format(i, j)+'.tif', dem, projWin = (xmin, ymax, xmax, ymin), xRes = resolution, yRes =-resolution)
print('\nOdszukaj pliki wynikowe w miejscu gdzie przechowujesz obecny plik.')
dem = None #zamkniecie danych
