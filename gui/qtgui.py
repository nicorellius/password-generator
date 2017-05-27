#!/usr/bin/env python

import os
import sys

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from scripts.generate import generate_secret


def window():

    app = QApplication(sys.argv)
    w = QWidget()

    main_label = QLabel(w)
    type_label = QLabel(w)
    dice_label = QLabel(w)
    rolls_label = QLabel(w)

    # def run_generate():
    #     return generate_secret()
    #
    # def on_click():
    #     return textbox.setText(run_generate())
    #
    # def get_arg():
    #
    #     if words_radio_btn.isChecked():
    #         arg = words_radio_btn.text()
    #
    #     elif mixed_radio_btn.isChecked():
    #         arg = mixed_radio_btn.text()
    #
    #     else:
    #         arg = numbers_radio_btn.text()
    #
    #     print(arg)
    #     return str(arg)

    def run_function():

        if words_radio_btn.isChecked():

            arg = words_radio_btn.text()

        elif mixed_radio_btn.isChecked():
            arg = mixed_radio_btn.text()

        else:
            arg = numbers_radio_btn.text()

        print(arg)

        result = generate_secret(str(arg))

        print(result)

        textbox.setText(result)

    def disabled_unused():

        radio_dice_group.setExclusive(False)
        radio_rolls_group.setExclusive(False)

        num_dice1.setChecked(False)
        num_dice2.setChecked(False)

        num_rolls1.setChecked(False)
        num_rolls2.setChecked(False)

        radio_dice_group.setExclusive(True)
        radio_rolls_group.setExclusive(True)

    def set_defaults():

        num_dice2.setChecked(True)
        num_rolls2.setChecked(True)

    textbox = QTextEdit(w)
    textbox.setMaximumSize(320, 100)

    # Add secret type radio buttons
    words_radio_btn = QRadioButton('words')
    words_radio_btn.clicked.connect(set_defaults)

    mixed_radio_btn = QRadioButton('mixed')
    mixed_radio_btn.clicked.connect(disabled_unused)

    numbers_radio_btn = QRadioButton('numbers')
    numbers_radio_btn.clicked.connect(disabled_unused)

    # Add dice roll radio buttons
    num_dice1 = QRadioButton('4')
    num_dice2 = QRadioButton('5')

    num_rolls1 = QRadioButton('4')
    num_rolls2 = QRadioButton('5')

    radio_type_group = QButtonGroup(w)
    radio_type_group.addButton(words_radio_btn)
    radio_type_group.addButton(mixed_radio_btn)
    radio_type_group.addButton(numbers_radio_btn)

    radio_dice_group = QButtonGroup(w)
    radio_dice_group.addButton(num_dice1)
    radio_dice_group.addButton(num_dice2)

    radio_rolls_group = QButtonGroup(w)
    radio_rolls_group.addButton(num_rolls1)
    radio_rolls_group.addButton(num_rolls2)

    width = 157

    # Add Generate button
    generate_btn = QPushButton("Generate", w)
    generate_btn.setToolTip('Click to generate password!')
    # generate_btn.clicked.connect(on_click)
    generate_btn.clicked.connect(run_function)
    generate_btn.move(13, 300)
    generate_btn.setMaximumWidth(width)

    # Add Quit button
    quit_btn = QPushButton("Quit", w)
    quit_btn.setToolTip('Click to quit!')
    quit_btn.clicked.connect(exit)
    quit_btn.move(180, 300)
    quit_btn.setMaximumWidth(width)

    # Add Copy button
    # btn3 = QPushButton('Copy', w)
    # btn3.setToolTip('Copy the secret!')
    # btn3.clicked.connect(exit)
    # btn3.move(230, 240)
    # btn2.setMinimumWidth(width)

    main_label.setText(
        "Generate a password or passphrase with either\n"
        "random characters, words, or numbers. Optionally,\n"
        "choose number of dice and rolls for passphrase\n"
        "word selection. Defaults to 5 and 5.\n"
        "Check out eff.org/dice for more details...\n")
    # "Click generate to make your secret!\n")
    # lbl.move(100, 50)

    type_label.setText("Set secret type")
    dice_label.setText("Set number of dice")
    rolls_label.setText("Set number of rolls")

    # Set layout sections
    top_layout = QHBoxLayout()
    top_layout.addWidget(main_label)
    top_layout.addStrut(50)

    type_layout = QHBoxLayout()
    type_layout.addWidget(type_label)
    type_layout.addWidget(words_radio_btn)
    type_layout.addWidget(mixed_radio_btn)
    type_layout.addWidget(numbers_radio_btn)
    type_layout.addStrut(50)

    dice_layout = QHBoxLayout()
    dice_layout.addWidget(dice_label)
    dice_layout.addWidget(num_dice1)
    dice_layout.addWidget(num_dice2)

    rolls_layout = QHBoxLayout()
    rolls_layout.addWidget(rolls_label)
    rolls_layout.addWidget(num_rolls1)
    rolls_layout.addWidget(num_rolls2)

    text_layout = QHBoxLayout()
    text_layout.addWidget(textbox)

    button_layout = QHBoxLayout()
    button_layout.addWidget(generate_btn)
    button_layout.addWidget(quit_btn)

    layout = QVBoxLayout()
    layout.addLayout(top_layout)
    layout.addLayout(type_layout)
    layout.addLayout(dice_layout)
    layout.addLayout(rolls_layout)
    layout.addLayout(text_layout)
    layout.addLayout(button_layout)
    layout.addStretch(30)
    w.setLayout(layout)

    # textbox.setPlainText()

    w.setGeometry(100, 100, 300, 350)
    w.setWindowTitle("Password Generator")
    w.setWindowIcon(QIcon('../images/lock_icon_bkgrd.png'))
    w.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    window()

