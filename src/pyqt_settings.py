import os
import sys
import json

from PyQt4 import QtGui, QtCore

from options import Options, Colours


data = json.load(open('src/screen_text.json'))

def get_text(name):
    return data['settings'][name][Options.language]


class QColorButton(QtGui.QPushButton):
    '''
    Custom Qt Widget to show a chosen color.

    Left-clicking the button shows the color-chooser, while
    right-clicking resets the color to None (no-color).    
    '''

    colorChanged = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(QColorButton, self).__init__(*args, **kwargs)

        self._color = None
        self.setMaximumWidth(32)
        self.pressed.connect(self.onColorPicker)

    def setColor(self, color):
        if color != self._color:
            self._color = color
            self.colorChanged.emit()
            self.setStyleSheet("background-color: %s;" % self._color)


    def color(self):
        return self._color

    def onColorPicker(self):
        """
        Show color-picker dialog to select color.

        Qt will use the native dialog by default.
        """
        dlg = QtGui.QColorDialog(self)
        if self._color:
            dlg.setCurrentColor(QtGui.QColor(self._color))

        if dlg.exec_():
            self.setColor(dlg.currentColor().name())

    def mousePressEvent(self, e):
        if e.button() == QtCore.Qt.RightButton:
            self.setColor(None)

        return super(QColorButton, self).mousePressEvent(e)


class Window(QtGui.QMainWindow):
    """A settings window with pyqt"""
    width, height = 400, 550

    def __init__(self):
        super().__init__()
        self.setFixedSize(Window.width, Window.height)
        self.setWindowTitle(get_text('header'))
        self.setFont(QtGui.QFont('Times New Roman', 10))
        self.quit_shortcut = QtGui.QShortcut(QtGui.QKeySequence('Ctrl+C'), self)
        self.quit_shortcut.activated.connect(sys.exit)
        self.changed = False
        self.home()
        self.show()

    def home(self):
        self.header = QtGui.QLabel(self)
        self.header.setText(get_text('header'))
        self.header_font = QtGui.QFont('Times New Roman', 12)
        self.header_font.setBold(True)
        self.header.setFont(self.header_font)
        self.header.adjustSize()
        self.header.move(Window.width // 2 - self.header.width() // 2, 0)

        self.is_mute = Options.mute
        self.mute = QtGui.QCheckBox(get_text('mute'), self)
        self.mute.adjustSize()
        self.mute.move(Window.width // 4 - self.mute.width() // 2, 50)
        if self.is_mute:
            self.mute.toggle()
        self.mute.stateChanged.connect(self.toggle_mute)

        self.is_not_log = Options.not_log
        self.not_log = QtGui.QCheckBox(get_text('not_log'), self)
        self.not_log.adjustSize()
        self.not_log.move(3 * Window.width // 4 - self.not_log.width() // 2, 50)
        if self.is_not_log:
            self.not_log.toggle()
        self.not_log.stateChanged.connect(self.toggle_not_log)

        self.is_no_zmbs = Options.no_zombies
        self.no_zmbs = QtGui.QCheckBox(get_text('no_zombies'), self)
        self.no_zmbs.adjustSize()
        self.no_zmbs.move(Window.width // 4 - self.no_zmbs.width() // 2, 85)
        if self.is_no_zmbs:
            self.no_zmbs.toggle()
        self.no_zmbs.stateChanged.connect(self.toggle_no_zmbs)

        self.is_debug = Options.debug
        self.debug = QtGui.QCheckBox(get_text('debug'), self)
        self.debug.adjustSize()
        self.debug.move(3 * Window.width // 4 - self.debug.width() // 2, 85)
        if self.is_debug:
            self.debug.toggle()
        self.debug.stateChanged.connect(self.toggle_debug)

        self.gender = Options.gender
        self.male_b = QtGui.QRadioButton(get_text('male'), self)
        self.male_b.move(Window.width // 4 - self.male_b.width() // 2, 120)

        self.female_b = QtGui.QRadioButton(get_text('female'), self)
        self.female_b.move(3 * Window.width // 4 - self.female_b.width() // 2, 120)
        if self.gender == 'm':
            self.male_b.toggle()
        else:
            self.female_b.toggle()
        self.male_b.pressed.connect(self.toggle_gender)
        self.female_b.pressed.connect(self.toggle_gender)

        self.lang = Options.language
        self.nor_b = QtGui.QRadioButton(get_text('norwegian'), self)
        self.nor_b.adjustSize()
        self.nor_b.move(Window.width // 4 - self.male_b.width() // 2, 155)

        self.eng_b = QtGui.QRadioButton(get_text('english'), self)
        self.eng_b.adjustSize()
        self.eng_b.move(3 * Window.width // 4 - self.female_b.width() // 2, 155)
        if self.lang == 'norsk':
            self.nor_b.toggle()
        else:
            self.eng_b.toggle()
        self.nor_b.pressed.connect(self.toggle_lang)
        self.eng_b.pressed.connect(self.toggle_lang)

        layout = QtGui.QHBoxLayout()
        widget = QtGui.QWidget(self)
        widget.setLayout(layout)

        gender_group = QtGui.QButtonGroup(widget)
        gender_group.addButton(self.male_b)
        gender_group.addButton(self.female_b)

        lang_group = QtGui.QButtonGroup(widget)
        lang_group.addButton(self.nor_b)
        lang_group.addButton(self.eng_b)

        self.fps_text = QtGui.QLabel(get_text('fps'), self)
        self.fps_text.adjustSize()
        self.fps_text.move(10, 270)

        self.fps = Options.fps
        self.fps_slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.fps_slider.resize(220, 30)
        self.fps_slider.move(150, 270)
        self.fps_slider.setMinimum(10)
        self.fps_slider.setMaximum(180)
        self.fps_slider.setValue(self.fps)
        self.fps_slider.sliderMoved.connect(self.fps_change)

        self.fps_value_text = QtGui.QLabel(str(self.fps), self)
        self.fps_value_text.move(self.fps_slider.pos().x() + self.fps * 1.15 - 12, 240)

        self.map_text = QtGui.QLabel(get_text('map'), self)
        self.map_text.adjustSize()
        self.map_text.move(10, 200)

        self.map = Options.mapname
        options = [f.replace('.txt', '') for f in os.listdir('assets/Maps/') if 'test' not in f]
        self.map_dropdown = QtGui.QComboBox(self)
        self.map_dropdown.addItems(options)
        self.map_dropdown.setCurrentIndex(options.index(self.map.rstrip('.txt')))
        self.map_dropdown.resize(220, 30)
        self.map_dropdown.move(150, 200)
        self.map_dropdown.currentIndexChanged.connect(self.change_map)

        self.volume_text = QtGui.QLabel(get_text('volume'), self)
        self.volume_text.adjustSize()
        self.volume_text.move(10, 330)

        self.volume = Options.volume
        self.volume_slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.volume_slider.resize(220, 30)
        self.volume_slider.move(150, 330)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(self.volume * 100)
        self.volume_slider.sliderMoved.connect(self.volume_change)

        self.volume_value_text = QtGui.QLabel(str(self.volume), self)
        self.volume_value_text.move(self.volume_slider.pos().x() + self.volume * 200 - 12, 300)

        self.tile_length_text = QtGui.QLabel(get_text('tile_length'), self)
        self.tile_length_text.adjustSize()
        self.tile_length_text.move(10, 390)

        self.tile_length = Options.tile_length
        self.tile_length_slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.tile_length_slider.resize(220, 30)
        self.tile_length_slider.move(150, 390)
        self.tile_length_slider.setMinimum(10)
        self.tile_length_slider.setMaximum(100)
        self.tile_length_slider.setValue(self.tile_length)
        self.tile_length_slider.sliderMoved.connect(self.tile_length_change)

        self.tile_length_value_text = QtGui.QLabel(str(self.tile_length), self)
        self.tile_length_value_text.move(self.tile_length_slider.pos().x() + self.tile_length * 2.35 - 27, 360)

        self.mod12 = QtGui.QPushButton(get_text('div12'), self)
        self.mod12.move(0, 430)
        self.mod12.resize(Window.width, 40)
        self.mod12.pressed.connect(self.mod12pressed)

        self.fillcolourtext = QtGui.QLabel(get_text('fillcolour') + ':', self)
        self.fillcolourtext.move(10, 470)
        self.fillcolourtext.adjustSize()
        self.fillcolour = QColorButton()
        self.fillcolour.setParent(self)
        self.fillcolour.setColor(Colours.get_hex(Options.fillcolour))
        self.fillcolour.resize(40, 40)
        self.fillcolour.move(self.fillcolourtext.width() + 15, 470)

        self.loopcolourtext = QtGui.QLabel(get_text('loopcolour') + ':', self)
        self.loopcolourtext.move(Window.width // 2 - self.fillcolour.width() // 2 + self.fillcolour.width(), 470)
        self.loopcolourtext.adjustSize()
        self.loopcolour = QColorButton()
        self.loopcolour.setParent(self)
        self.loopcolour.setColor(Colours.get_hex(Options.loopcolour))
        self.loopcolour.resize(40, 40)
        self.loopcolour.move(self.loopcolourtext.pos().x() + self.loopcolourtext.width() + 15, 470)

        self.commit_b = QtGui.QPushButton(get_text('commit'), self)
        self.commit_b.move(0, 510)
        self.commit_b.resize(Window.width // 2, 40)
        self.commit_b.pressed.connect(self.commit)

        self.exit_b = QtGui.QPushButton(get_text('discard'), self)
        self.exit_b.move(Window.width // 2, 510)
        self.exit_b.resize(Window.width // 2, 40)
        self.exit_b.pressed.connect(self.exit)

    def toggle_mute(self): self.is_mute = not self.is_mute
    def toggle_not_log(self): self.is_not_log = not self.is_not_log
    def toggle_no_zmbs(self): self.is_no_zmbs = not self.is_no_zmbs
    def toggle_debug(self): self.is_debug = not self.is_debug

    def toggle_gender(self):
        if self.gender == 'm':
            self.gender = 'f'
        else:
            self.gender = 'm'

    def toggle_lang(self):
        if self.lang == 'norsk':
            self.lang = 'english'
        else:
            self.lang = 'norsk'

    def fps_change(self):
        self.fps = self.fps_slider.value()
        self.fps_value_text.setText(str(self.fps))
        self.fps_value_text.move(self.fps_slider.pos().x() + self.fps * 1.15 - 12, 240)

    def change_map(self):
        self.map = self.map_dropdown.currentText() + '.txt'

    def volume_change(self):
        self.volume = self.volume_slider.value()
        self.volume_value_text.setText(str(self.volume / 100))
        self.volume_value_text.move(self.volume_slider.pos().x() + self.volume * 2 - 12, 300)

    def tile_length_change(self):
        self.tile_length = self.tile_length_slider.value()
        self.tile_length_value_text.setText(str(self.tile_length))
        self.tile_length_value_text.move(self.tile_length_slider.pos().x() + self.tile_length * 2.35 - 27, 360)

    def mod12pressed(self):
        self.tile_length = self.tile_length_slider.value()
        tl_mod12 = self.tile_length % 12
        if tl_mod12 <= 6:
            self.tile_length_slider.setValue(self.tile_length - tl_mod12)
        else:
            self.tile_length_slider.setValue(self.tile_length + 12 - tl_mod12)
        self.tile_length_change()
        self.fps = self.fps_slider.value()
        fps_mod = self.fps % 12
        if fps_mod <= 6:
            self.fps_slider.setValue(self.fps - fps_mod)
        else:
            self.fps_slider.setValue(self.fps + 12 - tl_mod12)
        self.fps_change()

    def commit(self):
        if (Options.mapname != self.map or Options.tile_length != self.tile_length or
                self.lang != Options.language):
            self.changed = True
        Options.fps = self.fps
        Options.mapname = self.map
        Options.volume = self.volume
        Options.mute = self.is_mute
        Options.tile_length = self.tile_length
        Options.gender = self.gender
        Options.not_log = self.is_not_log
        Options.no_zombies = self.is_no_zmbs
        Options.debug = self.is_debug
        Options.language = self.lang
        Options.fillcolour = Colours.get_rgb(self.fillcolour._color)
        Options.loopcolour = Colours.get_rgb(self.loopcolour._color)
        try:
            Options.assertions()
        except AssertionError as e:
            self.error_box = QtGui.QMessageBox()
            self.error_box.setIcon(QtGui.QMessageBox.Critical)
            self.error_box.setText(get_text('error') + str(e))
            self.error_box.exec_()
            return
        try:
            Options.warnings()
        except AssertionError as e:
            self.warning_box = QtGui.QMessageBox.question(
                self,
                'warning',
                get_text('warning').format(e),
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            if self.warning_box == QtGui.QMessageBox.Yes:
                self.exit()
            else:
                return
        else:
            self.exit()

    def exit(self):
        self.close()


def main():
    app = QtGui.QApplication([])
    GUI = Window()
    app.exec_()
    return GUI.changed


if __name__ == '__main__':
    main()
