"""
Widget helpers to generate widgets faster.

Example:
    Create an Animation Widget

    .. code::python

        from cartoframes.viz import Map, Layer
        from cartoframes.viz.widgets import animation_widget

        Map(
            Layer(
                'seattle_collisions',
                'filter: animation($incdate, 20, fade(0.5,0.5))',
                widgets=[
                    animation_widget(
                        title='Collision Date',
                        description= 'Play, pause, or select the range of the animation'
                    )]
            )
        )

    Create a Category Widget

    .. code::python

        from cartoframes.viz import Map, Layer
        from cartoframes.viz.widgets import category_widget

        Map(
            Layer(
                'seattle_collisions',
                widgets=[
                    category_widget(
                        'collisiontype',
                        title='Type of Collision',
                        description='Select a category to filter',
                    )
                ]
            )
        )
"""

from __future__ import absolute_import

from .animation_widget import animation_widget
from .category_widget import category_widget
from .default_widget import default_widget
from .formula_widget import formula_widget
from .histogram_widget import histogram_widget
from .time_series_widget import time_series_widget
from ..widget import Widget
from ..widget_list import WidgetList


def _inspect(widget):
    import inspect
    lines = inspect.getsource(widget)
    print(lines)


__all__ = [
    'Widget',
    'WidgetList',
    'animation_widget',
    'category_widget',
    'default_widget',
    'formula_widget',
    'histogram_widget',
    'time_series_widget',
]
