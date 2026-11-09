
import os
import tempfile
import unittest

from adsdata.diffs import Diff
from adsdata.file_defs import data_files_CC


class TestDiffs(unittest.TestCase):
    """test computing changed bibcodes"""

    def test_CC_new_input_file(self):
        """a CitationCapture input file not yet in previous/ is initialized empty and all its bibcodes are changed"""
        with tempfile.TemporaryDirectory() as root_dir:
            for x in data_files_CC:
                for d in ['current', 'previous']:
                    os.makedirs(os.path.dirname(os.path.join(root_dir, d, data_files_CC[x]['path'])), exist_ok=True)
                with open(os.path.join(root_dir, 'current', data_files_CC[x]['path']), 'w'):
                    pass
            with open(os.path.join(root_dir, 'current', data_files_CC['canonical']['path']), 'w') as f:
                f.write('2017zndo....240895I\n2018zndo....000000X\n')
            with open(os.path.join(root_dir, 'current', data_files_CC['author']['path']), 'w') as f:
                f.write('2017zndo....240895I\tIlma, R\n')

            Diff._compute_changed_bibcodes(root_dir=root_dir, CC_records=True)

            self.assertTrue(os.path.isfile(os.path.join(root_dir, 'previous', data_files_CC['author']['path'])))
            with open(os.path.join(root_dir, 'current', data_files_CC['author']['path'] + '.changedbibs')) as f:
                self.assertEqual('2017zndo....240895I\n', f.read())
