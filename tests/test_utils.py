import unittest
from unittest.mock import patch
from unittest.mock import MagicMock
import numpy as np
from chart_ipynb import utils

class TestUtils(unittest.TestCase):

    def test_clean_dict(self):
        test2 = np.array([1.0,3.0])
        test2.astype(np.floating)
        result = utils.clean_dict(test1=np.array([1,2,3]),
                                  test2=test2[0],
                                  test3=(1,2))
        expected_result = {'test1': [1, 2, 3], 
                            'test2': 1.0, 
                            'test3': [1, 2]}
        self.assertEqual(result, expected_result)

    def test_config(self):
        utils.config()

    def test_color_rgb(self):
        mock_name = {'color1':[1,2,3]}
        utils.colorName = mock_name
        self.assertRaises(ValueError, lambda: utils.color_rgb([12]))
        self.assertRaises(KeyError,lambda:utils.color_rgb('test'))
        result = utils.color_rgb('color1')
        self.assertEqual(result, 'rgb(1, 2, 3, 1.000000)')