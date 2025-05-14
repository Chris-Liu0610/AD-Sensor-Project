from dataclasses import dataclass
from typing import Optional
import mediapipe as mp
import numpy as np


@dataclass
class FaceMeshResult:
    """
    A data class to hold the results of face detection.
    """
    image_size: tuple
    bounding_box: tuple
    face_ratio: float
    landmarks: np.ndarray


class FaceMeshExtractor:
    """
    A class to extract facial landmarks using MediaPipe Face Mesh.
    """

    def __init__(
        self,
        static_image_mode: bool = True,
        refine_landmarks: bool = True,
        max_num_faces: int = 1,
        min_detection_confidence: float = 0.5,
    ) -> None:
        """
        Initializes the FaceMeshExtractor with MediaPipe Face Mesh model.
        """
        self._face_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=static_image_mode,
            refine_landmarks=refine_landmarks,
            max_num_faces=max_num_faces,
            min_detection_confidence=min_detection_confidence
        )

    def _extract(self, image: np.ndarray) -> Optional[np.ndarray]:
        """
        Extract facial landmarks using MediaPipe Face Mesh.

        Parameters
        ----------
        image : np.ndarray
            The input image in RGB format.
        
        Returns
        -------
        Optional[np.ndarray]
            Facial landmarks as a numpy array of shape (478, 3), where:
            - Each row represents a landmark point (x, y, z)
            - Points 468-477 represent iris landmarks   
            Returns None if no face is detected.
        """
        results = self._face_mesh.process(image)
        
        if not results.multi_face_landmarks:
            return None 

        # Get the first detected face
        face_landmarks = results.multi_face_landmarks[0]

        # Extract landmark coordinates
        landmarks = np.zeros((len(face_landmarks.landmark), 3), dtype=np.float32)
        for i, landmark in enumerate(face_landmarks.landmark):
            landmarks[i] = (landmark.x, landmark.y, landmark.z)

        return landmarks

    def extract(self, image: np.ndarray) -> Optional[FaceMeshResult]:
        """
        Extract facial landmarks along with bounding box and face ratio.

        Parameters
        ----------
        image : np.ndarray
            The input image in RGB format.
        
        Returns
        -------
        Optional[FaceMeshResult]
            A FaceMeshResult object containing:
            - image_size: Size of the input image (width, height)
            - bounding_box: Bounding box coordinates (x1, y1, x2, y2)
            - face_ratio: Ratio of face area to image area
            - landmarks: Facial landmarks as a numpy array of shape (478, 3)   
            Returns None if no face is detected.
        """
        landmarks = self._extract(image)
        
        if landmarks is None:
            return None
        
        # Calculate bounding box
        ih, iw = image.shape[:2]
        x1 = int(np.min(landmarks[:, 0]) * iw)
        y1 = int(np.min(landmarks[:, 1]) * ih)
        x2 = int(np.max(landmarks[:, 0]) * iw)
        y2 = int(np.max(landmarks[:, 1]) * ih)

        # Convert normalized coordinates to pixel values
        bbox_width = x2 - x1
        bbox_height = y2 - y1
        face_area = bbox_width * bbox_height
        image_area = iw * ih
        face_ratio = face_area / image_area
        
        return FaceMeshResult(
            image_size=(iw, ih),
            bounding_box=(x1, y1, x2, y2),
            face_ratio=face_ratio,
            landmarks=landmarks
        )


if __name__ == "__main__":

    # Initialize the FaceMeshExtractor
    face_mesh_extractor = FaceMeshExtractor()

    dummy_img = np.zeros((480, 640, 3), dtype=np.uint8)  # Dummy image for testing

    # Extract facial landmarks
    landmarks = face_mesh_extractor._extract(dummy_img)

    assert landmarks is None
    print("Dummy image test passed. No face detected as expected.")

    metadata = face_mesh_extractor.extract(dummy_img)
    assert metadata is None
    print("Dummy image test with metadata passed. No face detected as expected.")

    print("All tests passed.")

