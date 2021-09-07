from app.components.datatable import DataGrid
import wx


class PreviewGridDialog(wx.Dialog):
    def __init__(self, parent, data=None, **kwargs):
        super(PreviewGridDialog, self).__init__(parent=None, **kwargs)
        sizer = wx.BoxSizer(wx.VERTICAL)
        grid = DataGrid(self)
        if data is not None:
            grid.set_table(data)
        sizer.Add(grid)
        buttons = self.CreateButtonSizer(wx.CLOSE | wx.OK)
        sizer.Add(buttons)
        self.SetSizer(sizer)