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

        _groove_control_rect = self.paintSliderGroove(painter, style)

        # self.paintTickMarks(_groove_control_rect, painter, style)

        self.paintSliderHandles(painter=painter, style=style)
        return


    # region Painters
    def paintSliderHandle(self, handle_value):
        """
        Paints a slider handle at the given value

        Parameters
        ----------
        handle_value : float
            The value to draw the slider handle at

        Returns
        -------
        QtWidgets.QStyleOptionSlider
            A slider style option defining the slider handle

        """
        opt = QtWidgets.QStyleOptionSlider()
        self.initStyleOption(opt)

        # Only draw the groove for the first slider so it doesn't get drawn
        # on top of the existing ones every time
        opt.subControls = QtWidgets.QStyle.SC_SliderHandle

        # if self.tickPosition() != self.NoTicks:
        #     opt.subControls |= QtWidgets.QStyle.SC_SliderTickmarks

        opt.sliderPosition = handle_value
        opt.sliderValue = handle_value
        return opt

    def paintSliderHandles(self, painter, style):
        """
        Draws the handles for the upper and lower bound

        Parameters
        ----------
        painter : QtGui.QPainter
            TYhe painter to be used to draw teh slider handles
        style : QtWidgets.QStyle
            The style for the current QApplication

        """
        for i, _handle_value in enumerate([self._lower_bound, self._upper_bound]):
            _slider_handle_style_option = self.paintSliderHandle(handle_value=_handle_value)
            style.drawComplexControl(QtWidgets.QStyle.CC_Slider, _slider_handle_style_option, painter, self)

    def paintSliderGroove(self, painter, style):
        _opt = QtWidgets.QStyleOptionSlider()
        self.initStyleOption(_opt)

        _opt.sliderValue = 0
        _opt.sliderPosition = 0
        _opt.subControls = QtWidgets.QStyle.SC_SliderGroove
        self.setTickPosition(self.TickPosition)
        _opt.subControls = QtWidgets.QStyle.SC_SliderTickmarks

        style.drawComplexControl(QtWidgets.QStyle.CC_Slider, _opt, painter, self)

        # _control_rect = style.subControlRect(QtWidgets.QStyle.CC_Slider, _opt, QtWidgets.QStyle.SC_SliderGroove, self)
        # return _control_rect



    def paintTickMarks(self, slider_groove_rect, painter, style):
        _opt = QtWidgets.QStyleOptionSlider()
        self.initStyleOption(_opt)
        _opt.subControls = QtWidgets.QStyle.SC_SliderTickmarks
        _opt.tickInterval = 1

        style.drawComplexControl(QtWidgets.QStyle.CC_Slider, _opt, painter, self)
        return
    # endregion

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

        for slider_index, slider_value in enumerate([self._lower_bound, self._upper_bound]):
            _slider_style_option.sliderPosition = slider_value
            _element_clicked_on = _widget_style.hitTestComplexControl(_widget_style.CC_Slider, _slider_style_option,
                                                                      event.pos(), self)

            if _element_clicked_on == _widget_style.SC_SliderHandle:
                self.active_slider = slider_index
                self._pressed_element = _element_clicked_on

                self.triggerAction(self.SliderMove)
                self.setRepeatAction(self.SliderNoAction)
                self.setSliderDown(True)
                break

    def mouseMoveEvent(self, event):
        if self._pressed_element != QtWidgets.QStyle.SC_SliderHandle:
            event.ignore()
            return

        event.accept()
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

    _window = RangeSlider(0, 100)
    # _vuiew = QtWidgets.QGraphicsView()
    # _vuiew.setScene(_scene)
    #
    # _window = base_layouts.VerticalLayout()
    # _window.addWidget(_vuiew)
    _window.show()

    sys.exit(_app.exec_())
