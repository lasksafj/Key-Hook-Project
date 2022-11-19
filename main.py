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

    # metadata.drop_all(bind=engine)  # start with a clean slate while in development
    #
    # metadata.create_all(bind=engine)

    sec1: Section = Section(section_id="123", department_name="CECS", course_name="323", section_number=1,
                            semester="Fall", year=2022)

    student1: Student = Student(student_id="1111", last_name="Nguyen", first_name="Nhat")
    student2: Student = Student(student_id="2222", last_name="Tran", first_name="Quy")
    student3: Student = Student(student_id="3333", last_name="Truong", first_name="Toan")

    with Session() as sess:
        sess.begin()
        print("Inside the session, woo hoo.")
        sess.add(sec1)
        sess.add(student1)
        sess.add(student2)
        sess.add(student3)
        sess.commit()

        sec1.add_student(student1, '3.5')
        sec1.add_student(student2, '3.5')
        sec1.add_student(student3, '3.5')
        sess.commit()

        students = sess.query(Student).all()
        print("Student: ")
        for student in students:
            pprint(student.__dict__)
        enrollments = sess.query(Enrollment).all()
        print("Enrollment: ")
        for e in enrollments:
            pprint(e.__dict__)
        sections = sess.query(Section).all()
        print("Section: ")
        for e in sections:
            pprint(e.__dict__)

    print("Exiting normally.")