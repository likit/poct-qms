import wx
from app.models.values import TestStatus
from ObjectListView import ObjectListView, ColumnDefn, Filter


class ScanResultDialog(wx.Dialog):
    def __init__(self, parent, records, columns, session, title='', **kwargs):
        super(ScanResultDialog, self).__init__(parent, title=title, size=(640, 480), **kwargs)
        self.columns = columns
        self.records = records
        vsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.choices = [''] + [item.status for item in session.query(TestStatus).all()]
        button_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, label='Edit')
        comment_label = wx.StaticText(self, label='Payment Status')
        self.status_entry = wx.ComboBox(self, value='',
                                        choices=self.choices,
                                        style=wx.CB_SORT | wx.CB_READONLY)
        save_button = wx.Button(self, label='Save')
        save_button.Bind(wx.EVT_BUTTON, self.onSaveButtonClicked)
        button_sizer.Add(comment_label)
        button_sizer.Add(self.status_entry)
        button_sizer.Add(save_button, 0, wx.TOP | wx.EXPAND, 20)
        buttons = self.CreateButtonSizer(wx.CANCEL | wx.OK)
        self.dataOlv = ObjectListView(self, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.dataOlv.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onItemSelected)
        hsizer.Add(self.dataOlv, 1, wx.EXPAND | wx.LEFT | wx.TOP, 10)
        hsizer.Add(button_sizer, 0, wx.EXPAND | wx.RIGHT, 10)
        vsizer.Add(hsizer, 1, wx.EXPAND)
        vsizer.Add(buttons)
        self.SetSizer(vsizer)
        self.dataOlv.SetFilter(Filter.Predicate(lambda x: x.payment_status != 'Success'))
        self.dataOlv.filter(self.records)
        self.setData(self.records, self.columns)
        self.Layout()
        self.Maximize(True)

    def setData(self, data, columns=[]):
        """Update the ObjectListView widget's contents """

        olv_columns = []
        for column in columns:
            olv_columns.append(ColumnDefn(column.title(), "left", 120, column.lower()))
        self.dataOlv.SetColumns(olv_columns)
        self.dataOlv.SetObjects(data)

    def onItemSelected(self, event):
        selected_row = self.dataOlv.GetSelectedObject()
        choice_idx = self.status_entry.FindString(selected_row.payment_status)
        self.status_entry.SetSelection(choice_idx)

    def onSaveButtonClicked(self, event):
        selected_row = self.dataOlv.GetSelectedObject()
        print(self.status_entry.GetStringSelection())
        selected_row.payment_status = self.status_entry.GetStringSelection()
        self.dataOlv.RefreshObject(selected_row)
