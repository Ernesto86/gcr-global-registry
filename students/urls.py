from django.urls import path

from students.view.student import StudentsCreateView
from students.view.student_registers import StudentRegistersView, StudentRegistersSearchView, StudentRegistersCreateView

app_name = 'students'

urlpatterns = [
    path('students-registers', StudentRegistersView.as_view(), name='students_registers'),
    path('students-registers/search', StudentRegistersSearchView.as_view(), name='students_registers_search'),
    path('students-registers/create', StudentRegistersCreateView.as_view(), name='students_registers_create'),
    path('students/create', StudentsCreateView.as_view(), name='students_create'),
]
