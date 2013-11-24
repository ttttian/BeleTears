import pickle
import re
import getpass
from ucb import main
from student import *
from course import *
from error import *

def log_in(students):
    name = input('Student Name: ')
    password = getpass.getpass('Password: ')
    student = get_student(name, students)
    if student.check_password(password):
        print('Login Successful!')
        return student

def check_args(cmd, args, n):
    if len(args) < n:
        raise BTError('illegal argument for {0}'.format(cmd))

def read_eval_print_loop(student, students, courses):
    def help():
        print(HELP)

    def bid(student, args, courses):
        check_args('bid', args, 2)
        course_name = ' '.join(args[:-1])
        price = eval(args[-1])
        course = get_course(course_name, courses)
        print(student.bid(course, price))

    def drop(student, args, courses):
        check_args('drop', args, 1)
        course_name = ' '.join(args)
        course = get_course(course_name, courses)
        print(student.drop(course))

    def info(student, courses):
        bids_info = student.bids_info(courses)
        print('Name: {0}\nBalance: {1}\nBids: {2}' \
            .format(student.name, student.balance, bids_info))

    def lst(courses):
        for course_name, course in sorted(courses.items(), key=lambda x: x[0]):
            print(course.info())

    def search(args, courses):
        check_args('search', args, 1)
        total_result = {}
        for arg in args:
            result = {}
            for course_name, course in courses.items():
                if arg.lower() in course_name:
                    result[course_name] = course
            if result == {}:
                total_result = {}
                break
            else:
                if total_result == {}:
                    total_result = result.copy()
                else:
                    total_result = {course_name: course for course_name, course \
                        in total_result.items() if course_name in result}
        if total_result == {}:
            print('No course matches the keywords.')
        else:
            lst(total_result)

    HELP = """Commands:
    bid [course] [price]    Bid PRICE on course.
    drop [course]           Drop COURSE, return your bid to your balance.
    info                    Display your current bids(including whether
                            safe to be selected) and balance.
    list                    List all courses.
    search [keywords...]    List courses that matches the KEYWORDS.
    help                    Display help message.
    logout                  Log out the current user account.
    exit/quit/<Control>-D   Exit this system."""

    help()
    while True:
        save(students, courses)
        string = input('> ')
        if string == '':
            continue
        cmds = string.split()
        cmd = cmds[0]
        if cmd == 'bid':
            bid(student, cmds[1:], courses)
        elif cmd == 'drop':
            drop(student, cmds[1:], courses)
        elif cmd == 'help':
            help()
        elif cmd == 'info':
            info(student, courses)
        elif cmd == 'list':
            lst(courses)
        elif cmd == 'search':
            search(cmds[1:], courses)
        elif cmd == 'logout':
            return True
        elif cmd == 'exit' or cmd == 'quit':
            return False
        else:
            raise BTError('illegal command {0}'.format(cmd))

def save(students, courses):
    f = open('data.pickle', 'wb')
    pickle.dump(students, f)
    pickle.dump(courses, f)
    f.close()

def load():
    f = open('data.pickle', 'rb')
    students = pickle.load(f)
    courses = pickle.load(f)
    f.close()
    return students, courses

@main
def run():
    students, courses = load()
    student = None
    while True:
        try:
            if student is None:
                student = log_in(students)
            if read_eval_print_loop(student, students, courses):
                student = None
            else:
                break
        except (BTError, SyntaxError, ValueError, RuntimeError) as e:
            print('Error:', e)
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")
        except EOFError:
            print()
            break
    save(students, courses)
    print('Byebye~')
