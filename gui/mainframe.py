import os
from pathlib import Path

import matplotlib.pyplot as plt
import wx

from gui.panels.panel_backtest import PanelBacktest

# from gui.widgets.widget_matplotlib import MatplotlibPanel
from gui.widgets.widget_web import WebPanel

TOP_DIR = Path(__file__).parent.parent.parent.joinpath("Qbot")
APP_NAME = "Qbot - Quant AI Robot"


def OnAbout(event):
    wx.MessageBox("公众号:迈微AI研习社", "关于 AI量化投研平台", wx.OK | wx.ICON_INFORMATION)


def OnExit(win, event):
    win.Close(True)


def make_menubar(win):
    # Make a file menu with Hello and Exit items
    fileMenu = wx.Menu()
    # The "\t..." syntax defines an accelerator key that also triggers
    # the same event
    helloItem = fileMenu.Append(
        -1, "&Hello...\tCtrl-H", "Help string shown in status bar for this menu item"
    )
    fileMenu.AppendSeparator()
    # When using a stock ID we don't need to specify the menu item's
    # label
    exitItem = fileMenu.Append(wx.ID_EXIT, "退出")

    # Now a help menu for the about item
    helpMenu = wx.Menu()
    aboutItem = helpMenu.Append(wx.ID_ABOUT, "关于")

    menuBar = wx.MenuBar()
    menuBar.Append(fileMenu, "&文件")
    menuBar.Append(helpMenu, "&帮助")

    win.Bind(wx.EVT_MENU, OnAbout, aboutItem)
    win.Bind(wx.EVT_MENU, OnExit, exitItem)
    return menuBar


class MainFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MainFrame, self).__init__(*args, **kw)
        # 设置默认大小
        self.SetSize(wx.Size(600, 400))
        self.SetName(APP_NAME)

        # 设置程序图标
        icon_file = os.path.join(
            os.path.abspath(TOP_DIR.joinpath("gui/imgs")), "logo.ico"
        )
        icon = wx.Icon(icon_file, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        # 屏幕居中显示
        self.Centre()
        self.SetMenuBar(make_menubar(self))
        self.Maximize()

        self.CreateStatusBar()
        self.SetStatusText("欢迎使用AI智能量化投研平台！请关注公众号:迈微AI研习社")

        # 主窗口notebook
        self.m_notebook = wx.Notebook(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0
        )

        homepage = WebPanel(self.m_notebook)
        self.m_notebook.AddPage(homepage, "Qbot 官方网站", True)
        homepage.show_url("http://ufund-me.github.io")

        plt.rc("grid", color="#316931", linewidth=1, linestyle="-")
        plt.rc("xtick", labelsize=15)
        plt.rc("ytick", labelsize=15)

        # plot = MatplotlibPanel(self.m_notebook)
        # self.m_notebook.AddPage(plot, "基金投资策略分析", True)
        # plot.show()

        web = WebPanel(self.m_notebook)
        self.m_notebook.AddPage(web, "AI 选股/选基", True)
        web.show_url("https://investool.axiaoxin.com/")

        web = WebPanel(self.m_notebook)
        self.m_notebook.AddPage(web, "交易策略在线回测", True)
        # bash: cd ~/Qbot/pytrader/strategies/ && jupyter-notebook
        web.show_url("http://localhost:8888/notebooks/workflow_by_code.ipynb")

        web = WebPanel(self.m_notebook)
        self.m_notebook.AddPage(web, "基金投资策略分析", True)
        web.show_url("http://sunshowerc.github.io/fund/#/")

        self.m_notebook.AddPage(PanelBacktest(self.m_notebook), "可视化股票回测系统", True)
