import datetime

from util import JSONDatabase


class StudentsDatabase(JSONDatabase):

    def __init__(self):
        super().__init__("students.json", [])

    def get_student(self, id: int | None,
                    email_address: str | None) -> dict | None:
        """Looks up a student using the provided unique identifier(s)
        
        - The student's ID and/or email address can be provided as search criteria
        - If more than one datapoint is provided, the ID takes precedence 
        - Returns a dictionary of the student's data
        """
        for student in self.data:
            if id and student["id"] == id:
                return student
            if email_address and student["email_address"] == email_address:
                return student
        return None

    def add_student(self, surname: str, forename: str, birthday: datetime.date,
                    home_address: str, home_phone: str, tutor_group: str):
        """Creates a dictionary to repsresnt a new student and adds it to the database.

        - A unique numerical ID is generated for the student, as well as a unique school email address
        - The provided surname and forename are normalised to title case
        - The provided tutor group is normalised to uppercase
        - The provided birthday is converted to a ISO-8601 timestamp
        - The other data (home address and phone number) is left as-is
        - Returns the directory of the student's data
        """

        new_student = {
            "surname": surname.strip().title(),
            "forename": forename.strip().title(),
            "birthday": birthday.isoformat(),
            "tutor_group": tutor_group.strip().upper(),
            "home_address": home_address,
            "home_phone": home_phone,
        }
        self.data.append(new_student)
        self.save()
        return new_student
