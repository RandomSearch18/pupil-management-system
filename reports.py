from menu import Menu, Option


def reports_menu():
    menu = Menu(
        [
            Option(
                "Birthdays this month", input, description="TODO: Write explanation"
            ),
            Option(
                "Alphabetical order",
                input,
                description="TODO: Write another explanation!",
            ),
        ],
        "Choose a report to view",
    )
    menu.show()
