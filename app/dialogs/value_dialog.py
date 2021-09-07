import wx

from app.extension import engine
from sqlalchemy.orm import sessionmaker
from ObjectListView import ObjectListView, ColumnDefn
from app.controller.value_dialog import *

Session = sessionmaker(bind=engine)


class ValueDialog(wx.Dialog):
    def __init__(self, parent, columns, model, attr, **kwargs):
        super(ValueDialog, self).__init__(parent, **kwargs)
        self.dbData = None
        self.columns = columns
        self.session = Session()
        self.dataOlv = ObjectListView(self, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.model = model
        self.attr = attr
        self.setData()

        vsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)

        hsizer.Add(self.dataOlv, 1, wx.LEFT | wx.CENTER | wx.EXPAND, 5)
        buttonSizer = wx.StaticBoxSizer(wx.VERTICAL, self, 'Edit')
        self.statusTextCtrl = wx.TextCtrl(self, value='')
        buttonSizer.Add(self.statusTextCtrl, 0, wx.ALL, 4)
        addBtn = wx.Button(self, wx.ID_ANY, label='Add')
        buttonSizer.Add(addBtn, 0, wx.ALL, 2)
        saveBtn = wx.Button(self, wx.ID_ANY, label='Save')
        buttonSizer.Add(saveBtn, 0, wx.ALL, 2)
        deleteBtn = wx.Button(self, wx.ID_ANY, label='Delete')
        buttonSizer.Add(deleteBtn, 0, wx.ALL, 2)
        addBtn.Bind(wx.EVT_BUTTON, self.addStatus)
        saveBtn.Bind(wx.EVT_BUTTON, self.saveStatus)
        deleteBtn.Bind(wx.EVT_BUTTON, self.deleteStatus)
        hsizer.Add(buttonSizer, 0, wx.RIGHT, 5)
        vsizer.Add(hsizer, 1, wx.EXPAND | wx.CENTER, 5)
        buttons = self.CreateButtonSizer(wx.CLOSE)
        vsizer.Add(buttons)
        self.SetSizer(vsizer)

        self.dataOlv.Bind(wx.EVT_LIST_ITEM_SELECTED, self.update_status_text_ctrl)
        self.Layout()

    def reloadData(self):
        self.dbData = show_all_records(self.session, self.model, self.attr)
        self.dataOlv.SetObjects(self.dbData)

    def setData(self, data=None):
        """Update the ObjectListView widget's contents """

        olv_columns = []
        for column in self.columns:
            olv_columns.append(ColumnDefn(column.title(), "left", 120, column.lower()))
        self.dataOlv.SetColumns(olv_columns)
        self.dbData = show_all_records(self.session, self.model, self.attr)
        self.dataOlv.SetObjects(self.dbData)

    def show_message(self, message):
        with wx.MessageDialog(self, message, 'Status') as msg:
            msg.ShowModal()

    def addStatus(self, event):
        is_succeeded, message = add_record(self.session,
                                           self.statusTextCtrl.GetValue(),
                                           self.model, self.attr)
        self.show_message(message)
        if is_succeeded:
            self.statusTextCtrl.SetValue('')
            self.reloadData()

    def saveStatus(self, event):
        selected_row = self.dataOlv.GetSelectedObject()
        is_succeeded, message = save_record(self.session, selected_row,
                                            self.statusTextCtrl.GetValue(),
                                            self.model, self.attr)
        self.show_message(message)
        if is_succeeded:
            self.reloadData()

    def deleteStatus(self, event):
        selected_row = self.dataOlv.GetSelectedObject()
        is_succeeded, message = delete_record(self.session, selected_row, self.model)
        self.show_message(message)
        if is_succeeded:
            self.reloadData()

    def update_status_text_ctrl(self, event):
        selected_row = self.dataOlv.GetSelectedObject()
        self.statusTextCtrl.SetValue(selected_row.status)
