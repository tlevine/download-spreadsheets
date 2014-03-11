from io import StringIO

import nose.tools as n

from featured_spreadsheets.examine import unique_indices

def test_unique_indices():
    fp = StringIO('a;b;c;d\r\n3;4;5;6')
    observed = unique_indices(fp, 'url is just for logging')
    expected = {('a','b','c'),('b','c','d')} # only adjacent, max 3
    n.assert_set_equal(observed, expected)
