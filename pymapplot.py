from plot import Plot
from staticmap import StaticMap
from boundary import Boundary

boundary = Boundary(-87.69215,-87.634896,41.858952,41.886565)
# StaticMap.download("chicago.png", boundary, zoom=14)

# Plot.plot_graph_with_bgmap([], "chicago.png", boundary, "pymapplot.png")

StaticMap.get_map("chicago.png")