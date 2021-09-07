import sqlalchemy.exc
import wx

from app.extension import engine
from sqlalchemy.orm import sessionmaker
from ObjectListView import ObjectListView, ColumnDefn
from app.controller.value_dialog import *
import pandas as pd

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
        self.valueTextCtrl = wx.TextCtrl(self, value='')
        buttonSizer.Add(self.valueTextCtrl, 0, wx.ALL, 4)
        addBtn = wx.Button(self, wx.ID_ANY, label='Add')
        buttonSizer.Add(addBtn, 0, wx.ALL, 2)
        saveBtn = wx.Button(self, wx.ID_ANY, label='Save')
        buttonSizer.Add(saveBtn, 0, wx.ALL, 2)
        deleteBtn = wx.Button(self, wx.ID_ANY, label='Delete')
        buttonSizer.Add(deleteBtn, 0, wx.ALL, 2)
        addBtn.Bind(wx.EVT_BUTTON, self.addValue)
        saveBtn.Bind(wx.EVT_BUTTON, self.saveValue)
        deleteBtn.Bind(wx.EVT_BUTTON, self.deleteValue)
        importBtn = wx.Button(self, wx.ID_ANY, label='Import')
        buttonSizer.Add(importBtn, 0, wx.ALL, 2)
        importBtn.Bind(wx.EVT_BUTTON, self.importValues)
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

    def addValue(self, event):
        is_succeeded, message = add_record(self.session,
                                           self.valueTextCtrl.GetValue(),
                                           self.model, self.attr)
        self.show_message(message)
        if is_succeeded:
            self.valueTextCtrl.SetValue('')
            self.reloadData()

    def saveValue(self, event):
        selected_row = self.dataOlv.GetSelectedObject()
        is_succeeded, message = save_record(self.session, selected_row,
                                            self.valueTextCtrl.GetValue(),
                                            self.model, self.attr)
        self.show_message(message)
        if is_succeeded:
            self.reloadData()

    def deleteValue(self, event):
        selected_row = self.dataOlv.GetSelectedObject()
        is_succeeded, message = delete_record(self.session, selected_row, self.model)
        self.show_message(message)
        if is_succeeded:
            self.reloadData()
            self.valueTextCtrl.SetValue('')

    def update_status_text_ctrl(self, event):
        selected_row = self.dataOlv.GetSelectedObject()
        self.valueTextCtrl.SetValue(getattr(selected_row, self.attr))

    def importValues(self, event):
        with wx.FileDialog(self, 'Import values from a file',
                           wildcard='Excel file (*.xlsx)|*.xlsx') as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathName = fileDialog.GetPath()
            try:
                df = pd.read_excel(pathName)
            except Exception as e:
                with wx.MessageBox('Could not open the file.', 'Failed!', style=wx.OK) as msgDialog:
                    msgDialog.ShowModal()
                    return
            else:
                with wx.SingleChoiceDialog(self, 'Which column contains value you want to import?', 'Choose column',
                                      df.columns) as columnDialog:
                    if columnDialog.ShowModal() == wx.ID_OK:
                        column = columnDialog.GetStringSelection()
                        values = set(df[column])
                        for val in values:
                            if pd.isna(val):
                                continue
                            try:
                                rec = self.model()
                                setattr(rec, self.attr, val)
                                self.session.add(rec)
                                self.session.commit()
                            except sqlalchemy.exc.IntegrityError:
                                self.session.rollback()
                                print(f'{val} exists.')
                                continue
                        self.reloadData()
