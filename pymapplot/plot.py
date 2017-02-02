import numpy as np
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
        pic_height = glob.PIC_WIDTH / boundary.ratio()
        
        print "Width:", glob.PIC_WIDTH, "Height:",pic_height
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
        plt.savefig(img_filename, bbox_inches='tight', dpi=glob.MY_DPI)
    
    @staticmethod
    def plot_graph(lines, boundary, img_filename, line_color='red', 
        bg_filename=None, bg_lines=None, linewidth=1, bg_line_color="grey",
        off_axis=True, points=[], labels=[], pt_size=1, pt_color="black"):
        
        ax = Plot.get_a_ax(boundary)
        Plot.format_ax(ax, boundary)
        
        # if off_axis:
        #     ax.axis('off')
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        
        # plot an image
        if bg_filename:
            Plot.plot_bgmap(ax, bg_filename, boundary)
        
        if bg_lines:
            ax.add_collection(LineCollection(bg_lines, color=bg_line_color, 
                              linewidth=linewidth))
        
        ax.add_collection(LineCollection(lines, color=line_color, 
                          linewidth=linewidth))
        
        Plot.plot_points(ax, points, labels, pt_size=pt_size, pt_color=pt_color)
        
        Plot.save_pic(img_filename)
    
    @staticmethod
    def plot_bgmap(ax, bg_filename, b):
        
        img = plt.imread(bg_filename)
        # height, width, colors = img.shape
        
        ax.imshow(img, zorder=0, 
             extent=[b.x_range.min, b.x_range.max, 
                     b.y_range.min, b.y_range.max], aspect=1.33)
    
    @staticmethod
    def scatter_points(ax, points, color='blue', size=1, zorder=1, alpha=1):
        # print type(points)
        # print points[0]
        # print type(points) == 'numpy.ndarray'
        # if type(points) == 'numpy.ndarray':
        #     points = points.tolist()
        #     print "TEST"
        #     print points[0], type(points[0])
        x = [p[0] for p in points]
        y = [p[1] for p in points]
        
        ax.scatter(x, y, s=size, c=color, edgecolor='', zorder=zorder, alpha=alpha)
        # ax.scatter(x, y, s=size, c=color, edgecolor='black', zorder=zorder, alpha=alpha)
    
    
    @staticmethod
    def plot_points(ax, gps_points, labels, pt_color="black", pt_size=1):
        
        np.random.seed(21)
        
        if len(labels) == 0:
            Plot.scatter_points(ax, gps_points, color=pt_color, size=pt_size, zorder=2)
        else:
            unique_labels = set(labels)
            print "len unique_labels:", len(unique_labels)
            colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
            
            # print "prev:", colors
            np.random.shuffle(colors)
            # print "after:", colors
        
            X = np.array(gps_points)
            Y = np.array(labels)
        
            # plot original GPS points
            Plot.scatter_points(ax, X, color='k', size=pt_size, zorder=2)
        
            for k, col in zip(unique_labels, colors):
                if k < 0:
                    # Black used for noise.
                    col = 'k'
                    continue
                
                xy = X[Y == k]
                Plot.scatter_points(ax, xy, color=col, size=pt_size, zorder=2)