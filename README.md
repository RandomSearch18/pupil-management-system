# Mr Leeman's System

A menu-based tool for viewing, searching, and managing pupils' details, made using Python. In other words, it's a pupil management system.

## Screenshots

![Screenshot of the program running in a terminal. A new account is being created, with inputs and descriptive text for the Username and Password fieldsScreenshot from 2023-10-17 20-02-13](https://github.com/RandomSearch18/pupil-management-system/assets/101704343/3e8c29a3-7515-4798-9e0c-615c4cf28290)
![image](https://github.com/RandomSearch18/pupil-management-system/assets/101704343/a251081d-e807-4a75-8867-0e1534317b30)
![Screenshot of the program running in a terminal. The user has asked for information about student #3, and their details have been printed.](https://github.com/RandomSearch18/pupil-management-system/assets/101704343/df6805ed-efc8-478a-b88e-cbcf7ecd5b56)


## Usage

Tested with Python 3.9 and 3.10. Will probably work with newer versions too. This project uses [Poetry](https://python-poetry.org/docs/) to manage Python libraries.

```bash
$ poetry install
$ poetry run python main.py
```

Alternatively, you can manually install [the required Python libraries](#libraries) using `pip`.

## Documentation

### Libraries

This program uses a few libraries to provide functionality that I wouldn't want to implement myself, like password hashing and regular expression support.

- `bcrypt` - Used for secure password storage with its password hashing features
- `regex` - Provides regular expression functionality with more features than the built-in `re` module, which is important for implementing robust validation
- `colorama` - Provides shorthands for terminal color codes, and makes sure they work on all platforms
- `phonenumbers` - The de-facto standard library for parsing and validating (inter)national phone number formats. This lets the program accurately and consistently work with any phone number.
