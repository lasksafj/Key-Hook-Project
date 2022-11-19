from pprint import pprint

import sqlalchemy.sql.functions
from sqlalchemy import or_, and_, except_

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
    logging.getLogger("sqlalchemy.engine").setLevel(logging.ERROR)
    # use the logging factory to create our second logger.
    logging.getLogger("sqlalchemy.pool").setLevel(logging.ERROR)

    with Session() as sess:
        sess.begin()


        def room_employee_can_enter(employee_id):
            queries = sess.query(Employee, Request, ReturnKey) \
                .join(Request, Employee.employee_id == Request.employee_employee_id) \
                .filter(Employee.employee_id == employee_id) \
                .outerjoin(ReturnKey, Request.id == ReturnKey.loan_request_id) \
                .filter(ReturnKey.loan_request_id == None)

            return [[row[1].room_building_name, row[1].room_number] for row in queries]


        while 1:
            print('-----------------------------------------------------------------')
            if input('Enter \'1\' to continue, else to exist ') != '1':
                break
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
                hook_number = int(input('Which hook do you want to create key: '))
                hook = sess.query(Hook).filter(Hook.number == hook_number).first()
                if not hook:
                    print('Cannot find hook')
                    continue
                key_number = int(input('Enter key number: '))
                key = sess.query(Key).filter(Key.number == key_number).first()
                if key:
                    print('Key already exist')
                    continue
                new_key = Key(number=key_number, hook=hook)
                sess.add(new_key)
                sess.commit()

            elif choose == 'b':
                employee_id = input('Enter employee id: ')
                building_name, room_number = input('Enter building and room: ').split()
                employee_id, room_number = int(employee_id), int(room_number)
                rooms = room_employee_can_enter(employee_id)
                if [building_name, room_number] in rooms:
                    print(employee_id, 'already has access to the room')
                    continue

                all_key = sess.query(Key).join(HookDoor, Key.hook_number == HookDoor.hook_number) \
                    .filter(and_(HookDoor.door_room_building_name == building_name,
                                 HookDoor.door_room_number == room_number)).all()

                key_not_return = sess.query(Key).join(Loan, Key.number == Loan.key_number) \
                    .outerjoin(ReturnKey, Loan.request_id == ReturnKey.loan_request_id) \
                    .filter(or_(ReturnKey.loan_request_id == None, ReturnKey.loss)).all()
                key = {}
                for k in all_key:
                    if k not in key_not_return:
                        key = k
                        break
                if not key:
                    print('Keys for the room are not available')
                    continue
                date = input('Enter current date: ')

                employee = sess.query(Employee).filter(Employee.employee_id == employee_id)[0]
                room = sess.query(Room).filter(and_(Room.building_name == building_name, Room.number == room_number))[0]
                request = employee.request_room(room=room, request_time=date)
                request.grant_key(key=key)
                sess.commit()

            elif choose == 'c':
                employee_id = int(input('Enter employee id: '))
                key_number = int(input('Enter key number: '))
                keys = sess.query(Loan.key_number, Request.request_time).select_from(Employee) \
                    .join(Request, Employee.employee_id == Request.employee_employee_id) \
                    .filter(Employee.employee_id == employee_id) \
                    .join(Loan, Request.id == Loan.request_id) \
                    .outerjoin(ReturnKey, Loan.request_id == ReturnKey.loan_request_id) \
                    .filter(ReturnKey.loan_request_id == None).all()
                key = {}
                for k in keys:
                    if k[0] == key_number:
                        key = k
                        break
                if not key:
                    print('Employee', employee_id, 'does not have the key')
                else:
                    print('Employee', employee_id, 'have the key on', key[1])

            elif choose == 'd':
                key_number = int(input('Enter key number: '))
                key = sess.query(Key).filter(Key.number == key_number).first()
                if not key:
                    print('Key does not exist')
                    continue
                q = sess.query(Loan.key_number).select_from(Loan) \
                    .join(ReturnKey, Loan.request_id == ReturnKey.loan_request_id) \
                    .filter(and_(Loan.key_number == key_number, ReturnKey.loss)).first()
                if q:
                    print('Key is lost')
                else:
                    print('Key is not lost')

            elif choose == 'e':
                keys = list(map(lambda x: int(x), input('Enter all the key numbers you have: ').split()))
                q = sess.query(HookDoor.door_room_building_name, HookDoor.door_room_number).select_from(Key) \
                    .join(Hook, Key.hook_number == Hook.number).filter(Key.number.in_(keys)) \
                    .join(HookDoor, Hook.number == HookDoor.hook_number).all()
                print('You can enter: ', end='')
                res = ', '.join([' '.join([room[0], str(room[1])]) for room in q])
                print(res)

            elif choose == 'f':
                key_number = int(input('Enter key number: '))
                key = sess.query(Key).filter(Key.number == key_number).first()
                if not key:
                    print('Key does not exist')
                    continue
                sess.delete(key)
                sess.commit()

            elif choose == 'g':
                employee_id = int(input('Enter employee id: '))
                employee = sess.query(Employee).filter(Employee.employee_id == employee_id).first()
                if not employee:
                    print('Employee does not exist')
                    continue
                sess.delete(employee)
                sess.commit()

            elif choose == 'h':
                hook_number = int(input('Enter hook number: '))

            elif choose == 'i':
                old_employee_id = int(input('Enter old employee id: '))
                new_employee_id = int(input('Enter new employee id: '))


            elif choose == 'j':
                building_name, room_number = input('Enter building and room: ').split()
                room_number = int(room_number)

                q = sess.query(Employee.employee_id, Employee.name).select_from(Room) \
                    .filter(and_(Room.building_name == building_name, Room.number == room_number)) \
                    .join(Request, and_(Room.building_name == Request.room_building_name,
                                        Room.number == Request.room_number)) \
                    .outerjoin(ReturnKey, Request.id == ReturnKey.loan_request_id) \
                    .filter(ReturnKey.loan_request_id == None) \
                    .join(Employee, Request.employee_employee_id == Employee.employee_id).distinct().all()
                if not q:
                    print('No employee can enter the room')
                    continue
                print('Employees can enter the room: ', end='')
                res = ', '.join([' - '.join([str(employee[0]), employee[1]]) for employee in q])
                print(res)


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
