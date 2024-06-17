import sqlite3


try:
    con = sqlite3.connect('ToDoApp.db', timeout=15)
    crs = con.cursor()
    print('Connected to database.')

except:
    print('Error! Could not connect to database.')

finally:
    if con:

        crs.execute("""CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_name VARCHAR(15) NOT NULL,
                    description TEXT NOT NULL,
                    due_date DATE NOT NULL,
                    user_name INTEGER,
                    FOREIGN KEY (user_name) REFERENCES users (user_name))""")

        crs.execute("""CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_name VARCHAR(15) NOT NULL,
                    phone TEXT)""")


        def addTask():
            while True:
                option = input("If you don't have a user ID enter 'u' and if you have enter 't': ")
                if option == 'b':
                    break

                if option == 'u':
                    addUser()
                    continue

                if option == 't':
                    uName = input('Enter your username: ')
                    if uName == 'b':
                        break

                    crs.execute("SELECT user_name FROM users WHERE user_name = ?", (uName,))
                    if crs.fetchone() is not None:
                        tName = input('Enter the task name: ')
                        desc = input('Enter task description: ')
                        date = input('Enter due date (DD-MM-YYYY): ')

                        crs.execute("SELECT user_name FROM users WHERE user_name = ?", (uName,))
                        userName = crs.fetchone()[0]

                        crs.execute("INSERT INTO tasks (task_name, description, due_date, user_name) VALUES (?, ?, ?, ?)", (tName, desc, date, userName))
                        con.commit()

                        print(f'Your task named "{tName}" for user "{uName}" has been added.')
                    else:
                        print('Error! This username does not exist. Please create a new one or enter the correct username.')
                else:
                    print("Error! Enter 'u' to add user or 't' to add task")


        def deleteTask():
            while True:
                option = input("If you want to delete all tasks enter 'a', If you want to delete a specific task enter task id: ").strip().lower()
                if option == 'b':
                    break

                if option == 'a':
                    crs.execute("DELETE FROM tasks")
                    con.commit()

                    print(f'The tasks are deleted. There is no tasks right now.')
                else:
                    crs.execute(f"SELECT * FROM tasks WHERE id = '{option}'")
                    task = crs.fetchone()
                    if task is None:
                        print("Error! Please enter a valid id task or exist id task.")
                        continue
                    else:
                        crs.execute(f"DELETE FROM tasks WHERE id='{option}'")
                        con.commit()

                        print(f'The task is deleted.')


        def showTasks():
            while True:
                option = input("If you want all tasks enter 'a', if you want user tasks enter 'u': ").strip().lower()
                if option == 'b':
                    break

                if option == 'a':
                    crs.execute('SELECT * FROM tasks')
                    result1 = crs.fetchall()

                    print(f'\nYou have {len(result1)} tasks')
                    print('=' * 17)
                    for task in result1:
                        print(f'Task name: {task[1]}, Task description: {task[2]}, Due Date: {task[3]}, Username: {task[4]}')

                elif option == 'u':
                    userName = input('Enter username: ').strip().lower()
                    if userName == 'b':
                        break

                    crs.execute("SELECT * FROM tasks WHERE user_name = (?)", (userName,))
                    result2 = crs.fetchall()

                    if len(result2) > 0:
                        print(f'\nYou have {len(result2)} tasks for user: {userName}')
                        print('=' * 35)
                        for task in result2:
                            print(
                                f'Task name: {task[1]}, Task description: {task[2]}, Due Date: {task[3]}')
                    else:
                        print('Error! No tasks found for the entered username or the username does not exist.')
                else:
                    print("Error! Please enter 'a' or 'u'.")


        def updateTask():
            while True:
                taskId = input('Enter a task ID to update: ')
                if taskId == 'b':
                    break

                crs.execute("SELECT * FROM tasks WHERE id = ?", (taskId,))
                result = crs.fetchone()

                if result:
                    newDesc = input('Enter new description: ')
                    newDate = input('Enter new due date (DD-MM-YYYY): ')

                    crs.execute("UPDATE tasks SET description = ? WHERE id = ?", (newDesc, taskId))
                    crs.execute("UPDATE tasks SET due_date = ? WHERE id = ?", (newDate, taskId))
                    con.commit()

                    print(f"The task with ID {taskId} has been updated.")
                else:
                    print('Error! Enter a valid or existing task ID.')


        def addUser():
            while True:
                name = input('Enter username: ').lower().strip()
                if name == 'b':
                    break

                crs.execute("SELECT user_name FROM users WHERE user_name = ?", (name,))
                if crs.fetchone() is None:
                    phone = input('Enter your phone: ')

                    crs.execute("INSERT INTO users (user_name, phone) VALUES (?, ?)", (name, phone))
                    con.commit()

                    print(f'{name} is added to users.')

                    crs.execute("SELECT * FROM users WHERE user_name = ?", (name,))
                    result2 = crs.fetchone()
                    print(f"ID: {result2[0]},  USERNAME: {result2[1]}")
                else:
                    print('The username is used before. Please create a new one.')


        def deleteUser():
            while True:
                option = input("If you want to delete user enter ID, If you want to delete all user enter 'a': ")
                if option == 'b':
                    break

                if option == 'a':
                    crs.execute("DELETE FROM users")
                    con.commit()

                    print(f'The users are deleted. There is no users right now.')
                else:
                    crs.execute(f"SELECT * FROM users WHERE id = '{option}'")
                    user = crs.fetchone()
                    if user is None:
                        print("Error! Please enter a valid user ID or exist user ID.")
                        continue
                    else:
                        crs.execute(f"DELETE FROM users WHERE id='{option}'")
                        con.commit()

                        print(f'The user is deleted.')


        def showUsers():
            crs.execute(f'SELECT * FROM users')
            result = crs.fetchall()

            print(f'\n{len(result)} users in system')
            print('=' * 17)
            if len(result) > 0:
                for i in result:
                    print(f'User ID: {i[0]}, Username: {i[1]}, Phone: {i[2]}')


        def main():
            msg = """
            'au' -> Add user
            'du' -> Delete user
            'su' -> Show users
            'at' -> Add task
            'dt' -> Delete task
            'st' -> Show tasks
            'ut' -> Update task
            'b' -> Back by one step in any mode
            'q' -> Quit the app
            """
            print(msg)

            while True:
                user_input = input('Choose an operation: ').strip().lower()

                if user_input == 'at':
                    addTask()
                elif user_input == 'dt':
                    deleteTask()
                elif user_input == 'st':
                    showTasks()
                elif user_input == 'ut':
                    updateTask()
                elif user_input == 'au':
                    addUser()
                elif user_input == 'du':
                    deleteUser()
                elif user_input == 'su':
                    showUsers()
                elif user_input == 'q' or user_input == 'b':
                    con.close()
                    print('\nExiting...')
                    print('Thanks for using my software. | Powered By Omar Mohamed Sharawi.')
                    exit()
                else:
                    print('Error! enter a valid operation.')



if __name__ == '__main__':
    main()
