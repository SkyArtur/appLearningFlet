from flet import Page
from components import custom_snack_bar
from database import dbSQLite


def save_profile(page: Page, *args: str):
    """
    Saves the user profile information in the database. Inserts the first name, last name, and birth date
    into the profiles table and returns the ID of the newly created profile.
    :param page: A Page object from the Flet library.
    :param args: A variable number of strings representing the first name, last name, and birth date.
    :return: The ID of the newly created profile if the operation is successful, otherwise raises an Exception.
    """
    try:
        # Insert the profile information into the database
        query = 'insert into profiles (first_name, last_name, birth) values (?, ?, ?) returning id;'
        new = dbSQLite.save(query, args)
        return new[0] # Return the ID of the newly created profile
    except (ValueError, IndexError, Exception) as error:
        custom_snack_bar(save_profile, f'{error}.', page)


def save_user(page: Page, first_name: str, last_name: str, birth: str, *args: str):
    """
    Saves a new user in the database. Creates a profile with the provided first name, last name, and birth date,
    then inserts the user information along with the profile ID into the users table.

    :param page: A Page object from the Flet library.
    :param first_name: A string representing the user's first name.
    :param last_name: A string representing the user's last name.
    :param birth: A string representing the user's birth date.
    :param args: A variable number of strings representing the username, email, and password.
    :return: None
    """
    try:
        # Save the user profile and get the new profile ID
        new = [save_profile(page, first_name, last_name, birth)]
        # Prepare the query to insert the user data into the database
        query = 'insert into users (id_profile, username, email, password) values (?, ?, ?, ?);'
        new += [i for i in args]
        # Execute the database insert operation
        dbSQLite.save(query, tuple(new))
    except (ValueError, IndexError, Exception) as error:
        custom_snack_bar(save_user, f'{error}.', page)