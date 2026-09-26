import unittest
import numpy as np
import cv2
import os
import sys

# Add parent directory to path so tests can import photobooth.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from photobooth import overlay

class TestPhotobooth(unittest.TestCase):

    def setUp(self):
        """Create mock image arrays for testing without external files or camera."""
        # 100x100 3-channel BGR frame (solid black)
        self.mock_bg = np.zeros((100, 100, 3), dtype=np.uint8)

        # 100x100 4-channel BGRA overlay (solid red with 50% transparency alpha=128)
        self.mock_overlay = np.zeros((100, 100, 4), dtype=np.uint8)
        self.mock_overlay[:, :, 2] = 255  # Red channel
        self.mock_overlay[:, :, 3] = 128  # Alpha channel (50% opaque)

    def test_overlay_shape(self):
        """Test that the transparent overlay output maintains background dimensions."""
        result = overlay(self.mock_bg, self.mock_overlay)
        self.assertEqual(result.shape, self.mock_bg.shape)

    def test_overlay_blending(self):
        """Test that semi-transparent pixels properly alter the background color."""
        result = overlay(self.mock_bg, self.mock_overlay)
        # Red channel on blended output should be ~128 (50% of 255)
        self.assertGreater(result[50, 50, 2], 0)


if __name__ == '__main__':
    unittest.main()