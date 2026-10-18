def add_setting(settings_dict, setting_pair):
    """
    Unpacks a (key, value) tuple and attempts to insert it into the settings dictionary.
    Rejects the addition if the key already exists (case-insensitive).
    """
    key, value = setting_pair
    key_lower = key.lower()
    value_lower = value.lower()
    
    # Check if the lowercased setting key is missing from the dictionary
    if key_lower not in settings_dict:
        settings_dict[key_lower] = value_lower
        return f"Setting '{key_lower}' added with value '{value_lower}' successfully!"
    else:
        return f"Setting '{key_lower}' already exists! Cannot add a new setting with this name."


def update_setting(settings_dict, setting_pair):
    """
    Unpacks a (key, value) tuple and updates its value in the dictionary.
    Rejects the change if the setting key does not exist yet.
    """
    key, value = setting_pair
    key_lower = key.lower()
    value_lower = value.lower()
    
    # Verify the key actually exists before attempting to modify it
    if key_lower in settings_dict:
        settings_dict[key_lower] = value_lower
        return f"Setting '{key_lower}' updated to '{value_lower}' successfully!"
    else:
        # Fixed reference: key_lower is a string variable, not a function call
        return f"Setting '{key_lower}' does not exist! Cannot update a non-existing setting."


def delete_setting(settings_dict, key):
    """
    Removes a key-value setting pair completely from the dictionary.
    If the key isn't found, returns a standard fallback error string.
    """
    key_lower = key.lower()
    
    if key_lower in settings_dict:
        del settings_dict[key_lower]  # del deletes the entry directly from memory
        return f"Setting '{key_lower}' deleted successfully!"
    else:
        return f"Setting not found!"


def view_settings(settings):
    """
    Iterates through the active configuration keys and values, formatting 
    them into a clean, capitalized, printable text summary.
    """
    # Defensive check: if the settings dictionary is empty, exit early
    if not settings:
        return "No settings available."
  
    result = "Current User Settings:\n"
    for key, value in settings.items():
        # .capitalize() converts the first character of the key to uppercase for visual layout
        result += f"{key.capitalize()}: {value}\n"
    
    return result

# --- Test Script Execution ---

# 1. Initialize a test dictionary
test_settings = {
    'theme': 'light',
    'language': 'english',
    'notifications': 'enabled'
}

# 2. Add test user settings
# Note: Passing literal dicts like {'theme': 'light'} directly below means 
# test_settings itself is unaffected by those individual print statements.
print(add_setting({'theme': 'light'}, ('THEME', 'dark')))
print(add_setting({'theme': 'light'}, ('volume', 'high')))
print(add_setting(test_settings, ("Notifications", "Enabled")))

# 3. View current configurations
print("\n--- Viewing Settings ---")
print(view_settings(test_settings))

# 4. Update a setting
print("\n--- Updating a Setting ---")
print(update_setting({'theme': 'light'}, ('theme', 'dark')))
print(update_setting({'theme': 'light'}, ('volume', 'high')))

# 5. Delete a setting
print("\n--- Deleting a Setting ---")
print(delete_setting({'theme': 'light'}, 'theme'))

# 6. Final verification
print("\n--- Final Settings View ---")
print(view_settings(test_settings))
