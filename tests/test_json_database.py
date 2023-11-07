from pathlib import Path
from util import JSONDatabase

initial_data = {
    "float": 1.5,
    "int": 20,
    "string": "Pythons",
    "array": ["A", "B", "C"],
    "person": {
        "name": "David",
        "score": 20
    }
}

basic_database_filename = "test_database.json"
expected_path = Path(".", "data", basic_database_filename)
expected_path.unlink(missing_ok=True) # Delete the database file from any previous runs

basic_database = JSONDatabase(basic_database_filename, initial_data)

def test_database_path():
    """Test that the database is being stored at the expected path"""
    assert basic_database.get_file_path() == expected_path


def test_intial_data_datatypes():
    """Test that the initial data has been loaded into the database with correct datatypes"""
    assert isinstance(basic_database.data["float"], float)
    assert isinstance(basic_database.data["int"], int)
    assert isinstance(basic_database.data["string"], str)
    assert isinstance(basic_database.data["array"], list)
    assert isinstance(basic_database.data["person"], dict)

def test_intial_data_nested_dicts():
    """Test that nested dictionaries are loaded from the initial data"""
    assert basic_database.data["person"]["score"] == 20