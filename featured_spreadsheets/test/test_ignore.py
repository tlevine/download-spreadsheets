import nose.tools as n

from featured_spreadsheets.ignore import ignore

def test_ignore_opendatasoft_geom():
    'Geoms should be ignored because they\'re too big.'
    dataset = {"fields": [{"label": "Geometry X Y", "type": "geo_point_2d", "name": "geom_x_y"}, {"label": "Geometry Name", "type": "text", "name": "geom_name"},  {"label": "Geometry", "type": "geo_shape", "name": "geom"}]}
    n.assert_true(ignore(dataset))
