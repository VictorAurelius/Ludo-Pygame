"""
Geometry utility module providing common geometric calculations and collision detection.
"""

from typing import Tuple, List, Optional
import math
import pygame
from pygame import Rect

Point = Tuple[float, float]
Vector = Tuple[float, float]

def distance(p1: Point, p2: Point) -> float:
    """
    Calculate Euclidean distance between two points
    
    Args:
        p1: First point (x, y)
        p2: Second point (x, y)
        
    Returns:
        float: Distance between points
    """
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def manhattan_distance(p1: Point, p2: Point) -> float:
    """
    Calculate Manhattan distance between two points
    
    Args:
        p1: First point (x, y)
        p2: Second point (x, y)
        
    Returns:
        float: Manhattan distance between points
    """
    return abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])

def normalize_vector(vector: Vector) -> Vector:
    """
    Normalize a vector to unit length
    
    Args:
        vector: Vector to normalize (x, y)
        
    Returns:
        Vector: Normalized vector
    """
    magnitude = math.sqrt(vector[0]**2 + vector[1]**2)
    if magnitude == 0:
        return (0, 0)
    return (vector[0]/magnitude, vector[1]/magnitude)

def vector_to_angle(vector: Vector) -> float:
    """
    Convert a vector to an angle in degrees
    
    Args:
        vector: Vector (x, y)
        
    Returns:
        float: Angle in degrees
    """
    return math.degrees(math.atan2(vector[1], vector[0]))

def angle_to_vector(angle: float) -> Vector:
    """
    Convert an angle in degrees to a unit vector
    
    Args:
        angle: Angle in degrees
        
    Returns:
        Vector: Unit vector in that direction
    """
    radians = math.radians(angle)
    return (math.cos(radians), math.sin(radians))

def interpolate_points(p1: Point, p2: Point, steps: int) -> List[Point]:
    """
    Generate intermediate points between two points
    
    Args:
        p1: Start point (x, y)
        p2: End point (x, y)
        steps: Number of intermediate points
        
    Returns:
        List[Point]: List of interpolated points including start and end
    """
    points = []
    for i in range(steps + 1):
        t = i / steps
        x = p1[0] + (p2[0] - p1[0]) * t
        y = p1[1] + (p2[1] - p1[1]) * t
        points.append((x, y))
    return points

def rect_from_center(center: Point, size: Tuple[float, float]) -> Rect:
    """
    Create a Rect with specified center and size
    
    Args:
        center: Center point (x, y)
        size: Size (width, height)
        
    Returns:
        Rect: Rectangle with specified center and size
    """
    return Rect(
        center[0] - size[0]/2,
        center[1] - size[1]/2,
        size[0],
        size[1]
    )

def point_in_rect(point: Point, rect: Rect) -> bool:
    """
    Check if a point is inside a rectangle
    
    Args:
        point: Point to check (x, y)
        rect: Rectangle to check against
        
    Returns:
        bool: True if point is inside rectangle
    """
    return rect.collidepoint(point)

def rect_overlap(rect1: Rect, rect2: Rect) -> bool:
    """
    Check if two rectangles overlap
    
    Args:
        rect1: First rectangle
        rect2: Second rectangle
        
    Returns:
        bool: True if rectangles overlap
    """
    return rect1.colliderect(rect2)

def get_overlap_area(rect1: Rect, rect2: Rect) -> Optional[Rect]:
    """
    Get the overlapping area between two rectangles
    
    Args:
        rect1: First rectangle
        rect2: Second rectangle
        
    Returns:
        Optional[Rect]: Overlapping area or None if no overlap
    """
    if not rect_overlap(rect1, rect2):
        return None
        
    x1 = max(rect1.left, rect2.left)
    y1 = max(rect1.top, rect2.top)
    x2 = min(rect1.right, rect2.right)
    y2 = min(rect1.bottom, rect2.bottom)
    
    return Rect(x1, y1, x2 - x1, y2 - y1)

def get_direction(p1: Point, p2: Point) -> Vector:
    """
    Get direction vector from p1 to p2
    
    Args:
        p1: Start point (x, y)
        p2: End point (x, y)
        
    Returns:
        Vector: Normalized direction vector
    """
    return normalize_vector((p2[0] - p1[0], p2[1] - p1[1]))

def rotate_point(point: Point, center: Point, angle: float) -> Point:
    """
    Rotate a point around a center point by an angle
    
    Args:
        point: Point to rotate (x, y)
        center: Center of rotation (x, y)
        angle: Angle in degrees
        
    Returns:
        Point: Rotated point
    """
    radians = math.radians(angle)
    cos_a = math.cos(radians)
    sin_a = math.sin(radians)
    
    dx = point[0] - center[0]
    dy = point[1] - center[1]
    
    x = center[0] + (dx * cos_a - dy * sin_a)
    y = center[1] + (dx * sin_a + dy * cos_a)
    
    return (x, y)

def get_bounding_circle(rect: Rect) -> Tuple[Point, float]:
    """
    Get the bounding circle of a rectangle
    
    Args:
        rect: Rectangle
        
    Returns:
        Tuple[Point, float]: Center point and radius
    """
    center = rect.center
    radius = math.sqrt(rect.width**2 + rect.height**2) / 2
    return (center, radius)

def circle_collision(center1: Point, radius1: float,
                    center2: Point, radius2: float) -> bool:
    """
    Check if two circles collide
    
    Args:
        center1: Center of first circle (x, y)
        radius1: Radius of first circle
        center2: Center of second circle (x, y)
        radius2: Radius of second circle
        
    Returns:
        bool: True if circles collide
    """
    return distance(center1, center2) <= radius1 + radius2

def clamp_point_to_rect(point: Point, rect: Rect) -> Point:
    """
    Clamp a point to stay within a rectangle
    
    Args:
        point: Point to clamp (x, y)
        rect: Rectangle boundaries
        
    Returns:
        Point: Clamped point
    """
    x = max(rect.left, min(rect.right, point[0]))
    y = max(rect.top, min(rect.bottom, point[1]))
    return (x, y)

def get_rect_points(rect: Rect) -> List[Point]:
    """
    Get the corner points of a rectangle
    
    Args:
        rect: Rectangle
        
    Returns:
        List[Point]: List of corner points
    """
    return [
        (rect.left, rect.top),
        (rect.right, rect.top),
        (rect.right, rect.bottom),
        (rect.left, rect.bottom)
    ]