import os
def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        current_directory = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(current_directory, 'entries\\', title)
        with open(full_path, 'rb') as f:
            content = f.read()
            return content.decode("utf-8")
    except FileNotFoundError:
        return None