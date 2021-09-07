import wx
from ObjectListView import ObjectListView, ColumnDefn
from openpyxl import load_workbook
from app.controller.load_data_dialog import load_and_convert


class LoadDataDialog(wx.Dialog):
    def __init__(self, parent, pathName='', **kwargs):
        super(LoadDataDialog, self).__init__(parent, **kwargs)
        self.pathName = pathName
        self.records = []
        self.columns = []
        vsizer = wx.BoxSizer(wx.VERTICAL)
        buttons = self.CreateButtonSizer(wx.CANCEL | wx.OK)
        self.dataOlv = ObjectListView(self, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        vsizer.Add(self.dataOlv, 1, wx.EXPAND)
        vsizer.Add(buttons)
        self.SetSizer(vsizer)
        self.Layout()
        if self.pathName:
            self.choose_worksheet()

    def setData(self, data=None, columns=[]):
        """Update the ObjectListView widget's contents """

        olv_columns = []
        for column in columns:
            olv_columns.append(ColumnDefn(column.title(), "left", 120, column.lower()))
        self.dataOlv.SetColumns(olv_columns)
        if len(data) > 20:
            self.dataOlv.SetObjects(data[:20])
        else:
            self.dataOlv.SetObjects(data)

    def choose_worksheet(self):
        wb = load_workbook(self.pathName)
        with wx.SingleChoiceDialog(self, '', 'Choose column', [ws.title for ws in wb.worksheets]) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                sheet = dialog.GetStringSelection()
                self.records, self.columns = load_and_convert(self.pathName, sheet)
                self.setData(self.records, self.columns)
