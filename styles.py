from pyqt_interface_elements import constants
import os

def process_stylesheet(stylesheet, variables):
    _processed = stylesheet

    for _var in list(variables.keys()):
        _processed = _processed.replace(_var, variables.get(_var))

    return _processed

variables = {
    "@maya_button_background;": "#5d5d5d;",
    "@maya_widget;": "#444444;",
    "@maya_white_text;": "#b2b2ab;",
    "@maya_outliner_background;": "#373737;",
    "@maya_blue_selection;": "#568aad;",
    "@maya_negative_space;": "#2b2b2b;",
}

def get_style_var(style):
    _stylesheet_path = os.path.join(constants.stylesheets_local_directory, style)
    with open(_stylesheet_path, "r") as f:
        _data = f.read()

    return process_stylesheet(_data, variables)



style_var = {
    "@@maya_button@@": get_style_var("maya_button.qss")
}
def get_stylesheet(style):
    _stylesheet_path = os.path.join(constants.stylesheets_local_directory, style)
    with open(_stylesheet_path, "r") as f:
        _data = f.read()

    _data = get_style_var(style)
    print(process_stylesheet(_data, style_var))

    return process_stylesheet(_data, style_var)



maya_button = get_stylesheet("maya_button.qss")
maya_widget = get_stylesheet("maya_widget.qss")
maya_outliner = get_stylesheet("maya_outliner.qss")
maya_detail_view = get_stylesheet("maya_detail_view.qss")
maya_splitter = get_stylesheet("maya_splitter.qss")
