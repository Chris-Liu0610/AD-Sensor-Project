from typing import Dict, Optional, Union
import numpy as np
from facial_landmarks import (
    RIGHT_LINE_INDICES,
    LEFT_LINE_INDICES,
    RIGHT_TRIANGLE_INDICES,
    LEFT_TRIANGLE_INDICES,
)


def evaluate_length_asymmetry_scores(landmarks: np.ndarray) -> np.ndarray:
    """
    Compute asymmetry scores by comparing line lengths between right and left sides.

    Parameters
    ----------
    landmarks : numpy.ndarray
        Facial landmarks array with shape (N, 3) where N is the number of points.

    Returns
    -------
    numpy.ndarray
        Array of normalized length asymmetry scores
    """
    # Extract line landmarks for both sides
    right_lines = landmarks[RIGHT_LINE_INDICES]
    left_lines = landmarks[LEFT_LINE_INDICES]

    # Calculate line lengths
    right_line_lengths = np.linalg.norm(right_lines[:, 0] - right_lines[:, 1], axis=1)
    left_line_lengths = np.linalg.norm(left_lines[:, 0] - left_lines[:, 1], axis=1)

    # Compute normalized differences
    length_diff_numerator = np.abs(right_line_lengths - left_line_lengths)
    length_diff_denominator = np.abs(right_line_lengths + left_line_lengths)
    
    # Avoid division by zero
    length_diff_denominator = np.maximum(length_diff_denominator, 1e-10)
    
    normalized_length_diffs = length_diff_numerator / length_diff_denominator

    return normalized_length_diffs


def evaluate_area_asymmetry_scores(landmarks: np.ndarray) -> np.ndarray:
    """
    Compute asymmetry scores by comparing triangle areas between right and left sides.

    Parameters
    ----------
    landmarks : numpy.ndarray
        Facial landmarks array with shape (N, 3) where N is the number of points.

    Returns
    -------
    numpy.ndarray
        Array of normalized area asymmetry scores
    """
    # Extract triangle landmarks for both sides
    right_triangles = landmarks[RIGHT_TRIANGLE_INDICES]
    left_triangles = landmarks[LEFT_TRIANGLE_INDICES]

    # Calculate vectors for triangle sides
    right_vec1 = right_triangles[:, 1] - right_triangles[:, 0]
    right_vec2 = right_triangles[:, 2] - right_triangles[:, 0]

    left_vec1 = left_triangles[:, 1] - left_triangles[:, 0]
    left_vec2 = left_triangles[:, 2] - left_triangles[:, 0]

    # Calculate cross products to get area
    right_cross_product = np.cross(right_vec1, right_vec2)
    left_cross_product = np.cross(left_vec1, left_vec2)

    # Handle case when cross product is a 1D array
    if len(right_cross_product.shape) == 1:
        right_cross_product = np.expand_dims(right_cross_product, axis=1)
        left_cross_product = np.expand_dims(left_cross_product, axis=1)

    # Calculate triangle areas
    right_areas = 0.5 * np.linalg.norm(right_cross_product, axis=1)
    left_areas = 0.5 * np.linalg.norm(left_cross_product, axis=1)

    # Compute normalized differences
    area_diff_numerator = np.abs(right_areas - left_areas)
    area_diff_denominator = np.abs(right_areas + left_areas)
    
    # Avoid division by zero
    area_diff_denominator = np.maximum(area_diff_denominator, 1e-10)
    
    normalized_area_diffs = area_diff_numerator / area_diff_denominator

    return normalized_area_diffs


def evaluate_face_quality(face_obj: Union[np.ndarray, Dict]) -> Optional[float]:
    """
    Evaluate face quality based on facial landmarks.

    Parameters
    ----------
    face_obj : Union[np.ndarray, Dict]
        The input can be a numpy array of landmarks or a dictionary containing landmarks.
    
    Returns
    -------
    Optional[float]
        Overall asymmetry score between 0 and 1, where 0 indicates perfect symmetry.  
        Returns None if no face is detected.
    """

    if face_obj is None:
        return None
    
    if isinstance(face_obj, np.ndarray):
        landmarks = face_obj
    elif isinstance(face_obj, dict):
        landmarks = face_obj["landmarks"]
    else:
        raise ValueError("Invalid input type. Expected numpy array or dictionary.")
    
    # Compute length and area asymmetry scores
    length_scores = evaluate_length_asymmetry_scores(landmarks)
    area_scores = evaluate_area_asymmetry_scores(landmarks)
    
    # Calculate overall asymmetry score
    overall_score = 0.5 * (np.mean(length_scores) + np.mean(area_scores))

    return overall_score


if __name__ == "__main__":
    # Example usage
    landmarks = np.random.rand(478, 3) 
    length_scores = evaluate_length_asymmetry_scores(landmarks)
    area_scores = evaluate_area_asymmetry_scores(landmarks)

    assert length_scores.shape == (len(RIGHT_LINE_INDICES),)
    assert area_scores.shape == (len(RIGHT_TRIANGLE_INDICES),)
    print("Passed shape tests!")

    assert np.all(length_scores >= 0) and np.all(length_scores <= 1)
    assert np.all(area_scores >= 0) and np.all(area_scores <= 1)
    print("Passed value range tests!")

    overall_score = evaluate_face_quality(None)
    assert overall_score is None
    print("Passed None value input!")

    overall_score = evaluate_face_quality(landmarks)
    assert isinstance(overall_score, float) and 0 <= overall_score <= 1
    print("Passed numpy.array input!")

    metadata = {
        "landmarks": landmarks
    }
    overall_score = evaluate_face_quality(metadata)
    assert isinstance(overall_score, float) and 0 <= overall_score <= 1
    print("Passed dictionary input!")

    print("All tests passed!")