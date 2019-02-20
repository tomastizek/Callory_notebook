import json
import sqlite_connector as sqlite
import calc_notebook
import sys

from PyQt5 import QtWidgets, QtGui


class Window(QtWidgets.QMainWindow):

    def __init__(self, **kwargs):
        super(Window, self).__init__(**kwargs)

        self.setWindowTitle("calc_notebook")
        self.init_gui()
        self.show()

    def init_gui(self):
        formular = QtWidgets.QWidget()
        formular_layout = QtWidgets.QVBoxLayout()
        formular.setLayout(formular_layout)




class User:
    def __init__(self):
        self.name = None
        self.age = None
        self.height = None
        self.weight = None
        self.bmi = None
        self.gender = None
        self.bmr = None


def get_user_info(user):
    dict_info = {"name": user.name, "age": user.age, "height": user.height,
                 "weight": user.weight,
                 "bmi": user.bmi, "gender": user.gender, "bmr": user.bmr}

    return dict_info


def get_user_bmi(weight, height):
    round_height = height ** 2
    bmi = weight / round_height
    return bmi


def get_user_bmr(gender, weight, height, age):

    bmr = None

    if gender == "male":
        bmr = 66.5 + (13.75 * weight) + (5 * height) - (6.755 * age)

    elif gender == "female":
        bmr = 655.1 + (9.6 * weight) + (1.8 * height) - (4.7 * age)

    else:
        print("wrong input")
    return bmr


def write_to_json(data):
    with open("stats.json", "a+") as f:
        f.write("\n")
        json.dump(data, f, separators=(',', ':'))


def write_to_db(sqlite, database, data):
    conn = sqlite.create_connection(database)

    conn.execute("INSERT INTO user_stats VALUES (?,?,?,?,?,?,?)",
              [data["name"], data["age"],
               data["weight"], data["height"],
               data["bmi"],
               data["gender"],
               data['bmr']])

    conn.commit()


def click_calculate(user, window):

    user.name = window.name.text()
    user.age = window.age.text()
    user.height = window.height.text()
    user.weight = window.weight.text()
    user.gender = window.gender.text()


def save_data(sqlite, database, data):

    write_to_db(sqlite, database, data)
    write_to_json(data)


def main():
    db = "stats.db"
    app = calc_notebook.QtWidgets.QApplication(sys.argv)
    window = calc_notebook.Ui_MainWindow()
    user = User()

    window.setupUi(QtWidgets.QMainWindow())

    window.pushButton.clicked.connect(click_calculate(user, window))

    user.bmi = get_user_bmi(user.weight, user.height)
    user.bmr = get_user_bmr(user.gender, user.weight, user.height, user.age)

    data = get_user_info(user)

    save_data(sqlite, db, data)

    print(data)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
