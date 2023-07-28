from PySide2 import QtCore, QtWidgets, QtGui
from pyqt_interface_elements import base_widgets, constants



class RangeSlider(base_widgets.Slider):


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
