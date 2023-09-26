"""Mr Leeman's System: A pupil management system for Tree Road School
This code is for Task 3 of the lesson 2.2.1 Programming fundamentals - validation"""

from menu import Menu, Option


def log_in():
    print("Logging in")


main_menu = Menu([Option("Log in", log_in)], title="Mr Leeman's system")

main_menu.show()
