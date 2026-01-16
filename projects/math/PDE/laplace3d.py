import numpy as np
from pde import CartesianGrid, solve_laplace_equation
#If you want to plot the entire 4d solution import plotly and uncomment relevent section. 
#import plotly.graph_objects as go

grid = CartesianGrid([[0, 10], [0, 10], [0, 10]], 30)
bcs = {"x-": {"value": 122}, "x+": {"value": 119}, "y-": {"value": 119}, "y+": {"value": 118}, "z-": {"value": 122}, "z+": {"value": 119}}

res = solve_laplace_equation(grid, bcs)
#boundry = res.get_boundary_field("x+")

#To find an inflection point, we can observe when the second differences equal zero. 
numPoints = 288*8
diff1=[]
diff2=[]
xSnip = 1
ySnip = 9
startpoint=1
endpoint=9

zpoint=startpoint
incr = endpoint/numPoints
while zpoint < endpoint:
    diff1.append(res.interpolate([xSnip, ySnip, zpoint+1])-res.interpolate([xSnip, ySnip, zpoint]))
    zpoint+=incr
for i in range(len(diff1)-1):
    diff2.append(diff1[i+1]-diff1[i])

for i, dif in enumerate(diff2):
    if i==0:
        continue
    if dif * diff2[i-1] <0:
        print(f"Inflection found between {(i+2)*incr+2} and {(i-1)*incr+2}")

#Print the velocities
print()
print("Velocites")
print(res.interpolate([1, 9, 5.1])-res.interpolate([1, 9, 5]))
print(res.interpolate([1, 9, 5.2])-res.interpolate([1, 9, 5.1]))
print(res.interpolate([1, 9, 5.3])-res.interpolate([1, 9, 5.2]))
print(res.interpolate([1, 9, 5.4])-res.interpolate([1, 9, 5.3]))
#Velocity changes from becoming less negetive to becoming more negetive
print(res.interpolate([1, 9, 5.5])-res.interpolate([1, 9, 5.4]))
print(res.interpolate([1, 9, 5.6])-res.interpolate([1, 9, 5.5]))

#print accelerations
print()
print("Acc")
print(res.interpolate([1, 9, 5.4])-2*res.interpolate([1, 9, 5.3])+res.interpolate([1, 9, 5.2]))
print(res.interpolate([1, 9, 5.5])-2*res.interpolate([1, 9, 5.4])+res.interpolate([1, 9, 5.3]))
print(res.interpolate([1, 9, 5.6])-2*res.interpolate([1, 9, 5.5])+res.interpolate([1, 9, 5.4]))

#Evaluate estimated inflection point, which appears to be around 5.5
print()
print("Inflection point final answer: ")
print(res.interpolate([1, 9, 5.5]))
#Rounding to nearest int
print(res.interpolate([1, 9, 6]))

#Plot the solution in the desired domain and its second derivate
targLine = res.slice({'x': 1, 'y': 9})
targLine.plot()
targLine.laplace(bc=None).plot()

#More sliced plots of curious
"""
res.slice({'x': 1, 'y': 5}).plot()
res.slice({'x': 3, 'y': 5}).plot()
res.slice({'x': 5, 'y': 5}).plot()
res.slice({'x': 7, 'y': 5}).plot()
res.slice({'x': 9, 'y': 5}).plot()

res.slice({'x': 1, 'y': 1}).plot()
res.slice({'x': 3, 'y': 1}).plot()
res.slice({'x': 5, 'y': 1}).plot()
res.slice({'x': 7, 'y': 1}).plot()
res.slice({'x': 9, 'y': 1}).plot()

res.slice({'x': 1, 'y': 9}).plot()
res.slice({'x': 3, 'y': 9}).plot()
res.slice({'x': 5, 'y': 9}).plot()
res.slice({'x': 7, 'y': 9}).plot()
res.slice({'x': 9, 'y': 9}).plot()
"""
#a 4d plot of the entire solution in plotly
"""
# 2) set up the mesh coordinates
x, y, z = grid.axes_coords
X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

# 3) create a Volume trace
vol = go.Volume(
    x=X.flatten(), y=Y.flatten(), z=Z.flatten(),
    value=res.data.flatten(),
    isomin=res.data.min(),      # lower bound for rendering
    isomax=res.data.max(),      # upper bound
    opacity=0.1,                # overall opacity
    surface_count=20,           # number of “layers” of surfaces
    colorscale='Viridis',       # the colormap
)

fig = go.Figure(vol)
fig.update_layout(scene=dict(
    xaxis_title='x', yaxis_title='y', zaxis_title='z'
))
fig.show()
"""

#Further analysis of points
"""
print(res.interpolate([1, 9, 1]))
print(res.interpolate([1, 9, 2]))
print(res.interpolate([1, 9, 3]))
print(res.interpolate([1, 9, 4]))
print(res.interpolate([1, 9, 5]))
print(res.interpolate([1, 9, 6]))
print(res.interpolate([1, 9, 7]))
print(res.interpolate([1, 9, 8]))
print(res.interpolate([1, 9, 9]))

print(res.interpolate([1, 9, 2])-res.interpolate([1, 9, 1]))
print(res.interpolate([1, 9, 3])-res.interpolate([1, 9, 2]))
print(res.interpolate([1, 9, 4])-res.interpolate([1, 9, 3]))
print(res.interpolate([1, 9, 5])-res.interpolate([1, 9, 4]))
print(res.interpolate([1, 9, 6])-res.interpolate([1, 9, 5]))
print(res.interpolate([1, 9, 7])-res.interpolate([1, 9, 6]))
print(res.interpolate([1, 9, 8])-res.interpolate([1, 9, 7]))
print(res.interpolate([1, 9, 9])-res.interpolate([1, 9, 8]))
"""