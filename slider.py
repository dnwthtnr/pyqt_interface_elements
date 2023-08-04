import copy
from PySide2 import QtCore, QtWidgets, QtGui
from pyqt_interface_elements import base_widgets, constants, styles

class RangeSliderTick(QtWidgets.QWidget):

    def __init__(self, rect):
        super().__init__()
        self.setGeometry(rect)

    def paintEvent(self, event):
        super().paintEvent(event)


class RangeSlider(base_widgets.Slider):
    sliderMoved = QtCore.Signal(int, int)

    def __init__(self, minimum, maximum, values_to_mark=[]):
        super().__init__()
        self.setOrientation(constants.horizontal)

        self._marked_values = values_to_mark

        self.setMinimum(minimum)
        self.setMaximum(maximum)

        self._lower_bound = 50
        self._upper_bound = self.maximum()

        self._pressed_element = None

    # region Value Setters

    def setValuesToMark(self, values):
        """
        Set values to paint markers at

        Parameters
        ----------
        values : list[int] or list[float]

        Returns
        -------

        """
        if not isinstance(values, list):
            return
        for _value in values:
            if not isinstance(_value, int) and not isinstance(_value, float):
                return

        self._marked_values = values

    def valuesToMark(self):
        """
        Values to paint markers at

        Returns
        -------

        """
        return self._marked_values

    def addValueToMark(self, value):
        """
        Adds a value to paint a marker at

        Parameters
        ----------
        value

        Returns
        -------

        """
        self._marked_values.append(value)

    def removeValueToMark(self, value):
        """
        Removes the given value from the values to paint markers at if it is present

        Parameters
        ----------
        value : int or float

        """
        if value in self.valuesToMark():
            _index = self._marked_values.index(value)
            self._marked_values.pop(_index)

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

        # self.paint

        # self.paintSliderGroove(painter, style)

        # self.paintTickMarks(_groove_control_rect, painter, style)

        self.paintSelectedRange(painter, style)
        self.paintTickMarks(painter, style)
        self.paintSliderHandles(painter=painter, style=style)
        self.paintMarkers(painter, style)
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
        self.setTickPosition(self.TicksBothSides)
        _opt.subControls = QtWidgets.QStyle.SC_SliderTickmarks

        # style.drawComplexControl(QtWidgets.QStyle.CC_Slider, _opt, painter, self)

        _palette = QtGui.QPalette()
        _palette.setColor(QtGui.QPalette.Window, QtGui.QColor(255, 0, 0))


        style.drawComplexControl(QtWidgets.QStyle.CC_Slider, _opt, painter, self)

    def paintSelectedRange(self, painter, style):
        """

        Parameters
        ----------
        painter
        style : QtWidget.QStyle

        Returns
        -------

        """

        _pixel_upper_limit = self.slider_value_to_pixel_value(self.upperBound())
        _pixel_lower_limit = self.slider_value_to_pixel_value(self.lowerBound())

        _slider_top = self.rect().top()
        _slider_bottom = self.rect().bottom()

        # print(_slider_height)

        _top_left = QtCore.QPoint(_pixel_lower_limit, _slider_top)
        _bottom_right   = QtCore.QPoint(_pixel_upper_limit, _slider_bottom)

        _selection_rectangle = QtCore.QRect(_top_left, _bottom_right)

        _color = QtGui.QColor(155, 155, 155, 255)

        painter.fillRect(_selection_rectangle, _color)
        # _selection_rectangle = QtCore.QRect(QtCore.QPoint(0, 100), QtCore.QPoint(500, 0))

        # _pen = QtGui.QPen()
        # _pen.setColor(QtCore.Qt.blue)
        #
        # _brush = QtGui.QBrush()
        # _brush.setColor(QtCore.Qt.blue)
        # # _brush
        #
        # painter.setPen(_pen)
        # painter.setBrush(_brush)
        #
        # _opt = QtWidgets.QStyleOptionSlider()
        # self.initStyleOption(_opt)
        # _opt.subControls = QtWidgets.QStyle.SC_SliderGroove
        # # print(_opt.rect)
        # _opt.rect = _selection_rectangle
        # print(_selection_rectangle)


        #TODO: style option for rectangle and set it as the region. then draw with the given style and painter

        # style.drawComplexControl(QtWidgets.QStyle.CC_Slider, _opt, painter, self)

    def paintMarkers(self, painter, style):
        """
        Paints markers
        Parameters
        ----------
        painter
        style

        Returns
        -------

        """
        for _handle_value in self.valuesToMark():
            _pixel_value = self.slider_value_to_pixel_value(_handle_value)
            _top = self.rect().top()

            _top_left = QtCore.QPoint(_pixel_value, _top)
            _bottom_right = QtCore.QPoint(_pixel_value + 1, self.rect().bottom())

            _rect = QtCore.QRect(_top_left, _bottom_right)

            _color = QtGui.QColor(255, 10, 20, 130)

            painter.fillRect(_rect, _color)


    def paintTickMarks(self, painter, style):
        _multiple_of = 5
        _draw_number = False
        for _value in range(self.maximum()-self.minimum()):

            _result = _value / _multiple_of
            if not _result.is_integer():
                continue

            _pixel_value = self.slider_value_to_pixel_value(_value)
            _top = self.rect().center().y()


            _top_left = QtCore.QPoint(_pixel_value, _top)
            _bottom_right = QtCore.QPoint(_pixel_value + 3, self.rect().bottom())

            _rect = QtCore.QRect(_top_left, _bottom_right)

            _color = QtGui.QColor(100, 100, 100, 255)

            painter.fillRect(_rect, _color)

            if _draw_number is False:
                _draw_number = True
                continue

            painter.drawText(QtCore.QPoint(_pixel_value+5, _top-5), str(_value))
            _draw_number = False

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
        _slider_axis_pixel_value = self.point_dimension_for_orientation(event.pos())
        _new_position = self.pixel_value_to_slider_value(_slider_axis_pixel_value)

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

    # region
    def point_dimension_for_orientation(self, point):
        return point.x() if self.orientation() == constants.horizontal else point.y()

    def pixel_value_to_slider_value(self, slider_axis_pixel_value):
        """
        Given a pixel value contained within the slider this will return the slider logic value it is equivalent to

        Parameters
        ----------
        slider_axis_pixel_value : int
            The appropriate pixel value on the correct axis for the slider orientation

        Returns
        -------
        float
            The slider value

        """
        slider_axis_pixel_value = self.mapFromParent(QtCore.QPoint(slider_axis_pixel_value, 0)).x()


        _widget_geometry_minimum_pixel_local  =  self.rect().left()
        _widget_geometry_maximum_pixel_local = self.rect().right()


        if self.orientation() == constants.horizontal:
            _widget_geometry_minimum_pixel_global =  self.mapFromParent(
                QtCore.QPoint(_widget_geometry_minimum_pixel_local, 0)
            )
            _widget_geometry_maximum_pixel_global = self.mapFromParent(
                QtCore.QPoint(_widget_geometry_maximum_pixel_local, 0)
            )
        else:
            _widget_geometry_minimum_pixel_global =  self.mapFromParent(
                QtCore.QPoint(0, _widget_geometry_minimum_pixel_local)
            )
            _widget_geometry_maximum_pixel_global = self.mapFromParent(
                QtCore.QPoint(0, _widget_geometry_maximum_pixel_local)
            )

        _widget_geometry_minimum = self.point_dimension_for_orientation(_widget_geometry_minimum_pixel_global)
        _widget_geometry_maximum = self.point_dimension_for_orientation(_widget_geometry_maximum_pixel_global)


        _widget_geometry_pixel_range = _widget_geometry_maximum - _widget_geometry_minimum
        _widget_geometry_pixel_lower_limit = slider_axis_pixel_value - _widget_geometry_minimum

        _difference_ratio = _widget_geometry_pixel_lower_limit / _widget_geometry_pixel_range

        _slider_range = self.maximum() - self.minimum()

        # print(_widget_geometry_pixel_lower_limit, _widget_geometry_pixel_range, _difference_ratio)

        _val = _slider_range * _difference_ratio

        # return _val
        # region###############################

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

        _slider_lower_span = slider_axis_pixel_value - _slider_min
        _slider_upper_span = _slider_max - _slider_min

        _slider_value = _widget_style.sliderValueFromPosition(
            self.minimum(),
            self.maximum(),
            _slider_lower_span,
            _slider_upper_span,
            _slider_style_option.upsideDown
        )

        print(_slider_value, _val)

        return _val

    def slider_value_to_pixel_value(self, slider_value):
        """
        Given a slider logic value this will return the pixel value it is equivalent to

        Parameters
        ----------
        slider_value : int
            The slider value

        Returns
        -------
        float
            The appropriate pixel value on the correct axis for the slider orientation

        """
        _widget_geometry_minimum_pixel_local  =  self.rect().left()
        _widget_geometry_maximum_pixel_local = self.rect().right()

        if self.orientation() == constants.horizontal:
            _widget_geometry_minimum_pixel_global =  self.mapFromParent(
                QtCore.QPoint(_widget_geometry_minimum_pixel_local, 0)
            )
            _widget_geometry_maximum_pixel_global = self.mapFromParent(
                QtCore.QPoint(_widget_geometry_maximum_pixel_local, 0)
            )
        else:
            _widget_geometry_minimum_pixel_global =  self.mapFromParent(
                QtCore.QPoint(0, _widget_geometry_minimum_pixel_local)
            )
            _widget_geometry_maximum_pixel_global = self.mapFromParent(
                QtCore.QPoint(0, _widget_geometry_maximum_pixel_local)
            )


        _widget_geometry_minimum = self.point_dimension_for_orientation(_widget_geometry_minimum_pixel_global)
        _widget_geometry_maximum = self.point_dimension_for_orientation(_widget_geometry_maximum_pixel_global)

        _slider_range = self.maximum() - self.minimum()
        _slider_lower_limit = slider_value - self.minimum()

        _difference_ratio = _slider_lower_limit / _slider_range

        _widget_geometry_span = _widget_geometry_maximum - _widget_geometry_minimum

        _val = _widget_geometry_span * _difference_ratio

        return _val

        ################
        #
        # _slider_style_option = QtWidgets.QStyleOptionSlider()
        # self.initStyleOption(_slider_style_option)
        # _widget_style = QtWidgets.QApplication.style()
        #
        # _slider_groove_geometry = _widget_style.subControlRect(
        #     _widget_style.CC_Slider,
        #     _slider_style_option,
        #     _widget_style.SC_SliderGroove,
        #     self
        # )
        # _slider_handle_geometry = _widget_style.subControlRect(
        #     _widget_style.CC_Slider,
        #     _slider_style_option,
        #     _widget_style.SC_SliderHandle,
        #     self
        # )
        #
        # if self.orientation() == constants.horizontal:
        #     _slider_length = _slider_handle_geometry.width()
        #     _slider_min = _slider_groove_geometry.x()
        #     _slider_max = _slider_groove_geometry.right() - _slider_length + 1
        # else:
        #     _slider_length = _slider_handle_geometry.height()
        #     _slider_min = _slider_groove_geometry.y()
        #     _slider_max = _slider_groove_geometry.bottom() - _slider_length + 1
        #
        # _slider_lower_span = slider_value - self.minimum()
        # _slider_upper_span = self.maximum() - self.minimum()
        #
        # _position = _widget_style.sliderPositionFromValue(_slider_min, _slider_max, slider_value, _slider_lower_span, _slider_upper_span)
        # return _position

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
