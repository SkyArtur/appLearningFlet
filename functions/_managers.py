from flet import Page, TextField, DataRow, DataCell, Text, DataTable
from passlib.hash import pbkdf2_sha256 as pbkdf2
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


def check_login_data(page: Page, username: TextField, password: TextField):
    """
    Validates the login credentials by checking the username (or email) and password against the stored data
    in the database. Returns True if the credentials are valid.
    :param page: A Page object from the Flet library.
    :param username: A TextField object representing the username or email input.
    :param password: A TextField object representing the password input.
    :return: True if the credentials are valid, otherwise raises a ValueError.
    """
    try:
        # Query to retrieve the stored password based on the username or email
        query = 'select password from users where username = ? or email = ?;'
        _password = dbSQLite.fetchone(query, (username.value, username.value))
        # Check if the user exists and if the password is valid
        if not _password:
            raise ValueError('User not found')
        elif not pbkdf2.verify(password.value, _password[0]):
            raise ValueError('Invalid password')
        else:
            return True
    except (ValueError, IndexError, Exception) as error:
        custom_snack_bar(save_user, f'{error}.', page)


def get_data_table_profiles(page: Page, table: DataTable, *args: str) -> None:
    """
    Retrieves all profiles that are not associated with any users from the database. Populates the provided DataTable
    with profile information (ID, first name, last name, birth date).

    :param page: A Page object from the Flet library.
    :param table: A DataTable object to be populated with profile data.
    :param args: Optional arguments (unused in this function).
    :return: None
    """
    try:
        # SQL query to select profiles not linked to any users
        query = '''
            select p.id, p.first_name, p.last_name, p.birth from profiles p
            left join users u on p.id = u.id_profile
            where u.id_profile is null;
        '''
        # Fetch profile data and convert to a list of dictionaries
        profiles = [dict(id=i[0], first_name=i[1], last_name=i[2], birth_date=i[3]) for i in dbSQLite.fetchall(query)]
        # Clear existing rows in the DataTable and populate it with the retrieved profiles
        table.rows.clear()
        for profile in profiles:
            table.rows.append(
                DataRow(
                    cells=[
                        DataCell(Text(str(profile['id']))),
                        DataCell(Text(str(profile['first_name']))),
                        DataCell(Text(str(profile['last_name']))),
                        DataCell(Text(str(profile['birth_date']))),
                    ]
                )
            )
    except (ValueError, IndexError, Exception) as error:
        custom_snack_bar(get_data_table_profiles, f'{error}.', page)