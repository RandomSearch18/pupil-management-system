from util import JSONDatabase, get_path_in_dictionary


class SettingsDatabase(JSONDatabase):

    DEFAULT_SETTINGS = {
        "tui": {
            "onboarding": {
                "show": True,
                "stage": None
            }
        }
    }

    # A unique object used to represent the value of a setting that was not present in the database 
    NOT_FOUND = object()

    def __init__(self):
        super().__init__("settings.json", self.DEFAULT_SETTINGS)
    
    def get_from_database(self, *path: str):
        """Gets a value from the settings database, without filling defaults
        
        - Note that a default value may still be returned, as defaults are added to the database on the first run of the program.
        - If the path isn't present in the database, the SettingsDatabase.NOT_FOUND object is returned
        """
        # Stores the dictionary we're checking (with the setting somewhere inside), or the setting itself
        matching_setting = self.data
        
        for path_item in path:
            try:
                matching_setting = matching_setting[path_item]
            except KeyError:
                # The setting at the specified path doesn't exist
                return self.NOT_FOUND
        
        # Finished searching, so we must have the actual setting value now
        return matching_setting


    def get(self, *path: str):
        """Gets the value of a setting at the provided path
        
        - If the setting isn't currently present in the database, returns the default value for that setting
        - If a default value doesn't exist, raises a KeyError
        """
        saved_value = self.get_from_database(*path)

        if saved_value is not self.NOT_FOUND:
            return saved_value

        try:
            default_value = get_path_in_dictionary(self.DEFAULT_SETTINGS, *path)
        except KeyError:
            path_string = ".".join(path)
            raise KeyError(f"Setting does not exist: {path_string}")
        
        return default_value
        
    def set(self, *path: str, value):
        # Stores the dictionary we're checking (with the target setting nested somewhere inside)
        current_dictionary = self.data
        while len(path) > 1:
            current_dictionary = current_dictionary[path[0]]
            path = path[1:]
        
        # No levels of nested dictionaries remain
        key = path[0]
        current_dictionary[key] = value

        self.save()
        return value