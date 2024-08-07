from django.urls import path
from companies.views.emplyoees import Emplyoees,EmployeeDetail
from companies.views.permissions import PermissionDetail
from companies.views.groups import Groups,GroupDetail
from companies.views.tasks import Tasks,TaskDetail

urlpatterns = [
    # endpoints de Employees
    path('employees',Emplyoees.as_view()),
    path('employees/<int:employee_id>',EmployeeDetail.as_view()),

    # endpoints de permissao de grupos
    path('groups',Groups.as_view()),
    path('groups/<int:group_id>',GroupDetail.as_view()),
    path('permissions',PermissionDetail.as_view()),

    # endpoints de tasks
    path('tasks',Tasks.as_view()),
    path('tasks/<int:task_id>'  ,TaskDetail.as_view())
]