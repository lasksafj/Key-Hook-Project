-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2022-11-18 05:55:36.022

-- tables
-- Table: buildings
CREATE TABLE buildings (
    name varchar(30)  NOT NULL,
    CONSTRAINT buildings_pk PRIMARY KEY (name)
);

-- Table: doors
CREATE TABLE doors (
    room_building_name varchar(10)  NOT NULL,
    room_number int  NOT NULL,
    name varchar(20)  NOT NULL,
    CONSTRAINT doors_pk PRIMARY KEY (room_number,room_building_name,name)
);

-- Table: employees
CREATE TABLE employees (
    name varchar(60)  NOT NULL,
    employee_id int  NOT NULL,
    CONSTRAINT employees_pk PRIMARY KEY (employee_id)
);

-- Table: hook_door
CREATE TABLE hook_door (
    hook_number int  NOT NULL,
    door_room_building_name varchar(10)  NOT NULL,
    door_room_number int  NOT NULL,
    door_name varchar(20)  NOT NULL,
    CONSTRAINT hook_door_pk PRIMARY KEY (hook_number,door_room_number,door_room_building_name,door_name)
);

-- Table: hooks
CREATE TABLE hooks (
    number int  NOT NULL,
    CONSTRAINT hooks_pk PRIMARY KEY (number)
);

-- Table: keys
CREATE TABLE keys (
    number int  NOT NULL,
    hook_number int  NOT NULL,
    CONSTRAINT keys_pk PRIMARY KEY (number)
);

-- Table: loan
CREATE TABLE loan (
    key_number int  NOT NULL,
    request_id int  NOT NULL,
    CONSTRAINT loan_pk PRIMARY KEY (request_id)
);

-- Table: requests
CREATE TABLE requests (
    employee_employee_id int  NOT NULL,
    room_building_name varchar(10)  NOT NULL,
    room_number int  NOT NULL,
    request_time time  NOT NULL,
    id serial  NOT NULL,
    CONSTRAINT request_uk_01 UNIQUE (employee_employee_id, request_time, room_building_name, room_number) NOT DEFERRABLE  INITIALLY IMMEDIATE,
    CONSTRAINT requests_pk PRIMARY KEY (id)
);

-- Table: return
CREATE TABLE return (
    loan_request_id int  NOT NULL,
    loss boolean  NOT NULL,
    return_time time  NOT NULL,
    CONSTRAINT return_pk PRIMARY KEY (loan_request_id)
);

-- Table: rooms
CREATE TABLE rooms (
    building_name varchar(10)  NOT NULL,
    number int  NOT NULL,
    CONSTRAINT rooms_pk PRIMARY KEY (number,building_name)
);

-- foreign keys
-- Reference: door_room (table: doors)
ALTER TABLE doors ADD CONSTRAINT door_room
    FOREIGN KEY (room_number, room_building_name)
    REFERENCES rooms (number, building_name)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: hook_door_door (table: hook_door)
ALTER TABLE hook_door ADD CONSTRAINT hook_door_door
    FOREIGN KEY (door_room_number, door_room_building_name, door_name)
    REFERENCES doors (room_number, room_building_name, name)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: hook_door_hook (table: hook_door)
ALTER TABLE hook_door ADD CONSTRAINT hook_door_hook
    FOREIGN KEY (hook_number)
    REFERENCES hooks (number)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: key_hook (table: keys)
ALTER TABLE keys ADD CONSTRAINT key_hook
    FOREIGN KEY (hook_number)
    REFERENCES hooks (number)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: loan_key (table: loan)
ALTER TABLE loan ADD CONSTRAINT loan_key
    FOREIGN KEY (key_number)
    REFERENCES keys (number)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: loan_request (table: loan)
ALTER TABLE loan ADD CONSTRAINT loan_request
    FOREIGN KEY (request_id)
    REFERENCES requests (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: request_employee (table: requests)
ALTER TABLE requests ADD CONSTRAINT request_employee
    FOREIGN KEY (employee_employee_id)
    REFERENCES employees (employee_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: request_room (table: requests)
ALTER TABLE requests ADD CONSTRAINT request_room
    FOREIGN KEY (room_number, room_building_name)
    REFERENCES rooms (number, building_name)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: return_loan (table: return)
ALTER TABLE return ADD CONSTRAINT return_loan
    FOREIGN KEY (loan_request_id)
    REFERENCES loan (request_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: room_building (table: rooms)
ALTER TABLE rooms ADD CONSTRAINT room_building
    FOREIGN KEY (building_name)
    REFERENCES buildings (name)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- End of file.

