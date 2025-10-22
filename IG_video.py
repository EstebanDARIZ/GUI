import sys

from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget

from config import VIDEO_PATH, FILE_PATH


def read_detection_file(path_file):
    """
    Reads a text file containing detection timestamps (in seconds)
    and converts them to milliseconds for synchronization with the player.

    Args:
        path_file (str): Path to the file containing detection times.

    Returns:
        list[int]: List of timestamps (in milliseconds).
    """
    time_detect = []
    try:
        with open(path_file, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                # Split by comma and convert each value to milliseconds
                for value in line.split(" ,"):
                    time_detect.append(int(value) * 1000)
    except Exception as e:
        print(f"Error during loading the file {path_file}: {e}")
    return time_detect


class MySlider(QtWidgets.QSlider):
    """
    Custom QSlider that displays red markers representing points of interest
    (timestamps of detected events) on the video timeline.
    """

    def __init__(self, orientation=QtCore.Qt.Horizontal, interesting_part=None):
        super().__init__(orientation)
        self.interesting_part = interesting_part or []

    def paintEvent(self, event):
        """
        Reimplements the paintEvent to draw custom markers along the slider.
        """
        super().paintEvent(event)

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtGui.QPen(QtCore.Qt.red, 2))

        # Initialize slider style options
        opt = QtWidgets.QStyleOptionSlider()
        QtWidgets.QSlider.initStyleOption(self, opt)

        # Get the slider groove (the main line of the slider)
        groove_rect = self.style().subControlRect(
            QtWidgets.QStyle.CC_Slider,
            opt,
            QtWidgets.QStyle.SC_SliderGroove,
            self
        )

        # Draw a vertical red line for each point of interest
        for t in self.interesting_part:
            ratio = t / self.maximum() if self.maximum() > 0 else 0
            x = groove_rect.x() + ratio * groove_rect.width()
            painter.drawLine(int(x), 0, int(x), self.rect().height())

        painter.end()


class MyWidget(QtWidgets.QWidget):
    """
    Main application widget combining:
    - A video player (QMediaPlayer + QVideoWidget)
    - A custom slider with detection markers
    - Playback controls (Play/Pause, <<, >>)
    """

    def __init__(self):
        super().__init__()

        # Playback state variables
        self.state = ["Play", "Pause"]
        self.current_state = "Pause"

        # Load timestamps of detected events
        self.interesting_part = read_detection_file(FILE_PATH)
        # print(self.interesting_part)

        # UI Elements 
        self.button_play = QtWidgets.QPushButton("Play")
        self.button_right = QtWidgets.QPushButton(">>")
        self.button_left = QtWidgets.QPushButton("<<")
        self.video_widget = QVideoWidget()
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.slider = MySlider(interesting_part=self.interesting_part)

        # Connect player video and audio outputs 
        self.player.setVideoOutput(self.video_widget)
        self.player.setAudioOutput(self.audio_output)

        # Set video source 
        self.player.setSource(QtCore.QUrl.fromLocalFile(VIDEO_PATH))

        # Synchronization between player and slider 
        self.player.positionChanged.connect(lambda pos: self.slider.setValue(pos))
        self.player.durationChanged.connect(lambda dur: self.slider.setMaximum(dur))
        self.slider.sliderMoved.connect(lambda value: self.player.setPosition(value))
        self.slider.sliderReleased.connect(lambda: self.player.setPosition(self.slider.value()))

        # Layout setup 
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addWidget(self.video_widget)
        self.main_layout.addWidget(self.slider)

        self.bottom_layout = QtWidgets.QHBoxLayout()
        self.bottom_layout.addWidget(self.button_play)
        self.bottom_layout.addWidget(self.button_left)
        self.bottom_layout.addWidget(self.button_right)
        self.bottom_layout.addStretch()

        self.main_layout.addLayout(self.bottom_layout)

        # Connect button actions 
        self.button_play.clicked.connect(self.change_state)
        self.button_right.clicked.connect(self.move2right)
        self.button_left.clicked.connect(self.move2left)

    @QtCore.Slot()
    def change_state(self):
        """
        Toggles between Play and Pause state.
        """
        if self.current_state == self.state[0]:
            self.current_state = self.state[1]
            self.button_play.setText("Play")
            self.player.pause()
        else:
            self.current_state = self.state[0]
            self.button_play.setText("Pause")
            self.player.play()

    def move2right(self):
        """
        Move the playback position to the next interesting part.
        If the end is reached, wrap around to the first one.
        """
        for i in self.interesting_part:
            if self.player.position() < i:
                self.player.setPosition(i)
                break
        else:
            self.player.setPosition(self.interesting_part[0])

    def move2left(self):
        """
        Move the playback position to the previous interesting part.
        If at the beginning, wrap around to the last one.
        """
        for i in reversed(self.interesting_part):
            if self.player.position() > i:
                self.player.setPosition(i)
                break
        else:
            self.player.setPosition(self.interesting_part[-1])


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
