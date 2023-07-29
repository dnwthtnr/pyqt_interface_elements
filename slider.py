from PySide2 import QtCore, QtWidgets, QtGui
from pyqt_interface_elements import base_widgets, constants



class RangeSlider(base_widgets.Slider):
    sliderMoved = QtCore.Signal(int, int)


    def __init__(self, minimum, maximum):
        super().__init__()
        self.setOrientation(constants.horizontal)

        self.setMinimum(minimum)
        self.setMaximum(maximum)

        self._lower_bound = 50
        self._upper_bound = self.maximum()


    # region Value Setters

    def lowerBound(self):
        return self._lower_bound

    def setLowerBound(self, value):
        self._lower_bound = value
        self.update()

    def upperBound(self):
        return self._upper_bound

    def setUpperBound(self, value):
        self._upper_bound = value
        self.update()


    # endregion

    def paintEvent(self, event):


        painter = QtGui.QPainter(self)
        style = QtWidgets.QApplication.style()


        for i, _handle_value in enumerate([self._lower_bound, self._upper_bound]):
            opt = QtWidgets.QStyleOptionSlider()
            self.initStyleOption(opt)

            # Only draw the groove for the first slider so it doesn't get drawn
            # on top of the existing ones every time
            if i == 0:
                opt.subControls = QtWidgets.QStyle.SC_SliderHandle# | QtWidgets.QStyle.SC_SliderGroove
            else:
                opt.subControls = QtWidgets.QStyle.SC_SliderHandle

            if self.tickPosition() != self.NoTicks:
                opt.subControls |= QtWidgets.QStyle.SC_SliderTickmarks

            # if self.pressed_control:
            #     opt.activeSubControls = self.pressed_control
            # else:
            #     opt.activeSubControls = self.hover_control

            opt.sliderPosition = _handle_value
            opt.sliderValue = _handle_value
            style.drawComplexControl(QtWidgets.QStyle.CC_Slider, opt, painter, self)

        return

    def mousePressEvent(self, event):
        event.accept()

        _widget_style = QtWidgets.QApplication.style()
        _button = event.button()

        if _button is None:
            event.ignore()
            return


        _slider_style_option = QtWidgets.QStyleOptionSlider()
        self.initStyleOption(_slider_style_option)

        self.active_slider = -1

        for i, slider_value in enumerate([self._lower_bound, self._upper_bound]):
            _slider_style_option.sliderPosition = slider_value
            _element_clicked_on = _widget_style.hitTestComplexControl(_widget_style.CC_Slider, _slider_style_option, event.pos(), self)

            if _element_clicked_on == _widget_style.SC_SliderHandle:
                self.active_slider = i
                self._pressed_element = _element_clicked_on

                self.triggerAction(self.SliderMove)
                self.setRepeatAction(self.SliderNoAction)
                self.setSliderDown(True)

                print(self.active_slider)

                break

    def mouseMoveEvent(self, event):
        if self._pressed_element != QtWidgets.QStyle.SC_SliderHandle:
            event.ignore()
            return


        event.accept()
        print(event.pos())
        _new_position = self.pixel_value_to_slider_value(event.pos())

        if self.active_slider == 0:
            if _new_position >= self._upper_bound:
                _new_position = self._upper_bound - 1
            self._lower_bound = _new_position

        if self.active_slider == 1:
            if _new_position <= self._lower_bound:
                _new_position = self._lower_bound + 1
            self._upper_bound = _new_position

        self.update()

        self.sliderMoved.emit(self._lower_bound, self._upper_bound)

    def pixel_value_to_slider_value(self, point_on_slider):
        position = point_on_slider.x() if self.orientation() == constants.horizontal else point_on_slider.y()

        _slider_style_option = QtWidgets.QStyleOptionSlider()
        self.initStyleOption(_slider_style_option)
        _widget_style = QtWidgets.QApplication.style()

        _slider_groove_geometry = _widget_style.subControlRect(
            _widget_style.CC_Slider,
            _slider_style_option,
            _widget_style.SC_SliderGroove,
            self
        )
        _slider_handle_geometry = _widget_style.subControlRect(
            _widget_style.CC_Slider,
            _slider_style_option,
            _widget_style.SC_SliderHandle,
            self
        )

        if self.orientation() == constants.horizontal:
            _slider_length = _slider_handle_geometry.width()
            _slider_min = _slider_groove_geometry.x()
            _slider_max = _slider_groove_geometry.right() - _slider_length + 1
        else:
            _slider_length = _slider_handle_geometry.height()
            _slider_min = _slider_groove_geometry.y()
            _slider_max = _slider_groove_geometry.bottom() - _slider_length + 1

        _slider_lower_span = position - _slider_min
        _slider_upper_span = _slider_max - _slider_min

        _slider_value = _widget_style.sliderValueFromPosition(
            self.minimum(),
            self.maximum(),
            _slider_lower_span,
            _slider_upper_span,
            _slider_style_option.upsideDown
        )
        
        return _slider_value





if __name__ == "__main__":
    import sys

    _app = QtWidgets.QApplication(sys.argv)

    try:
        _window = RangeSlider(0, 100)
        # _vuiew = QtWidgets.QGraphicsView()
        # _vuiew.setScene(_scene)
        #
        # _window = base_layouts.VerticalLayout()
        # _window.addWidget(_vuiew)
        _window.show()
    except Exception as e:
        print(e)

    sys.exit(_app.exec_())
