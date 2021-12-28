import unittest

import numpy as np
import pandas as pd
from pandas._testing.asserters import assert_series_equal
from pandas.testing import assert_frame_equal


class JURCoreTest(unittest.TestCase):
    def test_load_jur_db(self):

        # module import
        from src.jur import JUR
        from src.constants import TEST_PATH

        # arrange
        expected = pd.read_excel(TEST_PATH)

        # act
        jur = JUR(TEST_PATH)
        actual = jur.load_jur_db()

        # assert
        assert_frame_equal(expected, actual)

    def test_clean_jur_db_rows(self):
        # module import
        from src.jur import JUR
        from src.constants import (
            CAPACITY_BIN,
            CAPACITY_LABEL,
            COLS_TO_MAP,
            TEST_PATH,
        )

        # arrange
        expected = pd.read_excel(TEST_PATH).shape[0]

        # act
        jur = JUR(TEST_PATH)
        jur_db = jur.load_jur_db()
        actual = jur.clean_jur_db(
            jur_db, COLS_TO_MAP, CAPACITY_BIN, CAPACITY_LABEL
        ).shape[0]

        # assert
        self.assertEqual(expected, actual)

    def test_update_jur_db_to_plot_range(self):
        # module import
        from src.jur import JUR
        from src.constants import (
            CAPACITY_BIN,
            CAPACITY_LABEL,
            COLS_TO_MAP,
            QUESTIONS_TO_MAP,
            TEST_PATH,
        )

        # act
        jur = JUR(TEST_PATH)
        jur_db = jur.load_jur_db()
        jur_db_cleaned = jur.clean_jur_db(
            jur_db, COLS_TO_MAP, CAPACITY_BIN, CAPACITY_LABEL
        )
        actual = jur.update_jur_db_to_plot(
            jur_db_cleaned,
            QUESTIONS_TO_MAP,
            calc_mode="mean",
            only_effective_survey=False,
        )

        # assert
        self.assertTrue(actual["rating"].between(0, 10).any())


if __name__ == "__main__":
    unittest.main()
