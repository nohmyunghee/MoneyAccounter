import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Accounter import *
from Accounter import Accounter
from ui_window import Ui_MainWindow
import pandas as pd

def row_to_table(ui, row_series, num = None):
    """Writes row_series to ui.table"""
    if num is None:
        num = ui.table.rowCount()
    ui.table.insertRow(num)
    ui.table.setItem(num, 0, QTableWidgetItem(str(row_series['value'])))
    ui.table.setItem(num, 1, QTableWidgetItem(row_series['date'].strftime("%d/%m/%Y")))
    ui.table.setItem(num, 2, QTableWidgetItem(row_series['comment']))

def load_to_table(ui, acc):
    """Loads contents of acc to table widget"""
    # print(acc)

    # do things i didn't find a way to do with qt designer
    ui.table.setHorizontalHeaderItem(0, QTableWidgetItem("how much"))
    ui.table.setHorizontalHeaderItem(1, QTableWidgetItem("when"))
    ui.table.setHorizontalHeaderItem(2, QTableWidgetItem("comment"))
    ui.table.setColumnWidth(0, 100)
    ui.table.setColumnWidth(1, 100)
    ui.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)

    print(acc.account)
    for i, row in acc.account.iloc[::-1].iterrows():
        # print(i)
        # print(row)
        row_to_table(ui, row)

def make_push_button_clicked(acc, ui):
    """Function for push button clocking"""
    def push_button_clicked():
        # print(acc.account)
        value = ui.amountLine.text()
        comment = ui.commentLine.text()
        # print(ui.checkBox.isChecked())
        # print(date)
        if ui.use_this_date_cb.isChecked():
            date = ui.dateEdit.date().toPyDate().strftime("%Y%m%d")
            acc.add_new_data(value=value, comment=comment, date=date)
        else:
            acc.add_new_data(value=value, comment=comment)
        row_to_table(ui, acc.account.iloc[len(acc.account.index) - 1], 0)
    return push_button_clicked

def make_pop_button_clicked(acc, ui):
    """Function for pop button clocking"""
    def pop_button_clicked():
        acc.account = acc.account.drop(acc.account.tail(1).index)
        # print(acc)
        ui.table.removeRow(0)
    return pop_button_clicked

def make_filter_button_clicked(acc, ui):
    """Function for filter button clocking"""
    def filter_button_clicked():
        print("filter")
        new_acc = acc;
        if ui.by_date_cb.isChecked():
            print("by date")
            new_acc = new_acc.get_by_date(ui.from_date.date().toPyDate().strftime("%Y%m%d"), ui.to_date.date().toPyDate().strftime("%Y%m%d"))
        if ui.sort_by_value_cb.isChecked():
            print("by val")
            new_acc.account =  new_acc.account.sort_values(["value"])
        if ui.by_comment_cb.isChecked():
            print("by comment")
            new_acc = new_acc.get_by_comment(ui.by_comment_le.text())
        print(new_acc)
        while ui.table.rowCount() > 0:
            ui.table.removeRow(0)
        load_to_table(ui, new_acc)
    return filter_button_clicked

def start():
    """Starts application"""
    app = QApplication(sys.argv)
    window = QDialog()
    QShortcut(QKeySequence("Ctrl+Q"), window, window.close)
    
    ui = Ui_MainWindow()
    ui.setupUi(window)
    ui.dateEdit.setDate(QDate.currentDate())
    ui.from_date.setDate(QDate.currentDate())
    ui.to_date.setDate(QDate.currentDate())
    
    acc = Accounter()
    
    acc.load_data()
    acc.sort_by_date()
    load_to_table(ui, acc)

    ui.push_button.clicked.connect(make_push_button_clicked(acc, ui))
    ui.pop_button.clicked.connect(make_pop_button_clicked(acc, ui))
    ui.filter_button.clicked.connect(make_filter_button_clicked(acc, ui))
    
    window.show()
    app.exec_()
    acc.save_data()

if __name__== "__main__":
    start()
    sys.exit()
