import glob
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

class Plot:
    
    @staticmethod
    def get_a_ax(boundary):
        pic_height = glob.PIC_WIDTH/boundary.ratio
        # print "Width:",PIC_WIDTH, "Height:",pic_height
        fig = plt.figure(figsize=(glob.PIC_WIDTH/glob.MY_DPI, pic_height/glob.MY_DPI), \
                dpi=glob.MY_DPI)
        
        ax = fig.add_subplot(111)
        
        return ax
    
    @staticmethod
    def format_ax(ax, boundary):    
        ax.set_xlim(boundary.min_x, boundary.max_x)
        ax.set_ylim(boundary.min_y, boundary.max_y)
    
        # do not use offset notation for x- and y-axis
        x_formatter = matplotlib.ticker.ScalarFormatter(useOffset=False)
        ax.xaxis.set_major_formatter(x_formatter)
        y_formatter = matplotlib.ticker.ScalarFormatter(useOffset=False)
        ax.yaxis.set_major_formatter(y_formatter)
    
    @staticmethod
    def plot_graph_with_bgmap(edges, bg_filename, boundary, img_filename):
        ax = Plot.get_a_ax(boundary)
        Plot.format_ax(ax, boundary)
        # plot an image
        Plot.plot_bgmap(ax, bg_filename, boundary)
        # plot an road map
        # Plot.plot_road_map(ax, edges, "red")
        Plot.save_pic(img_filename)
    
    @staticmethod
    def plot_bgmap(ax, bg_filename, boundary):
        
        img = plt.imread(bg_filename)
        # height, width, colors = img.shape
        
        ax.imshow(img, zorder=0, \
             extent=[boundary.min_x, boundary.max_x, \
                     boundary.min_y, boundary.max_y])