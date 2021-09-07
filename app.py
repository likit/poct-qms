import pandas
import wx
from sqlalchemy.orm import sessionmaker

from app.extension import engine, Base, GenericDBClass
from app.views.preview_grid import PreviewGridDialog
from app.dialogs.test_status import ValueDialog
from app.models.values import TestStatus, ErrorCause

Base.metadata.create_all(engine)


class MainWindow(wx.Frame):
    def __init__(self, parent=None, title='Main Window'):
        super(MainWindow, self).__init__(parent)
        panel = wx.Panel(self)
        button = wx.Button(panel, label='Preview')
        button.Bind(wx.EVT_BUTTON, self.onPreviewBtnClick)
        self.data = pandas.DataFrame(dict(a=[1, 2, 3, 4, 5],
                                          b=[3, 4, 5, 6, 7],
                                          c=[5, 6, 7, 8, 9]))
        self.createMenuBar()
        self.Show()

    def createMenuBar(self):
        menuBar = wx.MenuBar()
        settingMenu = wx.Menu()
        testStatusItem = settingMenu.Append(
            wx.ID_ANY, "Test Status", "Config Test Status"
        )
        self.Bind(wx.EVT_MENU, self.onTestStatusMenuItemClick, testStatusItem)
        errorCauseItem = settingMenu.Append(
            wx.ID_ANY, "Error Cause", "Config Error Cause"
        )
        self.Bind(wx.EVT_MENU, self.onErrorCauseMenuItemClick, errorCauseItem)
        menuBar.Append(settingMenu, '&Setting')

        self.SetMenuBar(menuBar)

    def onTestStatusMenuItemClick(self, event):
        columns = ['id', 'status']
        with ValueDialog(self, columns, TestStatus, 'status', size=(480, 480), title='Test Status List') as dlg:
            if dlg.ShowModal() == wx.OK:
                print('It is ok.')

    def onErrorCauseMenuItemClick(self, event):
        columns = ['id', 'cause']
        with ValueDialog(self, columns, ErrorCause, 'cause', size=(480, 480), title='Error Cause List') as dlg:
            if dlg.ShowModal() == wx.OK:
                print('It is ok.')

    def onPreviewBtnClick(self, event):
        with PreviewGridDialog(self, self.data, title='Data Preview') as previewDlg:
            if previewDlg.ShowModal() == wx.CLOSE:
                print('Closing the preview dialog..')


if __name__ == '__main__':
    app = wx.App()
    window = MainWindow()
    app.MainLoop()