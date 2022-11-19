from pprint import pprint

import sqlalchemy.sql.functions
from db_connection import Session, engine
from orm_base import metadata
import logging

from Building import Building
from Room import Room
from Door import Door
from HookDoor import HookDoor
from Hook import Hook
from Key import Key
from Loan import Loan
from Request import Request
from ReturnKey import ReturnKey
from Employee import Employee

if __name__ == '__main__':
    logging.basicConfig()
    # use the logging factory to create our first logger.
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
    # use the logging factory to create our second logger.
    logging.getLogger("sqlalchemy.pool").setLevel(logging.DEBUG)

    with Session() as sess:
        sess.begin()
        while 1:
            print('Menu: choose one')
            print('a. Create a new Key.\n'
                  'b. Request access to a given room by a given employee.\n'
                  'c. Capture the issue of a key to an employee\n'
                  'd. Capture losing a key\n'
                  'e. Report out all the rooms that an employee can enter, given the keys that he/she already has.\n'
                  'f. Delete a key.\n'
                  'g. Delete an employee.\n'
                  'h. Add a new door that can be opened by an existing hook.\n'
                  'i. Update an access request to move it to a new employee.\n'
                  'j. Report out all the employees who can get into a room.')

            choose = input()
            if choose == 'a':
                hook_number = input('Which hook do you want to create key: ')
                hooks = sess.query(Hook).all()
                print(hooks)
                found_hook = {}
                for hook in hooks:
                    if hook_number == hook.number:
                        found_hook = hook
                        break
                if not found_hook:
                    print('Cannot find hook')
                    continue
                key_number = int(input('Enter key number: '))
                new_key = Key(number=key_number, hook=found_hook)
                sess.add(new_key)
                sess.commit()
            elif choose == 'b':
                employee_name = input('Enter employee name: ')
                building_name, room_number = input('Enter building and room: ').split()
                


    # metadata.drop_all(bind=engine)  # start with a clean slate while in development
    #
    # metadata.create_all(bind=engine)

    # sec1: Section = Section(section_id="123", department_name="CECS", course_name="323", section_number=1,
    #                         semester="Fall", year=2022)
    #
    # student1: Student = Student(student_id="1111", last_name="Nguyen", first_name="Nhat")
    # student2: Student = Student(student_id="2222", last_name="Tran", first_name="Quy")
    # student3: Student = Student(student_id="3333", last_name="Truong", first_name="Toan")
    #
    # with Session() as sess:
    #     sess.begin()
    #     print("Inside the session, woo hoo.")
    #     sess.add(sec1)
    #     sess.add(student1)
    #     sess.add(student2)
    #     sess.add(student3)
    #     sess.commit()
    #
    #     sec1.add_student(student1, '3.5')
    #     sec1.add_student(student2, '3.5')
    #     sec1.add_student(student3, '3.5')
    #     sess.commit()
    #
    #     students = sess.query(Student).all()
    #     print("Student: ")
    #     for student in students:
    #         pprint(student.__dict__)
    #     enrollments = sess.query(Enrollment).all()
    #     print("Enrollment: ")
    #     for e in enrollments:
    #         pprint(e.__dict__)
    #     sections = sess.query(Section).all()
    #     print("Section: ")
    #     for e in sections:
    #         pprint(e.__dict__)
    #
    # print("Exiting normally.")
