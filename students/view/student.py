from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView

from security.functions import addUserData
from students.forms import StudentsForm
from students.models import Students


class StudentsCreateView(CreateView):
    model = Students
    template_name = 'students/student/create.html'
    form_class = StudentsForm
    success_url = reverse_lazy('students:students_registers_search')

    def get_initial(self):
        super(StudentsCreateView, self).get_initial()

        self.initial = {
            'dni': self.request.GET.get('dni') if self.request.method == 'GET' else self.request.POST.get('dni'),
        }
        return self.initial

    def post(self, request, *args, **kwargs):
        data = {'errors': [], 'message': "No ha enviado ninguna opcion"}
        status = 500

        action = request.POST['action']

        if action == 'add':
            form = self.get_form()

            if Students.objects.filter(dni=self.request.POST.get('dni')).exists():
                status = 400
                data['message'] = 'Error'
                data['errors'] = ['Ya existe un dni registrado.']
                return JsonResponse(data, status=status)

            if form.is_valid():
                status = 200
                form.save()
                return JsonResponse(data, status=status)

            data['message'] = 'Error'
            data['errors'] = form.errors
            return JsonResponse(data, status=status)

        data['code'] = 'failed'
        return JsonResponse(data, status=status)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        addUserData(self.request, context)
        context['form_action'] = 'Crear'
        context['student_id'] = self.request.GET.get('student_id')
        context['success_url'] = self.success_url
        context['back_url'] = self.success_url
        context['title_label'] = "Nuevo registro de estudiante"
        return context
