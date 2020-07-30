import unittest
from unittest.mock import patch
from unittest.mock import MagicMock

from chart_ipynb import chart_framework, line, bar, utils
from chart_ipynb import time_series
import jp_proxy_widget
import pandas as pd
import numpy as np

class TestTimeSeries(unittest.TestCase):

    def test_data_format(self):
        date_val = np.array(['2020-01-02','2020-01-03','2020-01-04'])
        case_val = np.array([1,2,3])
        df = pd.DataFrame({'Date':date_val,
                           'cases':case_val})
        val, label = time_series.data_format(df, 'cases', data_provide=True, date_col='Date')
        self.assertEqual(val, list(case_val))
        self.assertEqual(label, list(date_val))

        val, label = time_series.data_format(df, 'cases')
        self.assertEqual(val, list(case_val))
        self.assertEqual(label, list(date_val))

        mock_global_label = ['2020-01-01','2020-01-02','2020-01-03','2020-01-04']
        time_series.global_label = mock_global_label
        val, label = time_series.data_format(df, 'cases', data_provide=True, date_col='Date')
        self.assertEqual(val, [0, 1, 2, 3])
        self.assertEqual(label, mock_global_label)

    @patch("chart_ipynb.utils.axes")
    def test_default_axis(self, mock_axes):
        x_axis = time_series.default_axis('x')
        y_axis = time_series.default_axis('y')
        assert mock_axes.called

        multi_axis = time_series.default_axis('y', multi_axis = True)
        assert mock_axes.called
        assert len(multi_axis)==2

        stack_axis = time_series.default_axis('y', stacked = True)
        assert stack_axis['stacked']

    @patch("chart_ipynb.utils.options")
    @patch("chart_ipynb.utils.axes")
    def test_ts_default_option(self, mock_options, mock_axes):
        time_series.ts_default_option()
        time_series.ts_default_option(stacked=True)
        time_series.ts_default_option(log_axis=True)
        assert mock_options.called
        assert mock_axes.called

    @patch("chart_ipynb.line")
    @patch("chart_ipynb.bar")
    @patch("chart_ipynb.time_series.ts_default_option")
    def test_time_series_Chart(self, mock_line, mock_bar,
                            mock_default_option):
        date_val = np.array(['2020-01-02','2020-01-03','2020-01-04'])
        case_val = np.array([1,2,3])
        df = pd.DataFrame({'Date':date_val,
                           'cases':case_val})
        time_series.time_series_Chart('line', 'test','cases',
                                    date_col='Date',
                                    backgroundColor='red',
                                    data_provide = True,
                                    input_dataset=[df])
        time_series.time_series_Chart('line', ['test1','test2'],'cases',
                                    date_col='Date',
                                    borderColor='red',
                                    data_provide = True,
                                    input_dataset=[df,df],
                                    multi_axis=True)
        time_series.time_series_Chart('bar', ['test1','test2'],'cases',
                                    date_col='Date',
                                    data_provide = True,
                                    input_dataset=[df,df],
                                    stacked=True)
        self.assertRaises(ValueError, lambda:time_series.time_series_Chart('bar', ['test1','test2'],'cases',
                                    date_col='Date',
                                    data_provide = True))
        self.assertRaises(ValueError, lambda:time_series.time_series_Chart('line', 'test1','cases',
                                    date_col='Date',
                                    data_provide = True,
                                    input_dataset=[df,df],
                                    multi_axis=True))
        arguments = []
        def mock_reader(*args,**kwargs):
            arguments.append(args)
        def mock_data_format(*args,**kwargs):
            if args:
                arguments.append(args)
            if kwargs:
                arguments.append(kwargs)
            return list(case_val), list(date_val)
        import pandas_datareader
        pandas_datareader.data.DataReader = mock_reader
        time_series.data_format = mock_data_format
        time_series.time_series_Chart('line', ['AAPL','GOOGL'],'Open',
                                        start='2017-03-01',
                                        end='2017-04-01')
        assert arguments
        
