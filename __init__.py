# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ShadowTracer
                                 A QGIS plugin
 Desenho de sombra solar.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2020-05-05
        copyright            : (C) 2020 by Marcelo Baliu Fiamenghi
        email                : ma.baliu@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load ShadowTracer class from file ShadowTracer.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .shadow_tracer import ShadowTracer
    return ShadowTracer(iface)
