import os
import sys
import unittest
from unittest.mock import MagicMock, patch

import numpy as np

# Add parent directory to path so tests can import photobooth.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from photobooth import ensure_model_exists, overlay, process_frame


class TestPhotobooth(unittest.TestCase):
    def setUp(self):
        """Create mock image arrays for testing"""
        # 100x100 3-channel BGR frame (solid black)
        self.mock_bg = np.zeros((100, 100, 3), dtype=np.uint8)

        # 100x100 4-channel BGRA overlay (solid red with 50% transparency alpha=128)
        self.mock_overlay = np.zeros((100, 100, 4), dtype=np.uint8)
        self.mock_overlay[:, :, 2] = 255  # Red channel
        self.mock_overlay[:, :, 3] = 255  # Alpha channel (50% opaque)

    def test_overlay_shape(self):
        """Test overlay output maintains background dimensions."""
        result = overlay(self.mock_bg, self.mock_overlay)
        self.assertEqual(result.shape, self.mock_bg.shape)

    def test_overlay_blending(self):
        """Test alpha blending changes pixel color values."""
        result = overlay(self.mock_bg, self.mock_overlay)
        self.assertEqual(result[50, 50, 2], 255)

    def test_overlay__without_alpha(self):
        """Verify fallback behavior when overlay has no alpha channel (BGR instead of BGRA)."""
        bgr_overlay = np.zeros((100, 100, 3), dtype=np.uint8)
        result = overlay(self.mock_bg, bgr_overlay)
        np.testing.assert_array_equal(result, self.mock_bg)

    @patch("photobooth.os.path.exists")
    @patch("photobooth.urllib.request.urlretrieve")
    def test_ensure_model_downloads_when_missing(self, mock_urlretrieve, mock_exists):
        """Verify model downloads automatically when missing."""
        mock_exists.return_value = False
        ensure_model_exists()
        mock_urlretrieve.assert_called_once()

    @patch("photobooth.os.path.exists")
    @patch("photobooth.urllib.request.urlretrieve")
    def test_ensure_model_dowload_skips_when_present(self, mock_urlretrieve, mock_exists):
        """Verify download is skipped if model already exists on disk."""
        mock_exists.return_value = True
        ensure_model_exists()
        mock_urlretrieve.assert_not_called()

    @patch("mediapipe.Image")
    def test_process_frame_layer_compositing(self, mock_mp_image):
        """Verify human foreground pixels are preserved and background replaced."""
        mock_segmentor = MagicMock()
        mock_mask_data = np.ones((100, 100, 1), dtype=np.uint8)
        mock_mask_data[25:75, 25:75, 0] = 0  # Person class ID

        mock_category_mask = MagicMock()
        mock_category_mask.numpy_view.return_value = mock_mask_data

        mock_result = MagicMock()
        mock_result.category_mask = mock_category_mask
        mock_segmentor.segment.return_value = mock_result

        output = process_frame(self.mock_bg, self.mock_overlay, mock_segmentor)

        self.assertEqual(output.shape, (100, 100, 3))
        # Center (human) should remain black
        np.testing.assert_array_equal(output[50, 50], [0, 0, 0])
        # Background should be red (from monster overlay)
        np.testing.assert_array_equal(output[0, 0], [0, 0, 255])


if __name__ == "__main__":
    unittest.main()
