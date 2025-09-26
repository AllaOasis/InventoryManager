# Inventory Management Application - A Python-based inventory management system using PyQt6
# Copyright (C) 2025 Lackovič Aljaž
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See <https://www.gnu.org/licenses/> for more details.
#
# Dependencies:
#  - PyQt6 (GPLv3) for the graphical user interface

from PyQt6.QtWidgets import  (
    QMainWindow, 
    QLineEdit, 
    QWidget, 
    QLabel, 
    QDialog, 
    QPushButton,
    QMenuBar,
    QTableWidget,
    QSpinBox,
    QComboBox,
)

class WidgetStyle(QWidget):

    # -------------------------------
    # Theme dictionary
    # -------------------------------
    theme = {
        "bgColor": "#2C2C2C",
        "textColor": "#FFFFFF",
        "accentColor": "#FF6A13",
        "borderColor": "#616161",
        "focusColor": "#FF7043",
        "pressedColor": "#FF3D00",
        "errorBgColor": "#3E2723",
        "errorBorderColor": "#D32F2F",
        "errorFocusColor": "#FFECB3",
        "disabledColor": "#CCCCCC",
        "disabledBgColor": "#505E65",
        "disabledBorderColor": "#B0BEC5",
        "headerBgColor": "#424242",
        "gridLineColor": "#444444",
        "menuBgColor": "#333333",
    }

    # -------------------------------
    # Input styles
    # -------------------------------
    inputDefault = """
    QLineEdit {{
        background-color: {headerBgColor};
        color: {textColor};
        border: 2px solid {borderColor};
        border-radius: 4px;
        padding: 0px 2px;
        font-size: 14px;
    }}
    QLineEdit:focus {{
        border-color: {accentColor};
        background-color: {focusColor};
    }}
    """.format(**theme)

    inputError = """
    QLineEdit {{
        background-color: {errorBgColor};
        color: {accentColor};
        border: 2px solid {errorBorderColor};
        border-radius: 4px;
        padding: 0px 2px;
        font-size: 14px;
    }}
    QLineEdit:focus {{
        border-color: {accentColor};
        background-color: {errorFocusColor};
    }}
    """.format(**theme)

    # -------------------------------
    # Button styles
    # -------------------------------
    buttonDefault = """
    QPushButton {{
        background-color: {headerBgColor};
        color: {textColor};
        border: 2px solid {borderColor};
        border-radius: 4px;
        padding: 2px 8px;
        font-size: 14px;
    }}
    QPushButton:hover {{
        background-color: {accentColor};
        border-color: {accentColor};
    }}
    QPushButton:focus {{
        outline: none;
        border-color: {accentColor};
        background-color: {focusColor};
    }}
    QPushButton:pressed {{
        background-color: {pressedColor};
        border-color: {accentColor};
    }}
    QPushButton:disabled {{
        background-color: {disabledBgColor};
        color: {disabledColor};
        border: 2px solid {disabledBorderColor};
    }}
    """.format(**theme)

    # -------------------------------
    # Label styles
    # -------------------------------
    labelDefault = """
    QLabel {{
        color: {textColor};
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 5px;
    }}
    """.format(**theme)

    labelError = """
    QLabel {{
        color: {accentColor};
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 5px;
    }}
    """.format(**theme)

    # -------------------------------
    # Menu styles
    # -------------------------------
    menuDefault = """
    QMenuBar {{
        background-color: {menuBgColor};
        color: {textColor};
        padding: 0px 2px;
    }}
    QMenuBar::item {{
        background-color: {gridLineColor};
        color: {textColor};
        padding: 10px 15px;
        border-radius: 4px;
        margin: 0px 2px;
    }}
    QMenuBar::item:selected {{
        background-color: {accentColor};
        color: {textColor};
    }}
    QMenuBar::item:disabled {{
        color: {disabledColor};
        background-color: {disabledBgColor};
    }}
    QMenuBar::item:hover {{
        background-color: {accentColor};
        color: {textColor};
    }}

    QMenu {{
        padding: 2px;
        background-color: {gridLineColor};
        color: {textColor};
        border-radius: 8px;
    }}
    QMenu::item {{
        padding: 5px 15px;
        background-color: {gridLineColor};
        color: {textColor};
        border-radius: 4px;
        margin: 2px 0px;
    }}
    QMenu::item:selected {{
        background-color: {accentColor};
        color: {textColor};
        border-radius: 4px;
    }}
    QMenu::item:disabled {{
        padding: 5px 15px;
        background-color: {disabledBgColor};
        color: {disabledColor};
        border-radius: 4px;
    }}
    QMenu::item:hover {{
        background-color: {accentColor};
        color: {textColor};
    }}
    """.format(**theme)

    # -------------------------------
    # Table styles
    # -------------------------------
    tableDefault = """
    QTableWidget {{
        background-color: {bgColor};
        color: {textColor};
        gridline-color: {gridLineColor};
        border: 2px solid {borderColor};
        border-radius: 6px;
        font-size: 14px;
    }}
    QTableWidget::item {{
        selection-background-color: {accentColor};
        selection-color: {textColor};
    }}
    QHeaderView::section {{
        background-color: {headerBgColor};
        color: {textColor};
        padding: 6px;
        border: 1px solid {borderColor};
        font-weight: bold;
    }}
    QTableCornerButton::section {{
        background-color: {headerBgColor};
        border: 1px solid {borderColor};
    }}
    """.format(**theme)

    logTable = """
        QTableWidget {
            background-color: #2C2C2C;     /* Dark background */
            color: #FFFFFF;                /* White text */
            gridline-color: #444444;       /* Subtle grid lines */
            border: 2px solid #616161;     /* Dark gray border */
            border-radius: 6px;
            font-size: 14px;
        }

        QTableWidget::item {
            selection-background-color: #FF6A13; /* KUKA Orange for selected rows */
            selection-color: #FFFFFF;            /* White text when selected */
        }

        QHeaderView::section {
            background-color: #424242;     /* Dark gray for headers */
            color: #FFFFFF;                /* White text in headers */
            padding: 6px;
            border: 1px solid #616161;     /* Border between header cells */
            font-weight: bold;
        }

        QTableCornerButton::section {
            background-color: #424242;     /* Corner box matches header */
            border: 1px solid #616161;
        }
    """

    # -------------------------------
    # SpinBox styles
    # -------------------------------
    spinboxDefault = """
    QSpinBox {{
        background-color: {headerBgColor};
        color: {textColor};
        border: 2px solid {borderColor};
        border-radius: 4px;
        padding: 2px 4px;
        font-size: 14px;
    }}
    QSpinBox::up-button {{
        width: 20px;
    }}
    QSpinBox::down-button {{
        width: 20px;
    }}
    QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
        background-color: {accentColor};
    }}
    QSpinBox:focus {{
        border-color: {accentColor};
        background-color: {focusColor};
    }}
    """.format(**theme)

    # -------------------------------
    # Main window style
    # -------------------------------
    windowDefault = """
    QWidget {{
        background-color: {bgColor};
        color: {textColor};
    }}
    """.format(**theme)

    # -------------------------------
    # Combo box style
    # -------------------------------
    comboBoxDefault = """
        QComboBox {{
            background-color: {headerBgColor};
            color: {textColor};
            border: 2px solid {borderColor};
            border-radius: 4px;
            padding: 2px 6px;
            font-size: 14px;
            min-height: 28px;
        }}
        QComboBox:focus {{
            border-color: {accentColor};
            background-color: {focusColor};
        }}
        QComboBox::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 20px;
            border-left: 1px solid {borderColor};
        }}
        QComboBox::down-arrow {{
            image: url("Modules/icons/down-arrow.png"); /* optional */
            width: 12px;
            height: 12px;
        }}
        QComboBox QAbstractItemView {{
            border: 1px solid {borderColor};
            selection-background-color: {accentColor};
            selection-color: {textColor};
            background-color: {headerBgColor};
            padding: 2px;
            outline: 0;
        }}
        """.format(**theme)

    @staticmethod
    def setErrorStyle(widget, exitOnError = True):
        if isinstance(widget, QLabel):
            widget.setStyleSheet(WidgetStyle.labelError)
        elif isinstance(widget, QLineEdit):
            widget.setStyleSheet(WidgetStyle.inputError)
        else:
            if exitOnError:
                raise TypeError(f"Unsupported widget type: {widget.__class__.__name__}")
            else:
                print(f"Unsupported widget type: {widget.__class__.__name__}")
    
    @staticmethod
    def setDefaultStyle(widget, exitOnError = True):
        if isinstance(widget, QLabel):
            widget.setStyleSheet(WidgetStyle.labelDefault)
        elif isinstance(widget, QLineEdit):
            widget.setStyleSheet(WidgetStyle.inputDefault)
        elif isinstance(widget, QPushButton):
            widget.setStyleSheet(WidgetStyle.buttonDefault)
        elif isinstance(widget, QMenuBar):
            widget.setStyleSheet(WidgetStyle.menuDefault)
        elif isinstance(widget, QMainWindow):
            widget.setStyleSheet(WidgetStyle.windowDefault)
        elif isinstance(widget, QDialog):
            widget.setStyleSheet(WidgetStyle.windowDefault)
        elif isinstance(widget, QTableWidget):
            widget.setStyleSheet(WidgetStyle.tableDefault)
        elif isinstance(widget, QSpinBox):
            widget.setStyleSheet(WidgetStyle.spinboxDefault)
        elif isinstance(widget, QComboBox):
            widget.setStyleSheet(WidgetStyle.comboBoxDefault)
        else:
            if exitOnError:
                raise TypeError(f"Unsupported widget type: {widget.__class__.__name__}")
            else:
                print(f"Unsupported widget type: {widget.__class__.__name__}")
 