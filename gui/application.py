#!/usr/bin/env python

import sys
import logging

# from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import (
    QMainWindow, QLabel, QTextEdit, QLineEdit,
    QPushButton, QRadioButton, QFrame, QButtonGroup,
    QIcon, QApplication, QFont, QMessageBox
)

import utils

from scripts.generate import generate_secret


# Set up logging configuration
# TODO: set up proper logging app with handler, formatter, etc...
logging.basicConfig(
    # filename='output.log',
    format='%(levelname)s %(message)s',
    level=logging.DEBUG
)


class ApplicationWindow(QMainWindow):

    def __init__(self):

        super(ApplicationWindow, self).__init__()

        self._init_ui()
        self._set_defaults()

    def _init_ui(self):

        # Styles
        self.setStyleSheet(
            """QRadioButton {
                max-width: 40px;
            }"""
        )

        bold_font = QFont()
        bold_font.setBold(True)

        title_label = QLabel(self)
        title_label.setText("PyPass3")
        title_label.move(10, 0)
        title_label.setMinimumSize(300, 20)
        title_label.setFont(bold_font)

        length_label = QLabel(self)
        length_label.setText("Length")
        length_label.move(192, 185)
        length_label.setMinimumSize(200, 20)
        length_label.setFont(bold_font)

        main_label = QLabel(self)
        main_label.setText(
            "Make robust secrets with random characters,\n"
            "words, or numbers. Or choose number of dice\n"
            "and rolls for words type passphrase. Defaults\n"
            "to 5 dice and 5 rolls.\n")
        main_label.setMinimumSize(280, 100)
        main_label.move(10, 15)

        type_label = QLabel(self)
        type_label.setText("Secret type")
        type_label.move(10, 87)
        type_label.setFont(bold_font)

        dice_label = QLabel(self)
        dice_label.setText("Number of dice")
        dice_label.move(10, 138)
        dice_label.setMinimumSize(280, 20)
        dice_label.setFont(bold_font)

        rolls_label = QLabel(self)
        rolls_label.setText("Number of rolls")
        rolls_label.move(10, 190)
        rolls_label.setMinimumSize(280, 20)
        rolls_label.setFont(bold_font)

        self.textbox = QTextEdit(self)
        self.textbox.setMinimumSize(280, 100)
        self.textbox.move(10, 245)
        self.textbox.setFontFamily("Courier New")

        self.length_textline = QLineEdit(self)
        self.length_textline.setMinimumSize(100, 20)
        self.length_textline.move(190, 210)

        min_width = 125
        # max_width = 150

        # Add Generate button
        generate_btn = QPushButton('Generate', self)
        generate_btn.setToolTip('Click to generate secret')
        # generate_btn.clicked.connect(on_click)
        generate_btn.clicked.connect(self._on_click)
        generate_btn.move(10, 355)
        generate_btn.setMinimumWidth(min_width)

        # Add Quit button
        quit_btn = QPushButton('Quit', self)
        quit_btn.setToolTip('Quit this application')
        quit_btn.clicked.connect(exit)
        quit_btn.move(165, 355)
        quit_btn.setMinimumWidth(min_width)

        # Add Copy button
        copy_btn = QPushButton('Copy', self)
        copy_btn.setToolTip('Copy your secret')
        copy_btn.clicked.connect(self._copy_textbox)
        copy_btn.move(250, 320)
        copy_btn.setMaximumWidth(35)
        copy_btn.setMaximumHeight(20)
        copy_btn.setStyleSheet('font-size: 11px;')

        # Add Help button
        help_btn = QPushButton('Help', self)
        help_btn.setToolTip('Get help about this application')
        help_btn.clicked.connect(self._open_help)
        help_btn.move(240, 80)
        help_btn.setMaximumWidth(35)
        help_btn.setMaximumHeight(20)
        help_btn.setStyleSheet('font-size: 11px;')

        hr1 = QFrame(self)
        hr1.setFrameShape(QFrame.HLine)
        hr1.move(10, 125)
        hr1.setMinimumWidth(280)
        hr1.setStyleSheet("color: #d0d0d0;")

        hr2 = QFrame(self)
        hr2.setFrameShape(QFrame.HLine)
        hr2.move(10, 175)
        hr2.setMinimumWidth(100)
        hr2.setStyleSheet("color: #d0d0d0;")

        # Add secret type radio buttons
        self.words_radio_btn = QRadioButton('words', self)
        self.words_radio_btn.move(10, 110)
        self.words_radio_btn.clicked.connect(self._set_word_defaults)
        self.words_radio_btn.setStyleSheet('max-width: 80px;')

        self.mixed_radio_btn = QRadioButton('mixed', self)
        self.mixed_radio_btn.move(90, 110)
        self.mixed_radio_btn.clicked.connect(self._disabled_unused)
        self.mixed_radio_btn.setStyleSheet('max-width: 80px;')

        self.numbers_radio_btn = QRadioButton('numbers', self)
        self.numbers_radio_btn.move(170, 110)
        self.numbers_radio_btn.clicked.connect(self._disabled_unused)
        self.numbers_radio_btn.setStyleSheet('max-width: 100px;')

        # Add dice roll radio buttons
        self.num_dice4 = QRadioButton('4', self)
        self.num_dice4.move(10, 160)
        
        self.num_dice5 = QRadioButton('5', self)
        self.num_dice5.move(60, 160)
        
        self.num_rolls3 = QRadioButton('3', self)
        self.num_rolls3.move(10, 212)
        
        self.num_rolls4 = QRadioButton('4', self)
        self.num_rolls4.move(60, 212)
        
        self.num_rolls5 = QRadioButton('5', self)
        self.num_rolls5.move(110, 212)

        self.radio_type_group = QButtonGroup(self)
        self.radio_type_group.addButton(self.words_radio_btn)
        self.radio_type_group.addButton(self.mixed_radio_btn)
        self.radio_type_group.addButton(self.numbers_radio_btn)

        self.radio_dice_group = QButtonGroup(self)
        self.radio_dice_group.addButton(self.num_dice4)
        self.radio_dice_group.addButton(self.num_dice5)

        self.radio_rolls_group = QButtonGroup(self)
        self.radio_rolls_group.addButton(self.num_rolls3)
        self.radio_rolls_group.addButton(self.num_rolls4)
        self.radio_rolls_group.addButton(self.num_rolls5)

        self.setGeometry(100, 100, 300, 400)
        self.setWindowTitle('Password Generator')
        self.setWindowIcon(QIcon('../images/lock_icon_bkgrd.png'))

    def _set_defaults(self):

        self.words_radio_btn.setChecked(True)
        self.num_dice5.setChecked(True)
        self.num_rolls5.setChecked(True)
        self.length_textline.setText('')

    def _run_generate(self):

        logging.info(
            '[{0}]\n{1}'.format(utils.get_timestamp(), self._get_args()))

        return generate_secret(
            int(self._get_args()['number_rolls']),
            int(self._get_args()['number_dice']),
            int(self._get_args()['how_many']),
            str(self._get_args()['output_type']),
            int(self._get_args()['password_length'])
        )

        # def generate_secret(number_rolls: int = 5, number_dice: int = 5,
        #                       how_many: int = 1, output_type: str = 'words',
        #                       password_length: int = 20)

        # output_type=self._get_args()['output_type'],
        # password_length=int(self._get_args()['password_length']),
        # number_dice=int(self._get_args()['number_dice']),
        # number_rolls=int(self._get_args()['number_rolls'])

    def _on_click(self):

        self.textbox.setFontFamily("Courier New")

        return self.textbox.setText(self._run_generate())

    def _get_args(self):

        args = {'password_length': 20, 'how_many': 1}

        # Type
        if self.numbers_radio_btn.isChecked():
            args['output_type'] = self.numbers_radio_btn.text()

        elif self.mixed_radio_btn.isChecked():
            args['output_type'] = self.mixed_radio_btn.text()

        else:
            args['output_type'] = self.words_radio_btn.text()

        # Length
        if self.length_textline.text():
            args['password_length'] = self.length_textline.text()

        # Dice
        if self.num_dice4.isChecked():
            args['number_dice'] = self.num_dice4.text()

        else:
            args['number_dice'] = self.num_dice5.text()

        # Rolls
        if self.num_rolls3.isChecked():
            args['number_rolls'] = self.num_rolls3.text()

        elif self.num_rolls4.isChecked():
            args['number_rolls'] = self.num_rolls4.text()

        else:
            args['number_rolls'] = self.num_rolls5.text()

        return args

    def _disabled_unused(self):

        tmp_text = self.length_textline.text()

        if tmp_text:
            self.length_textline.setText(tmp_text)
        else:
            self.length_textline.setText('20')

        self.radio_dice_group.setExclusive(False)
        self.radio_rolls_group.setExclusive(False)

        self.num_dice4.setChecked(False)
        self.num_dice4.setCheckable(False)
        self.num_dice4.setEnabled(False)

        self.num_dice5.setChecked(False)
        self.num_dice5.setCheckable(False)
        self.num_dice5.setEnabled(False)

        self.num_rolls3.setChecked(False)
        self.num_rolls3.setCheckable(False)
        self.num_rolls3.setEnabled(False)

        self.num_rolls4.setChecked(False)
        self.num_rolls4.setCheckable(False)
        self.num_rolls4.setEnabled(False)

        self.num_rolls5.setChecked(False)
        self.num_rolls5.setCheckable(False)
        self.num_rolls5.setEnabled(False)

        self.radio_dice_group.setExclusive(True)
        self.radio_rolls_group.setExclusive(True)

    def _set_word_defaults(self):

        self.length_textline.setText('')

        self.num_dice4.setCheckable(True)
        self.num_dice4.setEnabled(True)

        self.num_dice5.setCheckable(True)
        self.num_dice5.setEnabled(True)

        self.num_rolls3.setCheckable(True)
        self.num_rolls3.setEnabled(True)

        self.num_rolls4.setCheckable(True)
        self.num_rolls4.setEnabled(True)

        self.num_rolls5.setCheckable(True)
        self.num_rolls5.setEnabled(True)

        self.num_dice5.setChecked(True)
        self.num_rolls5.setChecked(True)

    def _copy_textbox(self):

        self.textbox.selectAll()
        self.textbox.copy()

    def _open_help(self):

        message = QMessageBox(self)

        with open('../assets/help/_main.txt', 'r') as help_text:
            message.setText(help_text.read())

        message.setIcon(QMessageBox.Question)

        with open('../assets/help/_inform.txt', 'r') as help_inform:
            message.setInformativeText(help_inform.read())

        message.setWindowTitle('PyPass3 Help')
        message.setStandardButtons(QMessageBox.Close)
        message.exec_()


def main():

    app = QApplication(sys.argv)

    window = ApplicationWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

