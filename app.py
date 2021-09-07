import pandas
import wx
from app.views.preview_grid import PreviewGridDialog


class MainWindow(wx.Frame):
    def __init__(self, parent=None, title='Main Window'):
        super(MainWindow, self).__init__(parent)
        panel = wx.Panel(self)
        button = wx.Button(panel, label='Preview')
        button.Bind(wx.EVT_BUTTON, self.onPreviewBtnClick)
        self.data = pandas.DataFrame(dict(a=[1, 2, 3, 4, 5],
                                          b=[3, 4, 5, 6, 7],
                                          c=[5, 6, 7, 8, 9]))
        self.Show()

    def onPreviewBtnClick(self, event):
        with PreviewGridDialog(self, self.data, title='Data Preview') as previewDlg:
            if previewDlg.ShowModal() == wx.CLOSE:
                print('Closing the preview dialog..')


if __name__ == '__main__':
    app = wx.App()
    window = MainWindow()
    app.MainLoop()