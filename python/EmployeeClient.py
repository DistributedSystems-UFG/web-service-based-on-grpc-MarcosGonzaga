from __future__ import print_function
import logging

import grpc
import EmployeeService_pb2
import EmployeeService_pb2_grpc

import const

def run():
    with grpc.insecure_channel(const.IP + ':' + const.PORT) as channel:
        stub = EmployeeService_pb2_grpc.EmployeeServiceStub(channel)

        # Query an employee's data
        response = stub.GetEmployeeDataFromID(EmployeeService_pb2.EmployeeID(id=101))
        print('Employee\'s data: ' + str(response))

        # Add a new employee
        new_employee_request = EmployeeService_pb2.EmployeeData(
            id=301,
            name='Jose da Silva',
            title='Programmer',
            salary=90000.0  # Adicione um exemplo de salário ao criar um novo funcionário
        )
        response = stub.CreateEmployee(new_employee_request)
        print('Added new employee ' + response.status)

        # Change an employee's details (including title)
        updated_employee_request = EmployeeService_pb2.EmployeeDetailsUpdate(
            id=301,
            name='Jose da Silva Updated',
            title='Senior Programmer'
        )
        response = stub.UpdateEmployeeDetails(updated_employee_request)
        print('Updated employee ' + response.status)

        # Delete an employee
        response = stub.DeleteEmployee(EmployeeService_pb2.EmployeeID(id=201))
        print('Deleted employee ' + response.status)

        # List all employees
        response = stub.ListAllEmployees(EmployeeService_pb2.EmptyMessage())
        print('All employees: ' + str(response))

        # Update an employee's salary
        update_salary_request = EmployeeService_pb2.EmployeeSalaryUpdate(
            id=101,
            new_salary=110000.0  # Adicione um exemplo de novo salário
        )
        response = stub.UpdateEmployeeSalary(update_salary_request)
        print('Updated employee salary: ' + str(response))

        # Calculate average salary
        response = stub.AverageSalary(EmployeeService_pb2.EmptyMessage())
        print('Average salary: ' + str(response.average_salary))


if __name__ == '__main__':
    logging.basicConfig()
    run()
