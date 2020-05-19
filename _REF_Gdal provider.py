
#    CREATING A RASTER DATASET
# Setup Dataset Raster's Features 
gt = dict(
        X0_Coord = 500000,
        Y0_Coord = 4600000,
        X_cellSize = 10,
        Y_cellSize = -10, # Negative to ZERO:Up left (like Numpy) | Positive - ZERO:Down left
        Y_Shering = 0,
        X_Shering = 0
        )

# Order the transform setup to input
geot = [gt['X0_Coord'], # X-Coord
        gt['X_cellSize'], # X-cellSize
        gt['Y_Shering'], # Y-Shering
        gt['Y0_Coord'], # Y-Coord
        gt['X_Shering'], # X-Shering
        gt['Y_cellSize'] # Y-cellSize
        ] # Georreferenciamento


driver = gdal.GetDriverByName('GTiff')
ds = driver.Create(fn_output, # Outfile
                    xsize=250, 
                    ysize=150, 
                    bands=1, 
                    eType=gdal.GDT_Float32)
ds.GetRasterBand(1).WriteArray(rasterband) # raster's Writer 
ds.SetGeoTransform(geot)

# Setup the CRS - Coordinate Reference System | SRS - Spatial Reference System | Projection
srs = osr.SpatialReference()
srs.ImportFromEPSG(31983) # SIRGAS-2000 UTM 23S
ds.SetProjection(srs.ExportToWkt())

# Cleaning memory
ds = None # Close the GDAL dataset



rlayer = iface.addRasterLayer(fn_output) # Load in QGIS