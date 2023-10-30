# import matplotlib

# matplotlib.use("TkAgg")  # Use a different backend (e.g., TkAgg)
import matplotlib.pyplot as plt

# # Define your list of points (x, y coordinates)

# # Add the first point at the end to close the shape
# points.append(points[0])

# # Extract x and y coordinates from the points
# x, y = zip(*points)

# # Create a plot
# plt.plot(x, y)

# # Optionally fill the shape with a color
# plt.fill(x, y, "b", alpha=0.2)  # 'b' stands for blue, you can change it
# # plt.savefig("output_plot.png")  # Save the plot to a file

# # Show the plot
# plt.show()
# Define your list of unordered points (x, y coordinates)
# points = [(3, 4), (7, 11), (1, 2), (5, 6)]

# Sort the points based on their x or y coordinates, depending on your desired order
# For example, you can sort by x-coordinate to connect points from left to right
# points.sort(key=lambda p: p[0])

# Add the first point at the end to close the shape
# points.append(points[0])

# # Extract x and y coordinates from the points
# x, y = zip(*points)

# # Create a plot
# # plt.plot(x, y)
# plt.plot(x, y, marker="o")  # 'o' specifies that points should be marked

# # Optionally fill the shape with a color
# plt.fill(x, y, "b", alpha=0.2)  # 'b' stands for blue, you can change it


import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
import numpy as np

points = [
    (5, 0),
    (0, 4),
    (5, 4),
    (0, 0),
    (-1, 8),
]

# Define your list of points (x, y coordinates)
# points = [(1, 2), (3, 4), (5, 6), (7, 8)]

# Convert the points to a NumPy array for compatibility with ConvexHull
points_array = np.array(points)

# Calculate the convex hull
hull = ConvexHull(points_array)

# Extract the vertices of the convex hull
hull_points = points_array[hull.vertices]

# Close the shape by adding the first point at the end
hull_points = np.append(hull_points, [hull_points[0]], axis=0)

# Extract x and y coordinates from the hull points
x, y = zip(*hull_points)

# Create a plot
plt.plot(x, y, marker="o")


# Show the plot
plt.savefig("output_plot2.png")  # Save the plot to a file
