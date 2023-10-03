import datetime

from util import JSONDatabase


class StudentsDatabase(JSONDatabase):

    def __init__(self):
        super().__init__("students.json", [])

    def get_student(self,
                    id: int | None = None,
                    email_address: str | None = None) -> dict | None:
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

    def generate_email_address(self,
                               surname,
                               forename,
                               discriminator: int = 0):
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
            return self.generate_email_address(surname, forename,
                                               discriminator)

        return possible_email

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

        email_address = self.generate_email_address(surname, forename)

        new_student = {
            "surname": surname.strip().title(),
            "forename": forename.strip().title(),
            "birthday": birthday.isoformat(),
            "tutor_group": tutor_group.strip().upper(),
            "home_address": home_address,
            "home_phone": home_phone,
            "id": self.next_id(),
            "school_email": email_address
        }
        self.data.append(new_student)
        self.save()
        return new_student
