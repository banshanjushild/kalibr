# 1. 注释掉 wx 相关的导入，防止因缺少库报错
# import wx
# import wx.aui

import matplotlib as mpl
# 2. 关键修改：切换到 'Agg' 后端
# 这告诉 Matplotlib 不要尝试连接 X Server，而是在内存中渲染图片
mpl.use('Agg') 

from matplotlib.backends.backend_agg import FigureCanvasAgg as Canvas
# 不需要 Toolbar，因为不显示窗口
# from matplotlib.backends.backend_wx import NavigationToolbar2Wx as Toolbar
import collections
import matplotlib.pyplot as plt

class PlotCollection:
    def __init__(self, window_name="", window_size=(800,600)):
        self.frame_name = window_name
        self.window_size = window_size
        self.figureList = collections.OrderedDict()
    
    def add_figure(self, tabname, fig):
        self.figureList[tabname] = fig
        
    def delete_figure(self, name):
        self.figureList.pop(name, None)
    
    def show(self):
        """
        重写 show 方法：不再创建 wx 窗口，而是直接保存所有图表到文件
        """
        if len(list(self.figureList.keys())) == 0:
            return
            
        print(f"[PlotCollection] 检测到 {len(self.figureList)} 个图表，正在后台静默保存...")
        
        for i, (name, fig) in enumerate(self.figureList.items()):
            # 自动调整布局防止遮挡
            plt.figure(fig.number)
            plt.tight_layout()
            
            # 将文件名中的非法字符替换掉，生成安全的文件名
            safe_name = name.replace(" ", "_").replace("/", "_")
            filename = f"kalibr_plot_{i}_{safe_name}.png"
            
            # 保存图表
            fig.savefig(filename, dpi=100)
            print(f"[PlotCollection] 已保存图表: {filename}")
            
        print("[PlotCollection] 所有图表保存完成。跳过 GUI 显示。")
        # 不再执行 app.MainLoop()，直接返回
        
    # 保留类定义以维持代码结构，防止其他代码调用时找不到类
    class Plot:
        def __init__(self, parent, fig, id = -1, dpi = None, **kwargs):
            # 这里的 parent 是 wx 对象，但我们不使用了，所以忽略它
            # wx.Panel.__init__(self, parent, id=id, **kwargs) # 注释掉
            fig.set_figheight(2)
            fig.set_figwidth(2)
            # 不再创建 Canvas 和 Toolbar
            pass 

    class PlotNotebook:
        def __init__(self, parent, id = -1):
            # wx.Panel.__init__(self, parent, id=id) # 注释掉
            # self.nb = wx.aui.AuiNotebook(self) # 注释掉
            pass
    
        def add(self, name, fig):
           # 不调用 wx 的 AddPage
           pass
