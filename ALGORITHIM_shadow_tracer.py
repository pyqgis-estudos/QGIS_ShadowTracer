﻿# -*- coding: utf-8 -*-
"""
    /***************************************************************************
    ShadowTracer
                                    A QGIS plugin
    Desenho de sombra solar.

    Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                                -------------------
            begin                : 2020-05-05
            git sha              : $Format:%H$
            copyright            : (C) 2020 by Marcelo Baliu Fiamenghi
            email                : ma.baliu@gmail.com
    ***************************************************************************/

    /***************************************************************************
    *                                                                         *
    *   This program is free software; you can redistribute it and/or modify  *
    *   it under the terms of the GNU General Public License as published by  *
    *   the Free Software Foundation; either version 2 of the License, or     *
    *   (at your option) any later version.                                   *
    *                                                                         *
    ***************************************************************************/
"""
import numpy as np

from .TOOL_GeomDrawer import GeomDrawer

class sunShadow:
    """
    """
    # sunShadow(ds, azimuth=0, zenith=45, ref_dataset=None)

    def __init__(self, ds=None, azimuth=0, zenith=45, ref_dataset=None, floorLimit=0, cell_size=1):
        # print('Iniacializado')  ##LOGGER-inline
        self.shadow_angle = azimuth + 180
        self.zenith = zenith
        self.ds = ds  #Should be the shadowMap
        self.ds_shape = ref_dataset.shape
        self.ref_dataset = ref_dataset
        self.floorLimit = floorLimit
        self.cell_size = cell_size

    def createShadowDataset(self):
        """Create a blank dataset for the shadow"""

        height, weight = self.ds_shape
        self.shadowMap = np.zeros((height, weight))

    # def   (self, x, y):
    #     """Return the pixel's value from a given coordenates
    #     DESNECESSÁRIO"""

    #     value = self.ds[y, x]
    #     return value

    # def drawValidate(self, cX, cY, cValue):
    #     """Valida se o pixel possui um valor inferior ao valor que se deseja
    #     inserir. Caso contrário, reprovado a alteração do pixel

    #     - Valor superior ao de referencia
    #     cX, cY - current Coordenate
    #     DESNECESSÁRIO
    #     """
    #     if (self.shadowMap[cY, cX] > cValue):
    #         return False
    #     elif (self.ds[cY, cX] > cValue):
    #         return False
    #     else:
    #         return True


    def shadow(self):
        """[summary]

        Returns:
            [type] -- [description]
        """

        # print('Shadow inicializado')  ##LOGGER-inline
        def processor(main_dataset, ref_dataset=None):
            """Renderer of the shadow"""

            # print('processor inicializado')  ##LOGGER-inline
            y_axis, x_axis = self.ds_shape
            for yi in range(y_axis):
                # if (yi%10 == 0):  ##LOGGER-inline
                    # print("Calculating:", yi) ##LOGGER-inline
                for xi in range(x_axis):
                    # if (yi%10 == 0) and (xi%10 == 0):  ##LOGGER-inline
                        # print("Calculating:", yi, xi) ##LOGGER-inline


                    # GET HEIGHT VALUE
                    if (ref_dataset is None):
                        ref_value = main_dataset[yi, xi]
                    else:
                        ref_value = ref_dataset[yi, xi]

                    GeomDrawer.drawLine(ds=main_dataset,
                             value=ref_value,
                             x0=xi,
                             y0=yi,
                             angle=self.shadow_angle,
                             angZ=self.zenith,
                             cell_size=self.cell_size,
                             steps=10000, # OPTIMIZER - Advanced setup
                             log=False, # LOGGER
                             limits=self.floorLimit, # OPTIMIZER
                             method='bresenham',
                             firstPoint=False, lastPoint=True,
                             ref_ds=ref_dataset)


        self.createShadowDataset()  # Create the Shadow Map -> self.shadowMap
        # print('createShadowDataset OK!')  ##LOGGER-inline
        processor(main_dataset=self.shadowMap, ref_dataset=self.ref_dataset)
        # return self.shadowMap

    # sunShadow(ds= ,azimuth=-30, zenith=45)


    # -------------------------------------------------------------------------
    def _testDataset(self):
        size_y, size_x = (150, 250)
        city = np.zeros((size_y, size_x))
        # Buindings
        sx, sy = (21, 21)

        y1 = 120
        x, y = (10, y1)
        city[x:x+sx, y:y+sy] = 15
        x, y = (40, y1)
        city[x:x+sx, y:y+sy] = 21
        x, y = (85, y1)
        city[x:x+sx, y:y+sy] = 21
        x, y = (x+30, y1)
        city[x:x+sx, y:y+sy] = 15

        return city