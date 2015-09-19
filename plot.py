import glob
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from matplotlib.collections import LineCollection

class Plot:
    
    @staticmethod
    def get_a_ax(boundary):
        
        # print "ratio:", boundary.ratio()
        # print boundary.x_range.span()
        # print boundary.y_range.span()
        #
        pic_height = glob.PIC_WIDTH
        print "Width:",glob.PIC_WIDTH, "Height:",pic_height
        fig = plt.figure(figsize=(glob.PIC_WIDTH/glob.MY_DPI, pic_height/glob.MY_DPI), \
                dpi=glob.MY_DPI)
        
        ax = fig.add_subplot(111)
        
        return ax
    
    @staticmethod
    def format_ax(ax, b):
        ax.set_xlim(b.x_range.min, b.x_range.max)
        ax.set_ylim(b.y_range.min, b.y_range.max)
        
        # ax.set_aspect('equal', 'datalim')
        
        # do not use offset notation for x- and y-axis
        x_formatter = matplotlib.ticker.ScalarFormatter(useOffset=False)
        ax.xaxis.set_major_formatter(x_formatter)
        y_formatter = matplotlib.ticker.ScalarFormatter(useOffset=False)
        ax.yaxis.set_major_formatter(y_formatter)
    
    @staticmethod
    def save_pic(img_filename):
        figure = plt.gcf() # get current figure
        # # # # when saving, specify the DPI
        plt.savefig(img_filename, bbox_inches='tight')
    
    @staticmethod
    def plot_graph_with_bgmap(lines, bg_filename, boundary, img_filename):
        ax = Plot.get_a_ax(boundary)
        Plot.format_ax(ax, boundary)
        # plot an image
        Plot.plot_bgmap(ax, bg_filename, boundary)
        
        ax.add_collection(LineCollection(lines, color='red'))
        
        Plot.save_pic(img_filename)
    
    @staticmethod
    def plot_bgmap(ax, bg_filename, b):
        
        img = plt.imread(bg_filename)
        # height, width, colors = img.shape
        
        ax.imshow(img, zorder=0, \
             extent=[b.x_range.min, b.x_range.max, \
                     b.y_range.min, b.y_range.max], aspect=1.33)