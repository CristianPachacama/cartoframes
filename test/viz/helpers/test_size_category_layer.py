import unittest
try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock
from cartoframes.viz import helpers, Source


class TestSizeCategoryLayerHelper(unittest.TestCase):
    def setUp(self):
        self.orig_compute_query_bounds = Source._compute_query_bounds
        Source._compute_query_bounds = Mock(return_valye=None)

    def tearDown(self):
        Source._compute_query_bounds = self.orig_compute_query_bounds

    def test_helpers(self):
        "should be defined"
        self.assertNotEqual(helpers.size_category_layer, None)

    def test_size_category_layer(self):
        "should create a layer with the proper attributes"
        Source._get_geom_type = Mock(return_value='point')

        layer = helpers.size_category_layer(
            source='sf_neighborhoods',
            value='name',
            title='Neighborhoods'
        )

        self.assertNotEqual(layer.style, None)
        self.assertEqual(layer.style._style['point']['width'], 'ramp(top($name, 5), [2, 20])')
        self.assertEqual(layer.style._style['line']['width'], 'ramp(top($name, 5), [1, 10])')
        self.assertEqual(layer.style._style['point']['color'], 'opacity(#F46D43, 0.8)')
        self.assertEqual(layer.style._style['line']['color'], 'opacity(#4CC8A3, 0.8)')
        self.assertNotEqual(layer.popup, None)
        self.assertEqual(layer.popup._hover, [{
            'title': 'Neighborhoods',
            'value': '$name'
        }])

        self.assertNotEqual(layer.legend, None)
        self.assertEqual(layer.legend._type['point'], 'size-category-point')
        self.assertEqual(layer.legend._type['line'], 'size-category-line')
        self.assertEqual(layer.legend._title, 'Neighborhoods')
        self.assertEqual(layer.legend._description, '')
        self.assertEqual(layer.legend._footer, '')

    def test_size_category_layer_point(self):
        "should create a point type layer"
        layer = helpers.size_category_layer(
            'sf_neighborhoods',
            'name',
            'Neighborhoods',
            top=5,
            size=[10, 20],
            color='blue'
        )

        self.assertEqual(
            layer.style._style['point']['width'],
            'ramp(top($name, 5), [10, 20])'
        )
        self.assertEqual(
            layer.style._style['point']['color'],
            'opacity(blue, 0.8)'
        )

        layer = helpers.size_category_layer(
            'sf_neighborhoods',
            'name',
            'Neighborhoods',
            cat=['A', 'B'],
            size=[10, 20],
            color='blue'
        )

        self.assertEqual(
            layer.style._style['point']['width'],
            "ramp(buckets($name, ['A', 'B']), [10, 20])"
        )
        self.assertEqual(
            layer.style._style['point']['color'],
            'opacity(blue, 0.8)'
        )

    def test_size_category_layer_line(self):
        "should create a line type layer"
        Source._get_geom_type = Mock(return_value='line')

        layer = helpers.size_category_layer(
            'sf_neighborhoods',
            'name',
            'Neighborhoods',
            top=5,
            size=[10, 20],
            color='blue'
        )

        self.assertEqual(
            layer.style._style['line']['width'],
            'ramp(top($name, 5), [10, 20])'
        )
        self.assertEqual(
            layer.style._style['line']['color'],
            'opacity(blue, 0.8)'
        )

        layer = helpers.size_category_layer(
            'sf_neighborhoods',
            'name',
            'Neighborhoods',
            cat=['A', 'B'],
            size=[10, 20],
            color='blue'
        )

        self.assertEqual(
            layer.style._style['line']['width'],
            "ramp(buckets($name, ['A', 'B']), [10, 20])"
        )
        self.assertEqual(
            layer.style._style['line']['color'],
            'opacity(blue, 0.8)'
        )

    def test_size_category_layer_legend(self):
        "should show/hide the legend"
        layer = helpers.size_category_layer(
            'sf_neighborhoods',
            'name',
            legend=False
        )

        self.assertEqual(layer.legend._type, '')
        self.assertEqual(layer.legend._title, '')

        layer = helpers.size_category_layer(
            'sf_neighborhoods',
            'name',
            legend=True
        )

        self.assertEqual(layer.legend._type, {
            'point': 'size-category-point',
            'line': 'size-category-line',
            'polygon': 'size-category-polygon'
        })
        self.assertEqual(layer.legend._title, 'name')

    def test_size_category_layer_popup(self):
        "should show/hide the popup"
        layer = helpers.size_category_layer(
            'sf_neighborhoods',
            'name',
            popup=False
        )

        self.assertEqual(layer.popup._hover, [])

        layer = helpers.size_category_layer(
            'sf_neighborhoods',
            'name',
            popup=True
        )

        self.assertEqual(layer.popup._hover, [{
            'title': 'name',
            'value': '$name'
        }])

    def test_size_category_layer_widget(self):
        "should show/hide the widget"
        layer = helpers.size_category_layer(
            'sf_neighborhoods',
            'name',
            widget=False
        )

        self.assertEqual(layer.widgets._widgets, [])

        layer = helpers.size_category_layer(
            'sf_neighborhoods',
            'name',
            widget=True
        )

        self.assertEqual(layer.widgets._widgets[0]._type, 'category')
        self.assertEqual(layer.widgets._widgets[0]._title, 'Categories')

    def test_size_category_layer_animate(self):
        "should animate a property and disable the popups"
        layer = helpers.size_category_layer(
            'sf_neighborhoods',
            'name',
            animate='time'
        )

        self.assertEqual(layer.popup._hover, [])
        self.assertEqual(layer.widgets._widgets[0]._type, 'time-series')
        self.assertEqual(layer.widgets._widgets[0]._title, 'Animation')
        self.assertEqual(layer.widgets._widgets[0]._value, 'time')
