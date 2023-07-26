from pyqt_interface_elements import base_layouts, base_widgets, constants
from PySide2 import QtWidgets

QtWidgets.QGraphicsView()


class TimeLine(QtWidgets.QGraphicsScene):

    def __init__(self, start_frame, end_frame):
        super().__init__()
        self.setSceneRect( -100.0, -100.0, 200.0, 200.0 )
        self.start_frame = start_frame
        self.end_frame = end_frame

        self.start_frame_slider = self.build_start_frame_slider()
        self.end_frame_slider = self.build_end_frame_slider()

        # QtWidgets.QGraphicsScene()

        self.addWidget(self.start_frame_slider)
        self.addWidget(self.end_frame_slider)


    def build_start_frame_slider(self):
        _slider = base_widgets.Slider()
        _slider.setOrientation(constants.horizontal)
        _slider.setRange(self.start_frame, self.end_frame)

        _slider.valueChanged.connect(self.startValueChanged)
        return _slider

    def set_start_frame(self, value):
        self.start_frame_slider.setValue(value)

    def build_end_frame_slider(self):
        _slider = base_widgets.Slider()
        _slider.setOrientation(constants.horizontal)
        _slider.setRange(self.start_frame, self.end_frame)

        _slider.valueChanged.connect(self.endValueChanged)
        return _slider

    def end_frame_value(self):
        _value = self.end_frame_slider.value()
        return _value

    def set_end_frame(self, value):
        self.end_frame_slider.setValue(value)

    def start_frame_value(self):
        _value = self.start_frame_slider.value()
        return _value

    def startValueChanged(self):
        _start_frame = self.start_frame_value()
        _end_frame = self.end_frame_value()

        if _start_frame > _end_frame:
            if _start_frame == self.end_frame:
                _start_frame = self.end_frame - 1
            _end_frame = _start_frame + 1

            self.set_end_frame(_end_frame)
            self.set_start_frame(_start_frame)

    def endValueChanged(self):
        _start_frame = self.start_frame_value()
        _end_frame = self.end_frame_value()

        if _start_frame > _end_frame:
            if _end_frame == self.start_frame:
                _end_frame = self.start_frame + 1
            _start_frame = _end_frame - 1

            self.set_end_frame(_end_frame)
            self.set_start_frame(_start_frame)


if __name__ == "__main__":
    import sys

    _app = QtWidgets.QApplication(sys.argv)

    try:
        _scene = TimeLine(0, 100)
        _vuiew = QtWidgets.QGraphicsView()
        _vuiew.setScene(_scene)

        _window = base_layouts.VerticalLayout()
        _window.addWidget(_vuiew)
        _window.show()
    except Exception as e:
        print(e)

    sys.exit(_app.exec_())

