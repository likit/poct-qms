import wx
from app.models.values import TestStatus, ErrorCause
from ObjectListView import ObjectListView, ColumnDefn, Filter


class ScanResultDialog(wx.Dialog):
    def __init__(self, parent, records, columns, session, title='', **kwargs):
        super(ScanResultDialog, self).__init__(parent, title=title, size=(1200, 800), **kwargs)
        self.columns = columns
        self.records = records
        vsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.status_choices = [''] + [item.status for item in session.query(TestStatus).all()]
        self.error_choices = [''] + [item.cause for item in session.query(ErrorCause).all()]
        button_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, label='Edit')
        status_label = wx.StaticText(self, label='Payment Status')
        self.status_entry = wx.ComboBox(self, value='',
                                        choices=self.status_choices,
                                        style=wx.CB_SORT | wx.CB_READONLY)
        error_label = wx.StaticText(self, label='Error')
        self.error_entry = wx.ComboBox(self, value='',
                                        choices=self.error_choices,
                                        style=wx.CB_SORT | wx.CB_READONLY)
        self.apply_to_all = wx.CheckBox(self, label='Apply to all')
        save_button = wx.Button(self, label='Save')
        save_button.Bind(wx.EVT_BUTTON, self.onSaveButtonClicked)
        button_sizer.Add(status_label)
        button_sizer.Add(self.status_entry, 1, wx.EXPAND)
        button_sizer.Add(error_label)
        button_sizer.Add(self.error_entry, 1, wx.EXPAND)
        button_sizer.Add(self.apply_to_all)
        button_sizer.Add(save_button, 0, wx.TOP | wx.EXPAND, 20)
        buttons = self.CreateButtonSizer(wx.OK)
        self.dataOlv = ObjectListView(self, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.dataOlv.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onItemSelected)
        hsizer.Add(self.dataOlv, 1, wx.EXPAND | wx.LEFT | wx.TOP, 10)
        hsizer.Add(button_sizer, 0, wx.RIGHT, 10)
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
        status_idx = self.status_entry.FindString(selected_row.payment_status)
        error_idx = self.error_entry.FindString(selected_row.error_cause)
        self.status_entry.SetSelection(status_idx)
        self.error_entry.SetSelection(error_idx)

    def onSaveButtonClicked(self, event):
        selected_row = self.dataOlv.GetSelectedObject()
        selected_row.payment_status = self.status_entry.GetStringSelection()
        new_error_cause = self.error_entry.GetStringSelection()
        selected_row.error_cause = new_error_cause
        if self.apply_to_all.IsChecked():
            for rec in self.records:
                if rec.payment_status == self.status_entry.GetStringSelection():
                    rec.error_cause = new_error_cause
            self.dataOlv.RefreshObjects(self.records)
        else:
            self.dataOlv.RefreshObject(selected_row)

        self.apply_to_all.SetValue(False)
