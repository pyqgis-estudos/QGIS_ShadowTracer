# -*- coding: utf-8 -*-
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
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QFileDialog
from qgis.core import QgsProject, QgsRasterLayer
from osgeo import gdal, ogr, gdalconst

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .shadow_tracer_dialog import ShadowTracerDialog
import os.path

from .ALGORITHIM_shadow_tracer import sunShadow


class ShadowTracer:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'ShadowTracer_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Shadow Tracer')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('ShadowTracer', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/shadow_tracer/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Shadow Tracer'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True
        self.dlg = ShadowTracerDialog()  #TODO: This is not recommended

        self.dlg.azim_spin.valueChanged.connect(self.onSpinChange)
        self.dlg.azim_dial.valueChanged['int'].connect(self.onDialChange)
        self.dlg.outputFolderToolButton.clicked.connect(self.setOutPath)

    def setOutPath(self):
        """Function to select the output folder and update the LineEdit
        """
        # outPath = QFileDialog.getExistingDirectory(self.dlg,
        #         caption="Select the output folder",
        #         directory=self.dlg.outputFolderToolButton.text())
        outPath, _ = QFileDialog.getSaveFileName(self.dlg,
                caption="Select the output folder",
                directory=self.dlg.outputFolderToolButton.text(),
                filter="GTiff (*.tif)")
        if outPath:
            self.dlg.outputFolderLineEdit.setText(outPath)

    #     ---- QDialog Signs----
    def correctDial(self, dialValue):
        """Factor to correct the Dial position, to convert the dial value
        to spin value"""
        if dialValue < 180:
            return 1
        elif dialValue >= 180:
            return -1

    def onSpinChange(self, v):
        """Trigger when changed teh spin"""
        DialValue = self.dlg.azim_dial.value()
        v = int(round(v))
        f = self.correctDial(v)
        if int(v+(180*f)) != int(DialValue):
            self.dlg.azim_dial.setValue(v+(180*f))
    def onDialChange(self, v):
        f = self.correctDial(v)
        if int(v+(180*f)) != int(self.dlg.azim_spin.value()):
            self.dlg.azim_spin.setValue(float(v+(180*f)))



    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Shadow Tracer'),
                action)
            self.iface.removeToolBarIcon(action)


    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            # self.dlg = ShadowTracerDialog()

        # ELEVATION LAYER COMBOBOX
        layers_registry = QgsProject.instance().mapLayers().values()
        self.dlg.combo_elevation.clear()
        for l in layers_registry:
            if isinstance(l, QgsRasterLayer):  # Filter in RASTER Layers
                self.dlg.combo_elevation.addItem(l.name(), l)
        # Mark the active layer
        currentLayer = self.iface.activeLayer()
        idx = self.dlg.combo_elevation.findData(currentLayer)
        if idx >= 0:
            self.dlg.combo_elevation.setCurrentIndex(idx)


        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:

            #     ---- 1. SETUP VARIABLES ----
            # FLOOR LIMIT
            if self.dlg.checkBox_floorLimit.isChecked():
                floor_limit = self.dlg.spin_floor.value()
            else:
                floor_limit = None
            # AZIMUTH
            azimuth_input = self.dlg.azim_spin.value()
            # ZENITH
            zenith_input = self.dlg.z_spin.value()
            # OUTPUT
            output_input = self.dlg.outputFolderLineEdit.text()
            # MODEL LAYER
            # elevation_layer = self.dlg.mMapLayerCombo.currentLayer()  #TODO: More appropriated, but has bug.
            elevation_layer = self.dlg.combo_elevation.currentData()

            #      ---- 1.2. GDAL VARIABLES ----
            # ELEVATION OBJECTS
            def Raster2Array(modelLayer):
                """Function to unload the memory after read the file"""
                provider = modelLayer.dataProvider()
                driver = gdal.Open(str(provider.dataSourceUri()), gdal.GA_Update)
                np_array = driver.GetRasterBand(1).ReadAsArray()

                geot = driver.GetGeoTransform()
                srs_WKT = driver.GetProjectionRef()
                rX = driver.RasterXSize
                rY = driver.RasterYSize
                return (np_array, rX, rY, geot, srs_WKT)

            Ref_array, rX, rY, geot, srs_WKT = Raster2Array(elevation_layer)

            # OUTPUT FILE
            """GetDriver - copiar driver?
            CopyLayer
            .GetGeoTransform()
            .GetProjectionRef()
            'RasterXSize', 'RasterYSize'
            """
            ds_output = gdal.GetDriverByName('GTiff').Create(
                        output_input,
                        xsize=rX,
                        ysize=rY,
                        bands=1,
                        eType=gdal.GDT_Float32)
                        # eType=gdalconst.GDT_Byte)

            ds_output.SetGeoTransform(geot)
            ds_output.SetProjection(srs_WKT)



            #     ---- 2. INSTANCE ----
            # """Create the instance for the processing"""
            print(abs(geot[1]))
            tracer = sunShadow(azimuth=azimuth_input,
                               zenith=zenith_input,
                               ref_dataset=Ref_array,
                               floorLimit=floor_limit,
                               cell_size=abs(geot[1]))

            #     ---- 3. EXECUTION ----
            # """Generate the shadows"""
            tracer.shadow()

            #     ---- 4. OUTPUT ----
            # """Save the shadows"""
            ds_output.GetRasterBand(1).WriteArray(tracer.shadowMap)
            ds_output = None

            rlayer = self.iface.addRasterLayer(output_input)

            # SHADER
            # shadeFile = ("styles", "shading_0-6m.qml")
            shadeFile = os.path.dirname(__file__) + "styles/shading_0-6m.qml"
            rlayer.loadNamedStyle(path)
            rlayer.triggerRepaint()
