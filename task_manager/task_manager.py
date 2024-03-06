# T17 Capstone Project - Lists, Functions,  and String Handling
# Task 1

"""
This is a program designed for a small business to help it manage tasks
 assigned to each member of a team.

The user interface allows for;
    - Controlling access through usernames and password
    - Adding new members
    - Adding new tasks
    - Updating existing tasks
    - Generating and displaying statistic reports 

Example usage:
import task_manager as tm
tm.launch_task_manager()

"""

# ====importing libraries====
import os
from datetime import datetime, date

# Define constant
DATE_STRING_FORMAT = "%Y-%m-%d"


# ====Get Task Section====
def get_task_data() -> list[str]:
    """
    Create list of tasks from tasks.txt file.

    - Create blank tasks.txt file if doesn't exist.
    - Read the tasks.txt file.
    - Creates a list of tasks in tasks.txt file, each line in the file
      is an element in the list.
    - Blank lines are removed from the list.

    Returns
    -------
    list[str]
        Contains data of each users tasks.
    """
    # Create tasks.txt if it doesn't exist
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w"):
            pass

    with open("tasks.txt", "r") as task_file:
        task_data = task_file.read().split("\n")

    # Gets rid of the blank line in the task
    task_data = [t for t in task_data if t != ""]
    return task_data


def get_task_list(task_data: list[str]) -> list[dict]:
    """
    Create a list of dictionaries for tasks.

    Each element in the list will be a dictionary containing all the
    information for a task.

    Parameters
    ----------
    task_data : list[str]
        A list of strings representing tasks.
        Fields within the task are separated by semicolons.

    Returns
    -------
    list[dict]
        A list of dictionaries representing tasks.
    """
    task_list = []
    for t_str in task_data:
        curr_t = {}

        # Split by semicolon and manually add each component
        task_components = t_str.split(";")
        curr_t["username"] = task_components[0]
        curr_t["title"] = task_components[1]
        curr_t["description"] = task_components[2]
        curr_t["due_date"] = datetime.strptime(
            task_components[3], DATE_STRING_FORMAT
        )
        curr_t["assigned_date"] = datetime.strptime(
            task_components[4], DATE_STRING_FORMAT
        )
        curr_t["completed"] = True if task_components[5] == "Yes" else False

        task_list.append(curr_t)
    return task_list


# ====Get User Section====
def get_user_data() -> list[str]:
    """
    Reads usernames and password from the user.txt file.

     - If user.txt file doesn't exist, a default admin account is written to
       the file: "admin;password".
     - The function then reads the contents of the file, and splits them into
       user data, to return a list.

    Returns
    -------
    list[str]
        A list containing user data. Each element of the list is a string
        representing a user with the format: username;password.
    """
    # If no user.txt file, write one with a default account
    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as default_file:
            default_file.write("admin;password")

    # Read in user_data
    with open("user.txt", "r") as user_file:
        user_data = user_file.read().split("\n")
    return user_data


# Convert user_data to a dictionary
def get_username_password(user_data: list[str]) -> dict:
    """
    Create a dictionary of username-password pairs from a list of user data.

    Parameters
    ----------
    user_data : list[str]
        A list containing user data. Each element of the list is a string
        representing a user with the format: "username;password".

    Returns
    -------
    dict
        A dictionary where the keys are usernames and the values are passwords.
    """
    username_password = {}
    for user in user_data:
        username, password = user.split(";")
        # Set key to username, set value to password
        username_password[username] = password
    return username_password


# ====Login Section====
# User input function: username/password
def get_user_login(username_password: dict) -> str:
    """
    Prompt the user for login details and validate against existing data
    in file.

    Parameters
    ----------
    username_password : dict
        A dictionary where the keys are usernames and the values are passwords.

    Returns
    -------
    str
        A str containing the username of each successfully logged-in user.
    """
    # Loop until successful
    while True:
        # Get user username and password
        print("LOGIN")
        curr_user = input("Username: ")
        curr_pass = input("Password: ")
        # Check user exists
        if curr_user not in username_password.keys():
            print("\nUser does not exist")
            continue
        # Check password if correct
        elif username_password[curr_user] != curr_pass:
            print("\nWrong password")
            continue
        else:
            # Success - return username
            print("\nLogin Successful!")
            return curr_user


# ====Main Menu Functions Section====
# Function that is called when the user selects ‘r’ to register a user.
def reg_user(username_password: dict):
    """
    Register a new user by adding their login details to the existing
    user data.

    Parameters
    ----------
    username_password : dict
        A dictionary where the keys are usernames and the values are passwords.
    """
    new_username = input("New Username: ")

    # Check if the username already exists
    if new_username in username_password:
        print("\nUsername already exists. Please choose a different username.")
        return

    # Get password
    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")

    # Confirm match
    if new_password == confirm_password:
        print("\nNew user added")
        username_password[new_username] = new_password

        # Format output string
        user_data = []
        for key in username_password:
            user_data.append(f"{key};{username_password[key]}")

        # Write out to user file
        # The code is opening a file named "user.txt" in write mode
        # and then writing the contents of the `user_data` list to the file,
        # with each element of the list on a new line.
        with open("user.txt", "w") as out_file:
            out_file.write("\n".join(user_data))
    else:
        print("Passwords do not match")


# Function for taking dict turning to list and writing to file
def write_task_list(task_list: list[dict]):
    """
    Write a list of tasks to 'tasks.txt'.

    Parameters
    ----------
    task_list : list[dict]
        List of dictionaries representing tasks with keys:
        - username (str)
        - title (str)
        - description (str)
        - due_date (datetime)
        - assigned_date (datetime)
        - completed (bool)
    """
    # Get tasks into list
    task_list_to_write = []
    for t in task_list:
        str_attrs = [
            t["username"],
            t["title"],
            t["description"],
            t["due_date"].strftime(DATE_STRING_FORMAT),
            t["assigned_date"].strftime(DATE_STRING_FORMAT),
            "Yes" if t["completed"] else "No",
        ]
        task_list_to_write.append(";".join(str_attrs))

    # Open file
    with open("tasks.txt", "w") as task_file:
        # Write out tasks
        task_file.write("\n".join(task_list_to_write))


# Function that is called when a user selects ‘a’ to add a new task.
def add_task(task_list: list[str], username_password: dict):
    """
    Allow a user to add a new task to task.txt file.

    Prompt a user for the following:
        - A username of the person whom the task is assigned to.
        - A title of a task.
        - A description of the task
        - The due date of the task in set format: YYYY-MM-DD

    Parameters
    ----------
    task_list : list[str]
        List of dictionaries representing tasks with keys:
        - username (str)
        - title (str)
        - description (str)
        - due_date (datetime)
        - assigned_date (datetime)
        - completed (bool)
    username_password : dict
        A dictionary where the keys are usernames and the values are passwords.
    """
    # Get user inputs
    task_username = input("\nName of person assigned to task: ")
    if task_username not in username_password.keys():
        print("\nUser does not exist. Please enter a valid username")
        return
    task_title = input("\nTitle of Task: ")
    task_description = input("\nDescription of Task: ")
    due_date_time = user_input_date("\nDue date of task (YYYY-MM-DD): ")

    # Then get the current date.
    curr_date = date.today()

    # Add the data to the file task.txt
    # Include completed: False
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False,
    }
    task_list.append(new_task)
    write_task_list(task_list=task_list)
    print("\nTask successfully added.")


# user input function: date
def user_input_date(
    msg: str = "\nPlease enter a date (YYYY-MM-DD): ",
) -> datetime:
    """
    Prompt user for a date in the specified format.

    Re-prompt if date is entered in an invalid format.

    Parameters
    ----------
    msg : str, optional
        Prompt message, by default "Please enter a date:"

    Returns
    -------
    datetime
        A datetime object representing the entered date.
    """
    while True:
        try:
            # Get input
            user_date = input(msg)
            # Cast to date
            user_date = datetime.strptime(user_date, DATE_STRING_FORMAT)
            return user_date
        # On error loop
        except ValueError:
            print("\nInvalid date format. Please use the format specified.")


# user input function: int
def user_input_int(msg: str = "\nPlease enter an int:") -> int:
    """
    Prompt user for an integer input.

    Re-prompt if the input is not a valid integer.

    Parameters
    ----------
    msg : str, optional
        Prompt message, by default "Please enter an integer:"

    Returns
    -------
    int
    """
    while True:
        try:
            # Get input
            user_int = input(msg)
            # Cast to int
            user_int = int(user_int)
            return user_int
        # On error loop
        except ValueError:
            print("\nInvalid input, please input an integer.")


# User input function: y/n
def user_input_yes_no(msg: str = "\nPlease enter y/n: ") -> str:
    """
    Prompt user for a y/n input.

    Re-prompt if value is not 'y' or 'n'.

    Parameters
    ----------
    msg : str, optional
        Prompt message, by default "Please enter y/n: "

    Returns
    -------
    str
        The entered response, 'y' for yes or 'n' for no.
    """
    while True:
        # Get input
        user_yn = input(msg).lower()
        # Check y/n else loop
        if user_yn in ["y", "n"]:
            return user_yn
        else:
            print("\nInvalid input, please enter 'y' or 'n'.")


# Allow the user to select either a speciﬁc task (by entering a number) or
# input ‘-1’ to return to the main menu
def user_task_num_select(task_list: list[dict], curr_user: str) -> int:
    """
    Prompt user for a task number.

    Task must belong to user.

    Parameters
    ----------
    task_list : list[dict]
        List of dictionaries representing tasks with keys:
        - username (str)
        - title (str)
        - description (str)
        - due_date (datetime)
        - assigned_date (datetime)
        - completed (bool)
    curr_user : str
        The username of the current user.

    Returns
    -------
    int
        The selected task number, or -1 to return to the menu.
    """
    while True:
        # Get an int from user
        user_int = user_input_int(
            msg=(
                "Select a task number to update,"
                " or input -1 to return to menu: "
            )
        )

        # If -1 then exit
        if user_int == -1:
            return -1
        # if less than 1 then not a valid list index number
        elif user_int < -1:
            print("\nThis is not a valid task number.")
            continue
        # if greater/equal-to the list len then nt valid index number
        elif user_int >= len(task_list):
            print("\nThis is not a valid task number.")
            continue

        # check this task is assigned to user
        selected_task = task_list[user_int]
        if selected_task["username"] == curr_user:
            return user_int

        # If not assigned to user, give error message and then loop
        print("\nThis task is not assigned to you.")


# Display task function used in va and vm
def display_task(task: dict, task_num: int):
    """
    Display the information for a task.

    Parameters
    ----------
    task : dict
        Dictionary representing a task.
    task_num : int
        Task number.
    """
    # Prep string
    display_str = (
        f"Task Number: \t {task_num}\n"
        f"Task: \t\t {task['title']}\n"
        f"Assigned to: \t {task['username']}\n"
        f"Date Assigned: \t {task['assigned_date'].strftime(DATE_STRING_FORMAT)}\n"
        f"Due Date: \t {task['due_date'].strftime(DATE_STRING_FORMAT)}\n"
        f"Complete: \t {'Yes' if task['completed'] else 'No'}\n"
        f"Task Description: \n\t{task['description']}\n"
    )
    # Print string
    print(display_str)


# Function that is called when users type ‘va’ to view all the tasks listed
# in ‘tasks.txt’.
def view_all(task_list: list[dict]):
    """
    Print formatted task list to the console.

    Parameters
    ----------
    task_list : list[dict]
        List of dictionaries representing tasks with keys:
        - username (str)
        - title (str)
        - description (str)
        - due_date (datetime)
        - assigned_date (datetime)
        - completed (bool)
    """
    for i, t in enumerate(task_list):
        display_task(task=t, task_num=i)


# Function that is called when users type ‘vm’ to view all the tasks that have
# been assigned to them. Allows for update of user tasks.
def view_mine(task_list: list[dict], curr_user: str, username_password: dict):
    """
    Print formatted task list to the console for tasks belonging to the user.

    Parameters
    ----------
    task_list : list[dict]
        List of dictionaries representing tasks with keys:
        - username (str)
        - title (str)
        - description (str)
        - due_date (datetime)
        - assigned_date (datetime)
        - completed (bool)
    curr_user : str
        The username of the current user.
    username_password : dict
        A dictionary containing username as key and password as values
    """

    # Check if user has any tasks
    found = False
    # List all of the task that belong to user
    for i, t in enumerate(task_list):
        if t["username"] == curr_user:
            display_task(task=t, task_num=i)
            found = True

    # If no tasks then exit
    if not found:
        print("\nYou have no tasks assigned to you.")
        return

    # Get user task number (if they want to edit)
    user_task_num = user_task_num_select(
        task_list=task_list, curr_user=curr_user
    )

    # Exit if user selected -1
    if user_task_num == -1:
        return

    # Get user task to update
    user_task = task_list[user_task_num]

    # If complete then cannot change, go to main menu
    if user_task["completed"]:
        print("\nThis task is complete and cannot be edited.")
        return

    # Check if want mark complete
    mark_task_complete = user_input_yes_no(
        msg="\nWould you like to mark the task as complete? (y/n): "
    )

    # If so update task, write out file and go to main menu
    if mark_task_complete == "y":
        user_task["completed"] = True
        write_task_list(task_list=task_list)
        print("\nTask successfully marked as complete.")
        return

    # Check if they want to edit the username
    update_username = user_input_yes_no(
        msg="\nWould you like update the username? (y/n): "
    )

    if update_username == "y":
        # Get new username
        new_username = input("\nProvide updated username: ")
        # Check username exists, else exit to main menu
        if new_username not in username_password:
            print("\nUsername not recognised. Exiting.")
            return

        # Update task with new username and write out to file
        user_task["username"] = new_username
        write_task_list(task_list=task_list)
        print("\nTask username successfully updated.")

    # Check if they want to edit the due date
    update_due_date = user_input_yes_no(
        msg="\nWould you like update the due date? (y/n): "
    )

    if update_due_date == "y":
        # Get new due date
        new_due_date = user_input_date(
            "\nProvide updated due date (YYYY-MM-DD): "
        )
        # Update task and write to file
        user_task["due_date"] = new_due_date
        write_task_list(task_list=task_list)
        print("\nTask due date successfully updated.")


# Function that is called when users type ‘gr’ or 'ds'
# Writes task_overview.txt and user_overview.txt reports
# Option to display the reports
def generate_reports(
    task_list: list[dict], username_password: dict, display: bool = False
):
    """
    Generate and optionally display the task and user overview statistics.

    Parameters
    ----------
    task_list : list[dict]
        List of dictionaries representing tasks with keys:
        - username (str)
        - title (str)
        - description (str)
        - due_date (datetime)
        - assigned_date (datetime)
        - completed (bool)
    username_password : dict
        A dictionary where the keys are usernames and the values are passwords.
    display : Bool, optional
        Whether to display the generated reports, by default False.
    """
    # Get date to check if overdue
    curr_date = date.today()

    # Get total tasks
    total_tasks = len(task_list)

    # Set up counters for total stats
    total_completed = 0
    total_overdue = 0

    # Create dict for user stats
    user_dict = {}
    for user in username_password.keys():
        user_dict[user] = {
            "task_count": 0,
            "completed": 0,
            "overdue": 0,
        }
    # Loop through tasks
    for t in task_list:

        # Increase user task count
        username = t["username"]
        user_dict[username]["task_count"] += 1

        # Check complete/overdue
        completed = t["completed"]
        overdue = t["due_date"].date() < curr_date

        # Increase counters if required (only overdue if not completed)
        if completed:
            total_completed += 1
            user_dict[username]["completed"] += 1
        elif overdue:
            total_overdue += 1
            user_dict[username]["overdue"] += 1

    # Accounting for zero division if user has no tasks
    if total_tasks == 0:
        pct_uncompleted = 0
        pct_overdue = 0
    else:
        pct_uncompleted = (total_tasks - total_completed) / total_tasks
        pct_overdue = total_overdue / total_tasks

    # Generate task overview stats
    task_overview = (
        f"Total Number of Tasks: \t\t\t\t{total_tasks}\n"
        f"Total Number of Completed Tasks: \t{total_completed}\n"
        f"Total Number of Uncompleted Tasks: \t{total_tasks - total_completed}\n"
        f"Total Number of Overdue Tasks: \t\t{total_overdue}\n"
        f"Percentage of Uncompleted Tasks \t{pct_uncompleted:.2%}\n"
        f"Percentage of Overdue Tasks \t\t{pct_overdue:.2%}"
    )

    # Generate base user overview stats
    user_overview = (
        f"Total Number of Users: \t{len(username_password)}\n"
        f"Total Number of Tasks: \t{total_tasks}"
    )
    # Loop to add user specific stats
    for user_name, stats in user_dict.items():
        user_task_count = stats["task_count"]
        user_completed = stats["completed"]
        user_overdue = stats["overdue"]

        # Handle division by 0 if no tasks
        if total_tasks == 0:
            pct_total_tasks = 0
        else:
            pct_total_tasks = user_task_count / total_tasks

        if user_task_count == 0:
            user_pct_completed = 0
            user_pct_uncompleted = 0
            user_pct_overdue = 0
        else:
            user_pct_completed = user_completed / user_task_count
            user_pct_uncompleted = 1 - user_pct_completed
            user_pct_overdue = user_overdue / user_task_count

        user_overview += (
            f"\n\nUsername: \t\t\t\t\t{user_name}\n"
            f"Number of User Tasks: \t\t{user_task_count}\n"
            f"Percentage of Total Tasks: \t{pct_total_tasks:.2%}\n"
            f"Percentage Completed: \t\t{user_pct_completed:.2%}\n"
            f"Percentage Uncompleted: \t{user_pct_uncompleted:.2%}\n"
            f"Percentage Overdue: \t\t{user_pct_overdue:.2%}"
        )

    # Write out files
    with open("task_overview.txt", "w") as task_overview_file:
        # Write out tasks
        task_overview_file.write(task_overview)

    with open("user_overview.txt", "w") as user_overview_file:
        # Write out tasks
        user_overview_file.write(user_overview)

    # Display if needed (note: adj tabs as look good in files but not in print)
    if display:
        print(
            "\nTASK OVERVIEW:\n--------------\n"
            f"{task_overview.replace('\t\t\t\t','\t\t\t')}\n\n"
            "USER OVERVIEW:\n--------------\n"
            f"{user_overview.replace('\t\t\t\t','\t\t')}\n"
        )


def set_menu_text(curr_user: str) -> str:
    """
    Set the user options for the menu.

    Admin has full menu options, while other users have a limited menu.

    Parameters
    ----------
    curr_user : str
        The username of the current user.
    Returns
    ----------
    menu_text : str
    """

    # If user is admin give the extra options (gr and ds)
    if curr_user == "admin":
        menu_text = """Please select one of the following options below:
        r - Registering a user
        a - Adding a task
        va - View all tasks
        vm - View my task
        gr - Generate reports
        ds - Display statistics
        e - Exit
        : """
    # Otherwise give reduced options
    else:
        menu_text = """Please select one of the following options below:
        r - Registering a user
        a - Adding a task
        va - View all tasks
        vm - View my task
        e - Exit
        : """

    return menu_text


# ====Main loop====
def launch_menu(
    curr_user: str, task_list: list[dict], username_password: dict
):
    """
    Present menu to the user allowing them to select an option.

    Loop until user choses to exit.
    Full list of potential user options:
        r - Registering a user
        a - Adding a task
        va - View all tasks
        vm - View my task
        gr - Generate reports
        ds - Display statistics
        e - Exit

    Parameters
    ----------
    curr_user : str
        The username of the current user.
    task_list : list[dict]
        List of dictionaries representing tasks with keys:
        - username (str)
        - title (str)
        - description (str)
        - due_date (datetime)
        - assigned_date (datetime)
        - completed (bool)
    username_password : dict
        A dictionary where the keys are usernames and the values are passwords.
    """
    # User terminal display
    while True:
        # Presenting the menu to the user and
        # making sure that the user input is converted to lower case.
        print()
        menu_text = set_menu_text(curr_user=curr_user)
        menu = input(menu_text).lower()

        if menu == "r":
            # Reg user
            reg_user(username_password=username_password)
        elif menu == "a":
            # Add new task
            add_task(task_list=task_list, username_password=username_password)
        elif menu == "va":
            # View all task
            view_all(task_list=task_list)
        elif menu == "vm":
            # View my tasks
            view_mine(
                task_list=task_list,
                curr_user=curr_user,
                username_password=username_password,
            )
        # Admin Only - Generate_reports(task_list, username_password)
        elif menu == "gr" and curr_user == "admin":
            # Generate reports
            generate_reports(
                task_list=task_list, username_password=username_password
            )
        # Admin Only - Display statistics
        elif menu == "ds" and curr_user == "admin":
            # Chose to regenerate reports rather than read from text files in
            # case they don't exist OR the tasks/users have been updated since
            generate_reports(
                task_list=task_list,
                username_password=username_password,
                display=True,
            )
        elif menu == "e":
            # Exit
            print("\nYou are exiting the program. Goodbye.")
            exit()
        else:
            # Invalid choice
            print("\nInvalid choice. Please Try again")


# ====Main code====
def launch_task_manager():
    """
    Launch task manager.

    Overview:
        - Load data from task.txt
        - Load data from user.txt
        - Get user login
        - Display task manager menu

    """

    # ----Get tasks----
    # Load task data from task.txt file
    task_data = get_task_data()
    # Split task data into a list of dictionaries represent each task
    task_list = get_task_list(task_data=task_data)

    # ----Get users----
    # Get_user_data from user.txt file
    user_data = get_user_data()
    # Get username_password dictionary
    username_password = get_username_password(user_data=user_data)

    # ----User login----
    curr_user = get_user_login(username_password=username_password)

    # ----Launch Menu----
    launch_menu(
        curr_user=curr_user,
        username_password=username_password,
        task_list=task_list,
    )


# Code only executes if the script is run as the main program.
# Stops code running straight away when imported as a module

if __name__ == "__main__":
    # Run the task manager
    launch_task_manager()
