import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app


def find_component(component, predicate):
    if predicate(component):
        return component

    children = getattr(component, 'children', None)
    if isinstance(children, list):
        for child in children:
            if not isinstance(child, (str, int, float)):
                result = find_component(child, predicate)
                if result is not None:
                    return result
    elif children is not None and not isinstance(children, (str, int, float)):
        result = find_component(children, predicate)
        if result is not None:
            return result

    return None


def test_header_present():
    header = find_component(
        app.layout,
        lambda c: getattr(c, '__class__', None) is not None
        and c.__class__.__name__ == 'H1'
        and getattr(c, 'children', None) == 'Pink Morsel Sales Visualiser',
    )
    assert header is not None
    assert header.children == 'Pink Morsel Sales Visualiser'


def test_visualisation_present():
    chart = find_component(app.layout, lambda c: getattr(c, 'id', None) == 'sales-chart')
    assert chart is not None


def test_region_picker_present():
    selector = find_component(app.layout, lambda c: getattr(c, 'id', None) == 'region-selector')
    assert selector is not None
    options = getattr(selector, 'options', None)
    assert options is not None
    labels = [option['value'] for option in options]
    assert set(labels) == {'all', 'north', 'east', 'south', 'west'}
