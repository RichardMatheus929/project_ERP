from companies.views.base import Base
from companies.utils.permission import TaskPermission
from companies.serializers import TaskSerializer,TasksSerializer
from companies.models import Task

from rest_framework.response import Response
from rest_framework.exceptions import APIException

import datetime

class Tasks(Base):
    permission_classes = [TaskPermission]

    def get(self,request) -> Response:
        
        enterprise_id = self.get_enterprise_id(request.user.id)

        tasks = Task.objects.filter(enterprise_id=enterprise_id).all()

        serializer = TasksSerializer(tasks,many=True)

        return Response({"Tasks":serializer.data})
    
    def post(self,request):
        employee_id = request.data.get('employee_id')
        title = request.data.get('title')
        description = request.data.get('description')
        status_id = request.data.get('status_id')
        due_date = request.data.get('due_date')

        employee = self.get_employee(employee_id,request.user.id)
        _status = self.get_status(status_id)

        # Criando validações
        if not title or len(title) > 125:
            raise APIException("Título não enviado ou maior que 125")
        
        if due_date:
            try:
                due_date = datetime.datetime.strptime(due_date,"%d/%m/%Y %H:%M")
            except ValueError:
                raise APIException("Data fora do padrão do sistema")

        task = Task.objects.create(
            title=title,
            description=description,
            due_date=due_date,
            status_id=status_id,
            employee_id=employee_id,
            enterprise_id=employee.enterprise.id,
        )

        serializer = TaskSerializer(task)

        return Response({"Task": serializer.data})
    
class TaskDetail(Base):
    permission_classes = [TaskPermission]

    def get(self,request,task_id):
        enterprise_id = self.get_enterprise_id(request.user.id)

        task = self.get_tasks(task_id,enterprise_id)

        serializer = TaskSerializer(task)

        return Response({"task":serializer.data})
    
    def put(self,request,task_id):
        enterprise_id = self.get_enterprise_id(request.user.id)

        task = self.get_tasks(task_id,enterprise_id)

        title = request.data.get('title',task.title)
        employee_id = request.data.get('employee_id',task.employee.id)
        description = request.data.get('description',task.description)
        status_id = request.data.get('status_id',task.status.id)
        due_date = request.data.get('due_date',task.due_date)

        # Validadores
        self.get_status(status_id)
        self.get_employee(employee_id,request.user.id)

        if due_date and due_date != task.due_date:
            try:
                due_date = datetime.datetime.strptime(due_date,"%d/%m/%Y %H:%M")
            except ValueError:
                raise APIException("Data fora do padrão do sistema")

        data = {
            'title': title,
            "description": description,
            "status_id": status_id,
            "employee_id": employee_id,
            "due_date": due_date,
        }

        serializer = TaskSerializer(task, data=data, partial=True)

        if not serializer.is_valid():
            raise APIException("Não foi possível atualizar a tarefa")
        
        serializer.update(task, serializer.validated_data)

        task.status_id = status_id
        task.employee_id = employee_id
        task.save()

        return Response({"task":serializer.data})
    
    def delete(self,request, task_id):
        enterprise_id = self.get_enterprise_id(request.user.id)

        _task = self.get_tasks(task_id,enterprise_id).delete()

        return Response({"sucess":True})
