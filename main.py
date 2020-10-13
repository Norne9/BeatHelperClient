#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import wx
import wx.grid
from game_finder import get_bs_path, NotFoundException
from app_logic import AppLogic
from song import Song
from typing import List


def wx_after(func):
    def after_fun(*args, **kwargs):
        wx.CallAfter(lambda: func(*args, **kwargs))
    return after_fun


class MainFrame(wx.Frame):
    app_logic: AppLogic

    def __init__(self, *args, **kwargs):
        try:
            game_path = get_bs_path()
        except NotFoundException:
            game_path = ""
        self.app_logic = AppLogic(game_path, self.show_songs, self.show_message, self.set_buttons,
                                  self.set_status, self.update_progress)

        # begin wxGlade: MainFrame.__init__
        kwargs["style"] = kwargs.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwargs)
        self.SetSize((640, 480))
        self.SetTitle("BeatHelper")

        self.main_statusbar: wx.StatusBar = self.CreateStatusBar(1)
        self.main_statusbar.SetStatusWidths([-1])
        self.main_statusbar.SetStatusText("Ready")

        self.panel_1 = wx.Panel(self, wx.ID_ANY)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        self.browse_panel = wx.Panel(self.panel_1, wx.ID_ANY)
        sizer_1.Add(self.browse_panel, 0, wx.ALL | wx.EXPAND, 3)

        sizer_2 = wx.StaticBoxSizer(wx.StaticBox(self.browse_panel, wx.ID_ANY, "Settings"), wx.HORIZONTAL)

        label_1 = wx.StaticText(self.browse_panel, wx.ID_ANY, "Game path: ")
        sizer_2.Add(label_1, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.path_text = wx.TextCtrl(self.browse_panel, wx.ID_ANY, game_path)
        sizer_2.Add(self.path_text, 1, wx.ALIGN_CENTER_VERTICAL, 0)

        self.browse_button = wx.Button(self.browse_panel, wx.ID_ANY, "Browse")
        sizer_2.Add(self.browse_button, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.notebook_1 = wx.Notebook(self.panel_1, wx.ID_ANY)
        sizer_1.Add(self.notebook_1, 0, wx.EXPAND, 0)

        self.notebook_1_pane_1 = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.notebook_1.AddPage(self.notebook_1_pane_1, "Personal recommendations")

        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)

        label_2 = wx.StaticText(self.notebook_1_pane_1, wx.ID_ANY, "ScoreSaber link: ")
        sizer_3.Add(label_2, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.link_text = wx.TextCtrl(self.notebook_1_pane_1, wx.ID_ANY, "")
        sizer_3.Add(self.link_text, 1, wx.ALIGN_CENTER_VERTICAL, 0)

        self.recommend_button = wx.Button(self.notebook_1_pane_1, wx.ID_ANY, "Recommend")
        sizer_3.Add(self.recommend_button, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.notebook_1_pane_2 = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.notebook_1.AddPage(self.notebook_1_pane_2, "Top songs")

        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)

        label_3 = wx.StaticText(self.notebook_1_pane_2, wx.ID_ANY, "From score: ")
        sizer_6.Add(label_3, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.min_score_spin = wx.SpinCtrlDouble(self.notebook_1_pane_2, wx.ID_ANY, initial=100.0, min=1.0, max=1000.0)
        sizer_6.Add(self.min_score_spin, 1, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 3)

        self.find_button = wx.Button(self.notebook_1_pane_2, wx.ID_ANY, "Find")
        sizer_6.Add(self.find_button, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.songs_panel = wx.Panel(self.panel_1, wx.ID_ANY)
        sizer_1.Add(self.songs_panel, 1, wx.ALL | wx.EXPAND, 3)

        sizer_4 = wx.StaticBoxSizer(wx.StaticBox(self.songs_panel, wx.ID_ANY, "Recommended songs"), wx.HORIZONTAL)

        self.song_grid = wx.grid.Grid(self.songs_panel, wx.ID_ANY, size=(1, 1))
        self.song_grid.CreateGrid(0, 6)
        self.song_grid.EnableEditing(0)
        self.song_grid.SetColLabelValue(0, "Name")
        self.song_grid.SetColLabelValue(1, "Uploader")
        self.song_grid.SetColLabelValue(2, "Difficulty")
        self.song_grid.SetColLabelValue(3, "Min Score")
        self.song_grid.SetColLabelValue(4, "Max Score")
        self.song_grid.SetColLabelValue(5, "Downloaded")
        sizer_4.Add(self.song_grid, 1, wx.EXPAND, 0)

        self.download_panel = wx.Panel(self.panel_1, wx.ID_ANY)
        sizer_1.Add(self.download_panel, 0, wx.ALL | wx.EXPAND, 3)

        sizer_5 = wx.StaticBoxSizer(wx.StaticBox(self.download_panel, wx.ID_ANY, "Download"), wx.HORIZONTAL)

        self.download_gauge = wx.Gauge(self.download_panel, wx.ID_ANY, range=10000,
                                       style=wx.GA_HORIZONTAL | wx.GA_SMOOTH)
        sizer_5.Add(self.download_gauge, 1, wx.EXPAND, 0)

        self.download_button = wx.Button(self.download_panel, wx.ID_ANY, "Make playlist and download")
        sizer_5.Add(self.download_button, 0, 0, 0)

        self.cancel_button = wx.Button(self.download_panel, wx.ID_ANY, "Cancel")
        self.cancel_button.Disable()
        sizer_5.Add(self.cancel_button, 0, 0, 0)

        self.download_panel.SetSizer(sizer_5)

        self.songs_panel.SetSizer(sizer_4)

        self.notebook_1_pane_2.SetSizer(sizer_6)

        self.notebook_1_pane_1.SetSizer(sizer_3)

        self.browse_panel.SetSizer(sizer_2)

        self.panel_1.SetSizer(sizer_1)

        self.Layout()

        self.Bind(wx.EVT_BUTTON, self.on_browse, self.browse_button)
        self.Bind(wx.EVT_BUTTON, self.on_recommend, self.recommend_button)
        self.Bind(wx.EVT_BUTTON, self.on_find, self.find_button)
        self.Bind(wx.EVT_BUTTON, self.on_download, self.download_button)
        self.Bind(wx.EVT_BUTTON, self.on_cancel, self.cancel_button)
        # end wxGlade

    @wx_after
    def show_songs(self, songs: List[Song]):
        song_count = len(songs)
        rows_count = self.song_grid.GetNumberRows()
        if song_count > rows_count:
            self.song_grid.InsertRows(0, song_count - rows_count)
        elif rows_count > song_count:
            self.song_grid.DeleteRows(0, rows_count - song_count)

        for i, song in enumerate(songs):
            self.song_grid.SetCellValue(i, 0, song.song_name)
            self.song_grid.SetCellAlignment(i, 0, wx.ALIGN_LEFT, wx.ALIGN_CENTRE)
            self.song_grid.SetCellValue(i, 1, song.uploader)
            self.song_grid.SetCellAlignment(i, 1, wx.ALIGN_LEFT, wx.ALIGN_CENTRE)
            self.song_grid.SetCellValue(i, 2, song.difficulty)
            self.song_grid.SetCellAlignment(i, 2, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
            self.song_grid.SetCellValue(i, 3, f"{song.worst_score:.2f}")
            self.song_grid.SetCellAlignment(i, 3, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
            self.song_grid.SetCellValue(i, 4, f"{song.best_score:.2f}")
            self.song_grid.SetCellAlignment(i, 4, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
            self.song_grid.SetCellValue(i, 5, "Yes" if song.downloaded else "No")
            self.song_grid.SetCellAlignment(i, 5, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        self.song_grid.AutoSizeColumns()

    @wx_after
    def show_message(self, msg: str):
        dialog = wx.MessageDialog(self, msg)
        dialog.ShowModal()
        dialog.Destroy()

    @wx_after
    def set_buttons(self, active: bool):
        buttons = [self.recommend_button, self.find_button, self.download_button]
        for btn in buttons:
            btn.Enable(active)
        self.cancel_button.Enable(not active)

    @wx_after
    def set_status(self, text: str):
        self.main_statusbar.SetStatusText(text)

    @wx_after
    def update_progress(self, progress: float):
        progress = max(0.0, min(progress, 10000.0))
        self.download_gauge.SetValue(int(progress * 10000))

    def on_cancel(self, _):
        self.app_logic.cancel_task()

    def on_browse(self, _):
        dir_selector = wx.DirDialog(self, "Select game folder", self.path_text.GetValue())
        if dir_selector.ShowModal() == wx.ID_OK:
            self.path_text.SetValue(dir_selector.GetPath())
        dir_selector.Destroy()

    def on_recommend(self, _):  # wxGlade: MainFrame.<event_handler>
        self.app_logic.recommend_songs(self.link_text.GetValue())

    def on_find(self, _):  # wxGlade: MainFrame.<event_handler>
        self.app_logic.find_songs(self.min_score_spin.GetValue())

    def on_download(self, _):  # wxGlade: MainFrame.<event_handler>
        self.app_logic.download()


class BeatHelperApp(wx.App):
    def OnInit(self):
        self.frame = MainFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True


if __name__ == "__main__":
    app = BeatHelperApp(0)
    app.MainLoop()
