import datetime
from typing import Callable, Optional

from colorama import Style
from menu import bold, color, info_line

from util import JSONDatabase


class StudentsReport:
    def __init__(
        self, students: list[dict], filter_function: Callable[[list[dict]], bool], title: str
    ):
        self.students = students
        self.filter = filter_function
        self.title = title

    def get_matching_students(self) -> list[dict]:
        matching_students = filter(self.filter, self.students)
        return matching_students
    
    def display(self):
        """Prints the report's contents, with nice formatting"""
        students = self.get_matching_students()
        print(bold(self.title))
        for i, student in enumerate(students):
            index = i + 1
            index_part = color(f"{index:3})", Style.DIM)
            name_part = student["full_name"]
            print(f"{index_part} {name_part}")


class StudentsDatabase(JSONDatabase):
    def __init__(self):
        super().__init__("students.json", [])

        def report_birthday_this_month(student):
            birthday = datetime.date.fromisoformat(student["birthday"])
            return birthday.month == datetime.date.today().month


        self.report_birthday_this_month = StudentsReport(self.data, report_birthday_this_month, "Birthdays this month")

    def get_student(
        self, id: Optional[int] = None, email_address: Optional[str] = None
    ) -> Optional[dict]:
        """Looks up a student using the provided unique identifier(s)

        - The student's ID and/or email address can be provided as search criteria
        - If more than one datapoint is provided, the ID takes precedence
        - Returns a dictionary of the student's data
        """
        for student in self.data:
            if id and student["id"] == id:
                return student
            if email_address and student["school_email"] == email_address:
                return student
        return None

    def next_id(self):
        return len(self.data) + 1

    def generate_email_address(self, surname, forename, discriminator: int = 0):
        domain = "tree-road.edu"
        surname_part = surname.lower()
        forename_part = forename.lower()[0]
        # If the discriminator is 0, don't include it at all:
        discriminator_part = str(discriminator) if discriminator else ""

        possible_email = f"{surname_part}{forename_part}{discriminator_part}@{domain}"

        # Check if the addresss is taken
        if self.get_student(email_address=possible_email):
            # Increment the discriminator
            discriminator = discriminator + 1
            return self.generate_email_address(surname, forename, discriminator)

        return possible_email

    def get_students(self, current_account) -> list[dict]:
        """Returns a list of all the students"""
        # TODO: In the future, we can only return students that are akkiwed to be accessed by the current user.
        if not current_account:
            # Users that aren't signed in don't get to access student data
            return []
        return self.data.copy()

    def add_student(
        self,
        surname: str,
        forename: str,
        birthday: datetime.date,
        home_address: str,
        home_phone: str,
        tutor_group: str,
    ):
        """Creates a dictionary to repsresnt a new student and adds it to the database.

        - A unique numerical ID is generated for the student, as well as a unique school email address
        - The provided surname and forename are normalised to title case
        - The provided tutor group is normalised to uppercase
        - The provided birthday is converted to a ISO-8601 timestamp
        - The other data (home address and phone number) is left as-is
        - Returns the directory of the student's data
        """

        email_address = self.generate_email_address(surname, forename)
        full_name = " ".join([forename, surname])

        new_student = {
            "surname": surname.strip().title(),
            "forename": forename.strip().title(),
            "birthday": birthday.isoformat(),
            "tutor_group": tutor_group.strip().upper(),
            "home_address": home_address,
            "home_phone": home_phone,
            "id": self.next_id(),
            "school_email": email_address,
            "full_name": full_name,
        }
        self.data.append(new_student)
        self.save()
        return new_student

    def display_student_info(self, student):
        birthday = datetime.date.fromisoformat(student["birthday"])
        formatted_id = color(f"(#{student['id']})", Style.DIM)

        print(f"Details for {bold(student['full_name'])} {formatted_id}")
        info_line("Surname", student["surname"])
        info_line("Forename", student["forename"])
        info_line("Birthday", birthday.strftime("%x"))
        info_line("Tutor group", student["tutor_group"])
        info_line("Home phone number", student["home_phone"])
        info_line("School email address", student["school_email"])

