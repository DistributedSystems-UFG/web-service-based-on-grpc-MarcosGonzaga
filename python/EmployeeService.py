from concurrent import futures
import logging

import grpc
import EmployeeService_pb2
import EmployeeService_pb2_grpc

import const

empDB = [
    {
        'id': 101,
        'name': 'Saravanan S',
        'title': 'Technical Leader',
        'salary': 100000.0
    },
    {
        'id': 201,
        'name': 'Rajkumar P',
        'title': 'Sr Software Engineer',
        'salary': 80000.0
    }
]

class EmployeeServer(EmployeeService_pb2_grpc.EmployeeServiceServicer):

    def CreateEmployee(self, request, context):
        dat = {
            'id': request.id,
            'name': request.name,
            'title': request.title,
            'salary': request.salary
        }
        empDB.append(dat)
        return EmployeeService_pb2.StatusReply(status='OK')

    def GetEmployeeDataFromID(self, request, context):
        usr = [emp for emp in empDB if emp['id'] == request.id]
        if usr:
            return EmployeeService_pb2.EmployeeData(
                id=usr[0]['id'],
                name=usr[0]['name'],
                title=usr[0]['title'],
                salary=usr[0]['salary']
            )
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Employee not found")
            return EmployeeService_pb2.EmployeeData()

    def UpdateEmployeeDetails(self, request, context):
        usr = [emp for emp in empDB if emp['id'] == request.id]
        if usr:
            usr[0]['name'] = request.name
            usr[0]['title'] = request.title
            return EmployeeService_pb2.StatusReply(status='OK')
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Employee not found")
            return EmployeeService_pb2.StatusReply(status='NOK')

    def DeleteEmployee(self, request, context):
        usr = [emp for emp in empDB if emp['id'] == request.id]
        if usr:
            empDB.remove(usr[0])
            return EmployeeService_pb2.StatusReply(status='OK')
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Employee not found")
            return EmployeeService_pb2.StatusReply(status='NOK')

    def ListAllEmployees(self, request, context):
        employee_data_list = EmployeeService_pb2.EmployeeDataList()
        for item in empDB:
            emp_data = EmployeeService_pb2.EmployeeData(
                id=item['id'],
                name=item['name'],
                title=item['title'],
                salary=item['salary']
            )
            employee_data_list.employee_data.append(emp_data)
        return employee_data_list

    def UpdateEmployeeSalary(self, request, context):
        usr = [emp for emp in empDB if emp['id'] == request.id]
        if usr:
            usr[0]['salary'] = request.new_salary
            return EmployeeService_pb2.StatusReply(status='OK')
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Employee not found")
            return EmployeeService_pb2.StatusReply(status='NOK')

    def AverageSalary(self, request, context):
        total_salary = sum(emp['salary'] for emp in empDB)
        average_salary = total_salary / max(len(empDB), 1)
        return EmployeeService_pb2.AverageSalaryReply(average_salary=average_salary)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    EmployeeService_pb2_grpc.add_EmployeeServiceServicer_to_server(EmployeeServer(), server)
    server.add_insecure_port('[::]:' + const.PORT)
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
