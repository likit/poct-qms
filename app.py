import pandas
import wx
from ObjectListView import ObjectListView, ColumnDefn
from sqlalchemy.orm import sessionmaker

from app.extension import engine, Base, GenericDBClass
from app.views.preview_grid import PreviewGridDialog
from app.dialogs.value_dialog import ValueDialog
from app.dialogs.load_data_dialog import LoadDataDialog
from app.dialogs.scan_result_dialog import ScanResultDialog
from app.models.values import TestStatus, ErrorCause

import ctypes

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
except:
    pass

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


class MainWindow(wx.Frame):
    def __init__(self, parent=None, title='Main Window', size=(860, 640)):
        super(MainWindow, self).__init__(parent, title=title, size=size)
        panel = wx.Panel(self)
        self.dataOlv = ObjectListView(panel, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.records = []
        self.columns = []
        self.setData(self.records, self.columns)
        self.pathName = ''
        data_source_sizer = wx.StaticBoxSizer(wx.HORIZONTAL, panel, 'Data source')
        self.datapath = wx.StaticText(data_source_sizer.GetStaticBox(), id=wx.ID_ANY, label='No data loaded.')
        data_source_sizer.Add(self.datapath, 0, wx.EXPAND)
        toolbar_sizer = wx.StaticBoxSizer(wx.HORIZONTAL, panel, 'Shortcut')
        import_btn = wx.Button(toolbar_sizer.GetStaticBox(), wx.ID_ANY, label='Import Data')
        import_btn.Bind(wx.EVT_BUTTON, self.onImportMenuItemClick)
        self.scan_btn = wx.Button(toolbar_sizer.GetStaticBox(), wx.ID_ANY, label='Scan Errors')
        self.scan_btn.Disable()
        self.scan_btn.Bind(wx.EVT_BUTTON, self.onScanBtnClick)
        toolbar_sizer.Add(import_btn, 0, wx.ALL, 2)
        toolbar_sizer.Add(self.scan_btn, 0, wx.ALL, 2)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(toolbar_sizer, 0, wx.EXPAND | wx.ALL, 5)
        vsizer.Add(data_source_sizer, 0, wx.ALL | wx.EXPAND, 5)
        vsizer.Add(self.dataOlv, 1, wx.EXPAND)
        self.createMenuBar()
        panel.SetSizer(vsizer)
        self.Layout()
        self.Maximize(True)
        self.Show()

    def createMenuBar(self):
        menuBar = wx.MenuBar()
        fileMenu = wx.Menu()
        importItem = fileMenu.Append(
            wx.ID_ANY, "Import Data", "Import Data from Excel"
        )
        self.Bind(wx.EVT_MENU, self.onImportMenuItemClick, importItem)
        settingMenu = wx.Menu()
        testStatusItem = settingMenu.Append(
            wx.ID_ANY, "Test Status", "Config Test Status"
        )
        self.Bind(wx.EVT_MENU, self.onTestStatusMenuItemClick, testStatusItem)
        errorCauseItem = settingMenu.Append(
            wx.ID_ANY, "Error Cause", "Config Error Cause"
        )
        self.Bind(wx.EVT_MENU, self.onErrorCauseMenuItemClick, errorCauseItem)
        menuBar.Append(fileMenu, '&File')
        menuBar.Append(settingMenu, '&Setting')

        self.SetMenuBar(menuBar)

    def onTestStatusMenuItemClick(self, event):
        columns = ['id', 'status']
        with ValueDialog(self, columns, TestStatus, 'status', size=(600, 400), title='Test Status List') as dlg:
            if dlg.ShowModal() == wx.OK:
                print('It is ok.')

    def onErrorCauseMenuItemClick(self, event):
        columns = ['id', 'cause']
        with ValueDialog(self, columns, ErrorCause, 'cause', size=(600, 400), title='Error Cause List') as dlg:
            if dlg.ShowModal() == wx.OK:
                print('It is ok.')

    def onImportMenuItemClick(self, event):
        with wx.FileDialog(self, 'Import values from a file',
                           wildcard='Excel file (*.xlsx)|*.xlsx') as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            self.pathName = fileDialog.GetPath()
            if self.pathName:
                with LoadDataDialog(self, self.pathName, title='Data Preview', size=(800, 640)) as importDialog:
                    if importDialog.ShowModal() == wx.ID_OK:
                        self.records = importDialog.records
                        self.columns = importDialog.columns
                        self.datapath.SetLabel(self.pathName)
                        self.setData(self.records, self.columns)
                        self.scan_btn.Enable()

    def onScanBtnClick(self, event):
        with ScanResultDialog(self, self.records,
                              self.columns,
                              session=session,
                              title='Not Success') as dialog:
            dialog.ShowModal()
            self.dataOlv.RefreshObjects(dialog.records)

    def setData(self, data=[], columns=[]):
        """Update the ObjectListView widget's contents """

        olv_columns = []
        for column in columns:
            olv_columns.append(ColumnDefn(column.title(), "left", 120, column.lower()))
        self.dataOlv.SetColumns(olv_columns)
        self.dataOlv.SetObjects(data)


if __name__ == '__main__':
    app = wx.App()
    window = MainWindow()
    app.MainLoop()
