from scipy.spatial import distance as dist

def calculate_ear(eye_points):
    """
    eye_points: [ (x1, y1), ..., (x6, y6) ]
    EAR = (||P2 - P6|| + ||P3 - P5||) / (2 * ||P1 - P4||)
    """
    A = dist.euclidean(eye_points[1], eye_points[5])
    B = dist.euclidean(eye_points[2], eye_points[4])
    C = dist.euclidean(eye_points[0], eye_points[3])
    ear = (A + B) / (2.0 * C)
    return ear
