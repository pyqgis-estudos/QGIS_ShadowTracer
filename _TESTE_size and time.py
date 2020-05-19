from osgeo import gdal, osr
import numpy as np
import math # tan() -> Tangente só aceita radianos
from time import time
from sys import getsizeof

from osgeo import gdal

"""IN QGIS
"""

r_later = iface.activeLayer()

TIME_init = time()
provider = r_later.dataProvider()
TIME_prov = time()
print(TIME_prov - TIME_init)

driver = gdal.Open(str(provider.dataSourceUri()), gdal.GA_Update)
TIME_driver = time()
print(TIME_driver - TIME_prov)

raster = driver.GetRasterBand(1).ReadAsArray()
TIME_raster = time()
print(TIME_raster - TIME_driver)

print(getsizeof(provider),  getsizeof(driver), getsizeof(raster))

"""
PROVIDER from QgsLayer: relativo pequeno, instanteneo
DRIVER: Muito pequeno espaço, menos tempo que o provider
RASTER: Muito ESPAÇO, e tempo menor do que o Driver
"""