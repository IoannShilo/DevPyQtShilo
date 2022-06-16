from PySide2 import QtWidgets, QtCore
import sys


class MyWidgets(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUi()

    def initUi(self):

        self.button_LT = QtWidgets.QPushButton()
        self.button_LT.setText('Лево/верх')
        self.button_LT.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                     QtWidgets.QSizePolicy.Policy.Expanding)

        self.button_RT = QtWidgets.QPushButton()
        self.button_RT.setText('Право/верх')
        self.button_RT.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                     QtWidgets.QSizePolicy.Policy.Expanding)
        self.button_Centr = QtWidgets.QPushButton()
        self.button_Centr.setText('Центр')
        self.button_Centr.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                     QtWidgets.QSizePolicy.Policy.Expanding)

        self.button_LB = QtWidgets.QPushButton()
        self.button_LB.setText('Лево/низ')
        self.button_LB.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                     QtWidgets.QSizePolicy.Policy.Expanding)

        self.button_RB = QtWidgets.QPushButton()
        self.button_RB.setText('Право/низ')
        self.button_RB.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                     QtWidgets.QSizePolicy.Policy.Expanding)

        self.button_Param = QtWidgets.QPushButton()
        self.button_Param.setText('Получить параметры')
        self.button_Param.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                        QtWidgets.QSizePolicy.Policy.Expanding)

        self.combo_box = QtWidgets.QComboBox()
        self.combo_box.addItems(["HEX", "DEC", "OCT", "BIN"])

        self.dial = QtWidgets.QDial()

        self.lcd_num = QtWidgets.QLCDNumber()

        self.slider = QtWidgets.QSlider()
        self.slider.setOrientation(QtCore.Qt.Orientation.Horizontal)

        self.text_edit = QtWidgets.QPlainTextEdit()

        #Layouts

        push_buttons_layout = QtWidgets.QVBoxLayout()

        pb_layout_row1 = QtWidgets.QHBoxLayout()
        pb_layout_row2 = QtWidgets.QHBoxLayout()
        pb_layout_row3 = QtWidgets.QHBoxLayout()
        pb_layout_row4 = QtWidgets.QHBoxLayout()

        pb_layout_row1.addWidget(self.button_LT)
        pb_layout_row1.addWidget(self.button_RT)

        pb_layout_row2.addWidget(self.button_Centr)

        pb_layout_row3.addWidget(self.button_LB)
        pb_layout_row3.addWidget(self.button_RB)

        pb_layout_row4.addWidget(self.button_Param)

        push_buttons_layout.addLayout(pb_layout_row1)
        push_buttons_layout.addLayout(pb_layout_row2)
        push_buttons_layout.addLayout(pb_layout_row3)
        push_buttons_layout.addLayout(pb_layout_row4)

        cbox_lcd_layout = QtWidgets.QVBoxLayout()
        cbox_lcd_layout.addWidget(self.combo_box)
        cbox_lcd_layout.addWidget(self.lcd_num)

        dial_cb_lcd_layout = QtWidgets.QHBoxLayout()
        dial_cb_lcd_layout.addWidget(self.dial)
        dial_cb_lcd_layout.addLayout(cbox_lcd_layout)

        left_main_layout = QtWidgets.QVBoxLayout()
        left_main_layout.addLayout(push_buttons_layout)
        left_main_layout.addLayout(dial_cb_lcd_layout)
        left_main_layout.addWidget(self.slider)

        main_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(left_main_layout)
        main_layout.addWidget(self.text_edit)

        self.setLayout(main_layout)

        self.button_LT.clicked.connect(self.ltb_clicked)
        self.button_RT.clicked.connect(self.rtb_clicked)
        self.button_LB.clicked.connect(self.lbb_clicked)
        self.button_RB.clicked.connect(self.rbb_clicked)
        self.button_Centr.clicked.connect(self.centr_clicked)
        self.button_Param.clicked.connect(self.get_param)
        self.dial.valueChanged.connect(self.dial_lcd)


    def ltb_clicked(self):
        self.move(0, 0)

    def rtb_clicked(self):
        x = QtWidgets.QApplication.screenAt(self.pos()).size().width() - self.width()
        self.move(x, 0)

    def lbb_clicked(self):
        y = QtWidgets.QApplication.screenAt(self.pos()).size().height() - self.height() - 75
        self.move(0, y)

    def rbb_clicked(self):
        x = QtWidgets.QApplication.screenAt(self.pos()).size().width() - self.width()
        y = QtWidgets.QApplication.screenAt(self.pos()).size().height() - self.height() - 75
        self.move(x, y)

    def centr_clicked(self):
        x = (QtWidgets.QApplication.screenAt(self.pos()).size().width() / 2) - (self.width() / 2)
        y = (QtWidgets.QApplication.screenAt(self.pos()).size().height() / 2) - (self.height() / 2)
        self.move(x, y)

    def get_param(self):
        print(QtWidgets.QApplication.screens())
        self.text_edit.appendPlainText(str(QtWidgets.QApplication.screens()))

    def dial_lcd(self):
        value = self.dial.value()
        self.lcd_num.display(value)

    def changeEvent(self, event:QtCore.QEvent) -> None:
        if event.type() == QtCore.QEvent.Type.WindowStateChange:
            if self.isMinimized():
                print('ddd')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myWindow = MyWidgets()
    myWindow.show()

    app.exec_()