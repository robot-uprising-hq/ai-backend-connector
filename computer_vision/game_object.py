import numpy as np
import cv2
import shapely
from shapely.geometry import LineString, Point, Polygon


LINE_THICKNESS = 2
LINE_COLOR = (0,255,255)

class GameObject():
    def __init__(self, coordinates, line_color, circle_radius=0, name=""):
        self._coordinates = coordinates
        self._line_color = line_color
        self._circle_radius = circle_radius
        self._name = name

        # print(f'Name {name}\n')
        # print(f'Coords {coordinates}\n')
        if len(self._coordinates) is 0:
            raise Exception("No coordinates given to the new game object.")
        elif len(self._coordinates) is 1:
            self._geometry = Point(self._coordinates[0])
            if circle_radius > 0:
                # Create a circle from the point by calling the buffer method
                self._geometry = point.buffer(self._circle_radius)
                self._coordinates = np.array([self._geometry.exterior.coords], np.float)
        elif len(self._coordinates) is 2:
            self._geometry = LineString(self._coordinates)
        else:
            self._geometry = Polygon(self._coordinates)

    def draw_object_on_image(self, image):
        '''
        Draw objects boundaries to the given image. Remember to call 
        "cv2.imshow" and  "cv2.waitKey"-functions after drawing all the 
        objects you want.
        '''
        if isinstance(self._geometry, Point):
            # Highlight single point with a bigger point on image
            line_thickness = LINE_THICKNESS + 10
        else:
            line_thickness = LINE_THICKNESS
        pts = np.array([self._coordinates], np.int32)
        pts = pts.reshape((-1,1,2))
        # print(f'pts: {pts}')
        cv2.polylines(image, [pts], True, self._line_color, line_thickness)

    @property
    def coords(self):
        return self._geometry.coords

    def distance(self, other_game_object):
        return self._geometry.distance(other_game_object)
    
    def intersection(self, other_game_object):
        return self._geometry.intersection(other_game_object)

    def intersects(self, other_game_object):
        return self._geometry.intersects(other_game_object)
