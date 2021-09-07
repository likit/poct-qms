import wx
from ObjectListView import ObjectListView, ColumnDefn


class ScanResultDialog(wx.Dialog):
    def __init__(self, parent, records, columns, title='New Values', **kwargs):
        super(ScanResultDialog, self).__init__(parent, title='New Values', **kwargs)
        self.records = records
        self.columns = columns
        vsizer = wx.BoxSizer(wx.VERTICAL)
        instruction = wx.StaticText(self, wx.ID_ANY, label='Double click to change.')
        buttons = self.CreateButtonSizer(wx.CANCEL | wx.OK)
        self.dataOlv = ObjectListView(self, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        vsizer.Add(instruction)
        vsizer.Add(self.dataOlv, 1, wx.EXPAND)
        vsizer.Add(buttons)
        self.SetSizer(vsizer)
        self.setData(self.records, self.columns)
        self.Layout()

    def setData(self, data, columns=[]):
        """Update the ObjectListView widget's contents """

        olv_columns = []
        for column in columns:
            olv_columns.append(ColumnDefn(column.title(), "left", 120, column.lower()))
        self.dataOlv.SetColumns(olv_columns)
        self.dataOlv.SetObjects(data)
