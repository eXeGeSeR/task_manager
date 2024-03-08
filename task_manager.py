# Notes:
# 1. Use the following username and password to access the admin rights
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3].strip(), DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4].strip(), DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)

#====Login Section====
'''This code reads usernames and password from the user.txt file to
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:
    print("LOGIN")
    curr_user = input("Username: ").strip()
    curr_pass = input("Password: ").strip()
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

def reg_user():
    ''' Register a new user '''
    new_username = input("New Username: ")
    if new_username in username_password.keys():
        print("Username already exists. Please use another username.")
        return
    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")
    if new_password == confirm_password:
        with open("user.txt", "a") as user_file:
            user_file.write(f"\n{new_username};{new_password}")
        print("New user added successfully.")
    else:
        print("Passwords do not match.")

def add_task():
    '''Allow a user to add a new task to task.txt file
    Prompt a user for the following:
    - A username of the person whom the task is assigned to,
    - A title of a task,
    - A description of the task and
    - the due date of the task.'''
    # A repeated input for an existing username
    while True:
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
        else:
            break
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Then get the current date.
    curr_date = date.today()

    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append("; ".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")

def view_all():
    '''Reads the task from task.txt file and prints to the console in the
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling)
        '''
    
    for t in task_list:
        print('-' * 80 + "\n")
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Complete: \t {t['completed']}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)
        print('-' * 80 + "\n")

def view_mine():
    '''Reads the tasks assigned to the current user from task.txt file and allows user interaction'''
    user_tasks = [task for task in task_list if task['username'] == curr_user]

    # Changed to iterate over the user_tasks variable created above instead of iterating over task_list
    for i, task in enumerate(user_tasks):
        if task['username'] == curr_user:
            print('-' * 80 + "\n")
            disp_str = f"Task {i + 1}: \t {task['title']}\n"
            disp_str += f"Assigned to: \t {task['username']}\n"
            disp_str += f"Date Assigned: \t {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Completed: Yes" if task['completed'] else "Completed: No \n"
            print(disp_str)
            print('-' * 80 + "\n")


    if not user_tasks:
        print("No tasks are being assigned to you")
        return

    while True:
        user_choice = input("Enter the number of the task (-1 to return to main menu): ")

        try:
            task_index = int(user_choice) - 1
            selected_t = user_tasks[task_index]

        except (ValueError, IndexError):
            print("Invalid input. Please enter a valid task number.")
            continue


        action = input('''Choose what to do with the selected task:\n
        1. Mark as complete\n
        2. Edit your task\n
        Choose one of the options (or -1 to return to main menu): ''')

        if action == '-1':
            return

        elif action == '1':
            if selected_t['completed'] == False:
                selected_t['completed'] = True
                print("\nThe task is completed")
                # Removed the break statement since the writing to the file is done inside the loop
            else:
                print("\nThe task is already marked as complete.")

        elif action == '2':
            if not selected_t['completed']:
                new_username = input("Enter a new username or leave it blank to keep the current username: ")
                new_due_date = input("Enter new date (YYYY-MM-DD) or leave it blank to keep the current due date: ")

                if new_username:
                    selected_t['username'] = new_username
                if new_due_date:
                    try:
                        selected_t['due_date'] = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                    except ValueError:
                        print("Invalid format date. The task was not updated.")
                        continue
                print("The task was updated successfully.")

            else:
                print("Task cannot be edited because it is already marked as complete")
        else:
            print("Invalid choice. Please enter a valid option.")

        with open("tasks.txt", "w") as task_file:
            task_list_to_write = []
            for task in task_list:
                str_attrs = [
                    task['username'],
                    task['title'],
                    task['description'],
                    task['due_date'].strftime(DATETIME_STRING_FORMAT),
                    task['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if task['completed'] else "No"
                ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))
        break


def generate_reports():
    ''' Generate reports to the task_overview.txt and user_overview.txt '''
    # The total number of tasks that have been generated and tracked using the task_manager.py
    total_tasks = len(task_list)

    # The total number of completed tasks
    total_completed_tasks = len([t for t in task_list if t['completed'] == "Yes"])

    # The total number of uncompleted tasks
    total_uncompleted_tasks = len([t for t in task_list if t['completed'] != "Yes"])

    # The total number of tasks that haven't been completed and that are overdue
    total_overdued = len([ t for t in task_list if t['due_date'] == False])
    total_uncompleted_overdued = total_uncompleted_tasks + total_overdued

    # The percentage of tasks that are incomplete
    if total_uncompleted_tasks == 0:
        uncompleted_tasks_percentage = 100
    else:
        uncompleted_tasks_percentage = int((total_uncompleted_tasks * 100)/ total_uncompleted_tasks)

    # The percentage of tasks that are overdued
    if total_overdued == 0:
        overdued_tasks_percentage = 100
    else:
        overdued_tasks_percentage = (total_overdued * 100) / total_overdued

    with open("task_overview.txt", "w") as file_task_overview:
        file_task_overview.write("Task Overview\n\n"
            f"The total number of tasks is: {total_tasks}.\n"
            f"The total number of completed tasks is: {total_completed_tasks}.\n"
            f"The total number of uncompleted tasks is: {total_uncompleted_tasks}.\n"
            f"The total number of uncompleted and overdued tasks is: {total_uncompleted_overdued}.\n"
            f"The percentage of uncompleted tasks is: {uncompleted_tasks_percentage}%.\n"
            f"The percentage of overdued tasks is: {overdued_tasks_percentage}%.\n")

    # Total number of users registered
    total_users = len(username_password)

    # Total number of tasks generated and tracked
    total_tasks = len(task_list)

    # Dictionary to store user-specific information
    user_info = {}

    # Calculate user-specific information
    for user in username_password:
        # Initialize user-specific information
        user_info[user] = {
            'total_tasks_assigned': 0,
            'percentage_of_total_tasks_assigned': 0,
            'percentage_of_tasks_completed': 0,
            'percentage_of_tasks_remaining': 0,
            'percentage_of_overdue_tasks': 0
        }

        # Count total tasks assigned to the user
        user_info[user]['total_tasks_assigned'] = sum(1 for task in task_list if task['username'] == user)

        # Calculate percentage of total tasks assigned to the user
        if total_tasks > 0:
            user_info[user]['percentage_of_total_tasks_assigned'] = (user_info[user]['total_tasks_assigned'] / total_tasks) * 100

        # Count total completed tasks for the user
        total_completed_tasks = sum(1 for task in task_list if task['username'] == user and task['completed'])

        # Calculate percentage of completed tasks
        if user_info[user]['total_tasks_assigned'] > 0:
            user_info[user]['percentage_of_tasks_completed'] = (total_completed_tasks / user_info[user]['total_tasks_assigned']) * 100

        # Calculate percentage of tasks remaining
        user_info[user]['percentage_of_tasks_remaining'] = 100 - user_info[user]['percentage_of_tasks_completed']

        # Count total overdue tasks for the user
        total_overdue_tasks = sum(1 for task in task_list if task['username'] == user and not task['completed'] and task['due_date'] < datetime.now())

        # Calculate percentage of overdue tasks
        if user_info[user]['total_tasks_assigned'] > 0:
            user_info[user]['percentage_of_overdue_tasks'] = (total_overdue_tasks / user_info[user]['total_tasks_assigned']) * 100

    # Write information to user_overview.txt
    with open("user_overview.txt", "w") as file_user_overview:
        file_user_overview.write("User Overview\n\n")
        file_user_overview.write(f"Total number of users registered: {total_users}\n")
        file_user_overview.write(f"Total number of tasks generated and tracked: {total_tasks}\n\n")

        for user, info in user_info.items():
            file_user_overview.write(f"User: {user}\n")
            file_user_overview.write(f"Total number of tasks assigned: {info['total_tasks_assigned']}\n")
            file_user_overview.write(f"Percentage of total tasks assigned: {info['percentage_of_total_tasks_assigned']:.2f}%\n")
            file_user_overview.write(f"Percentage of tasks completed: {info['percentage_of_tasks_completed']:.2f}%\n")
            file_user_overview.write(f"Percentage of tasks remaining: {info['percentage_of_tasks_remaining']:.2f}%\n")
            file_user_overview.write(f"Percentage of overdue tasks: {info['percentage_of_overdue_tasks']:.2f}%\n\n")

def display_statistics():
    '''If the user is an admin they can display statistics about number of users
            and tasks.'''

    if curr_user == "admin":
        print('-' * 80 + "\n")
        with open("user_overview.txt", "r") as file_user_overview:
            file_user_overview.seek(0)
            print(file_user_overview.read())
        print('-' * 80 + "\n")

        print('-' * 80 + "\n")
        with open("task_overview.txt", "r") as file_task_overview:
            file_task_overview.seek(0)
            print(file_task_overview.read())
        print('-' * 80 + "\n")
    else:
        pass

def main():
    while True:
        # presenting the menu to the user and
        # making sure that the user input is converted to lower case.
        print()
        MENU = input('''Select one of the following options:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports
ds - Display statistics
e - Exit
>> ''').lower()

        if MENU == 'r':
            if curr_user == "admin":
                reg_user()
            else:
                print("Only admin has been authorized to register users!")

        elif MENU == 'a':
            add_task()

        elif MENU == 'va':
            view_all()

        elif MENU == 'vm':
            view_mine()

        elif MENU == 'gr':
            generate_reports()
            print("You are generating user and task reports...")

        elif MENU == 'ds':
            if curr_user == 'admin':
                display_statistics()
            else:
                print("Only admin is authorized to display statistics!")

        elif MENU == 'e':
            print('Goodbye!!!')
            exit()

        else:
            print("You have made a wrong choice, Please Try again")

if __name__ == "__main__":
    main()