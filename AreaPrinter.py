# -*- coding: utf-8 -*-
"""
/***************************************************************************
 AreaPrinter
                                 A QGIS plugin
 AreaPrinter
                              -------------------
        begin                : 2017-06-18
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Fredrik Bakke
        email                : bakkefredrik@gmail.com
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
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon

from qgis.core import *
from qgis.gui import *

# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from AreaPrinter_dialog import AreaPrinterDialog
import os.path


class AreaPrinter:
    """QGIS Plugin Implementation."""
    initialized = 0
    extents = list()
    overlap = 0.1 #value*100 = %overlap
    layer = QgsVectorLayer
    pr = QgsVectorDataProvider
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
            'AreaPrinter_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&AreaPrinter')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'AreaPrinter')
        self.toolbar.setObjectName(u'AreaPrinter')

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
        return QCoreApplication.translate('AreaPrinter', message)


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

        # Create the dialog (after translation) and keep reference
        self.dlg = AreaPrinterDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/AreaPrinter/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'AreaPrinter'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&AreaPrinter'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
	self.setup()
        """Run method that performs all the real wrk"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass

    def setup(self):
	
	if(self.initialized == 0):
		map_1 = self.iface.activeComposers()[0].composition().getComposerMapById(1)	
	
		self.dlg.adjustBtnN.clicked.connect(self.moveNBtnClicked)
		self.dlg.adjustBtnS.clicked.connect(self.moveSBtnClicked)
		self.dlg.adjustBtnE.clicked.connect(self.moveEBtnClicked)
		self.dlg.adjustBtnW.clicked.connect(self.moveWBtnClicked)
	
		self.dlg.addBtnN.clicked.connect(self.addNBtnClicked)
		self.dlg.addBtnS.clicked.connect(self.addSBtnClicked)
		self.dlg.addBtnE.clicked.connect(self.addEBtnClicked)
		self.dlg.addBtnW.clicked.connect(self.addWBtnClicked)

		self.dlg.exitBtn.clicked.connect(self.exitBtnClicked)
		self.dlg.removeLastBtn.clicked.connect(self.removeLastPage)
		self.dlg.saveBtn.clicked.connect(self.generateComposer)
		
		extent_1 = QgsRectangle(map_1.currentMapExtent())
		self.extents.append(extent_1)
		self.initialized = 1	

	self.layer =  QgsVectorLayer('Polygon', 'fromAreaPrinter' , "memory")
	self.pr = self.layer.dataProvider() 		
		
		
	for ex in self.extents:
		self.printExtents(ex)
	
	QgsMapLayerRegistry.instance().addMapLayers([self.layer])

	

    def printExtents(self, rect):
	poly = QgsFeature()
	points = [QgsPoint(rect.xMinimum(), rect.yMinimum()), QgsPoint(rect.xMinimum(), rect.yMaximum()), QgsPoint(rect.xMaximum(), rect.yMaximum()),QgsPoint(rect.xMaximum(), rect.yMinimum())]
	poly.setGeometry(QgsGeometry.fromPolygon([points]))
	self.pr.addFeatures([poly])
	self.layer.updateExtents()
	


    
    def moveNBtnClicked(self):
	self.moveMap("North")

    def moveSBtnClicked(self):
	self.moveMap("South")
    def moveEBtnClicked(self):
	self.moveMap("East")
    def moveWBtnClicked(self):
	self.moveMap("West")
    def moveMap(self, direction):
	self.emptyLayer()
	offsetStep = 1000.0
	offsetX =0;
	offsetY =0;
	if direction == "North":
		offsetY = offsetStep
	elif direction == "South":
		offsetY = 0.0-offsetStep
	elif direction == "East":
		offsetX = offsetStep
	elif direction == "West":
		offsetX = 0.0-offsetStep
		

	
	for ex in self.extents:
		ex.setYMaximum(ex.yMaximum() + offsetY)
		ex.setYMinimum(ex.yMinimum() + offsetY)
		ex.setXMaximum(ex.xMaximum() + offsetX)
		ex.setXMinimum(ex.xMinimum() + offsetX)
		self.printExtents(ex)

	


    def addNBtnClicked(self):
	self.addExtent("North")
    def addSBtnClicked(self):
	self.addExtent("South")
    def addEBtnClicked(self):
	self.addExtent("East")
    def addWBtnClicked(self):
	self.addExtent("West")

    def addExtent(self, direction):
	self.emptyLayer()
	lastExtent = self.extents[len(self.extents)-1] #dont use on empty list

	offsetX = lastExtent.width() * (1-self.overlap);	
	offsetY = lastExtent.height() * (1-self.overlap);

	doOffsetX = 0.0
	doOffsetY = 0.0
	if direction == "North":
		doOffsetY = offsetY
	elif direction == "South":
		doOffsetY = 0.0-offsetY
	elif direction == "East":
		doOffsetX = offsetX
	elif direction == "West":
		doOffsetX = 0.0-offsetX

	newExtent = QgsRectangle(lastExtent)	
	newExtent.setXMaximum(lastExtent.xMaximum() + doOffsetX)	
	newExtent.setXMinimum(lastExtent.xMinimum() + doOffsetX)
	newExtent.setYMaximum(lastExtent.yMaximum() + doOffsetY)	
	newExtent.setYMinimum(lastExtent.yMinimum() + doOffsetY)
	
	
	self.extents.append(newExtent)
	for ex in self.extents:
		self.printExtents(ex)
	

    def exitBtnClicked(self):
	
	self.dlg.close()


    def removeLastPage(self):
	if len(self.extents) > 1:	
		self.extents.pop()
		self.emptyLayer()

		for ex in self.extents:
			self.printExtents(ex)	

    def emptyLayer(self):
	with edit(self.layer):
		    listOfIds = [feat.id() for feat in self.layer.getFeatures()]
		    self.layer.deleteFeatures( listOfIds )


    def generateComposer(self):
	A4PortraitHeight = 297.0
	A4PortraitWidth = 210.0
	topMargin = 10.0
	bottomMargin = 10.0
	sideMargin = 10.0
	
	self.iface.createNewComposer("AreaPrinter")
	composerViewIndex = len(self.iface.activeComposers()) -1
	comp = self.iface.activeComposers()[0].composition()      # new compositions dont have consistent index
	comp.setNumPages(len(self.extents))

	spaceBetweenPages = comp.spaceBetweenPages()
	comp.setPaperSize(A4PortraitWidth,A4PortraitHeight) 


	
	for i in range(0, len(self.extents)):
		newMap = QgsComposerMap(comp, sideMargin, i* (A4PortraitHeight + spaceBetweenPages) + topMargin, A4PortraitWidth- 2*sideMargin, A4PortraitHeight - topMargin - bottomMargin )
    		
		newMap.setNewExtent(self.extents[i])
		comp.addComposerMap(newMap)
		
		

	 
	
	







