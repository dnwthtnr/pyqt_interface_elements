from pyqt_interface_elements import base_layouts, base_widgets


class TimeLine(base_layouts.HorizontalLayout):

    def __init__(self, start_frame, end_frame):
        super().__init__()
        self.start_frame = start_frame
        self.end_frame = end_frame

        self.start_frame_slider = self.build_start_frame_slider()


        self.end_frame_slider = self.build_end_frame_slider()


    def build_start_frame_slider(self):
        _slider = base_widgets.Slider()
        _slider.setRange(self.start_frame, self.end_frame)

        _slider.valueChanged.connect()
        return _slider

    def set_start_frame(self, value):
        self.start_frame_slider.setValue(value)

    def build_end_frame_slider(self):
        _slider = base_widgets.Slider()
        _slider.setRange(self.start_frame, self.end_frame)

        _slider.valueChanged.connect()
        return _slider

    def end_frame_value(self):
        _value = self.end_frame_slider.value()
        return _value

    def set_end_frame(self, value):
        self.end_frame_slider.setValue(value)
        
    def start_frame_value(self):
        _value = self.start_frame_slider.value()
        return _value

    def valueChanged(self):
        _start_frame = self.start_frame_value()
        _end_frame = self.end_frame_value()

        if _start_frame > _end_frame:
            if _start_frame == self.end_frame:
                _start_frame = self.end_frame - 1
            _end_frame = _start_frame + 1

            self.set_end_frame(_end_frame)
            self.set_start_frame(_start_frame)





