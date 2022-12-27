from django.db.models import Sum
from django.forms import model_to_dict
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from core.common.form.form_common import FormCommon
from security.functions import addUserData
from security.manager.organizador_registros_manager import OrganizadorRegistrosManager
from security.mixins import PermissionMixin
from students.forms import StudentRegistersSearchForm, StudentRegistersForm
from students.models import Students, StudentRegisters, Certificates
from system.models import SysParameters, SysCountries
from transactions.models import InstitutionQuotesTypeRegister


class StudentRegistersView(PermissionMixin, TemplateView):
    template_name = 'students/student_registers/view.html'
    permission_required = 'add_studentregisters'

    def post(self, request, *args, **kwargs):
        data = {'errors': [], 'message': ''}
        status = 500

        action = request.POST.get('action', None)

        if action == 'type_registries_list':

            organizador_registros_manager = OrganizadorRegistrosManager(self.request.user)
            data['type_registries_list'] = organizador_registros_manager.get_type_registries_list()
            status = 200

        elif action == 'type_registries_count_available_list':

            organizador_registros_manager = OrganizadorRegistrosManager(self.request.user)
            type_registries_count_available_list = organizador_registros_manager.get_type_registries_count_available_list()
            data['type_registries_count_available_list'] = type_registries_count_available_list
            status = 200

        return JsonResponse(data, status=status)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        addUserData(self.request, context)
        context['title_label'] = 'INGRESO INTERNACIONAL DE REGISTROS INSTITUCIONAL'
        institution_quotes_type_register_sum = InstitutionQuotesTypeRegister.objects.filter(
            institution_id=context['user'].institution_id,
            deleted=False,
        ).aggregate(
            quotas=Sum('quotas'),
            quotas_balance=Sum('quotas_balance'),
        )

        context['institution_quotes_type_register_sum'] = institution_quotes_type_register_sum
        context['register_into_quotas'] = StudentRegisters.objects.filter(
            institution_id=context['user'].institution_id,
            deleted=False
        ).count()
        return context


class StudentRegistersSearchView(PermissionMixin, TemplateView):
    template_name = 'students/student_registers/search.html'
    permission_required = ('add_studentregisters',)

    def post(self, request, *args, **kwargs):
        data = {'errors': [], 'message': "No ha enviado ninguna opcion"}
        status = 500

        action = request.POST.get('action', '')

        if action == 'search':
            identification = request.POST.get('identification')

            try:
                student = Students.objects.get(dni=identification)
                data['student'] = model_to_dict(student)
                return JsonResponse(data, status=200)

            except Students.DoesNotExist:
                data['message'] = 'No existe el estudiante con el dni buscado'
                return JsonResponse(data, status=404)
            except Exception as ex:
                data['message'] = 'Error inesperado'
                return JsonResponse(data, status=500)

        return JsonResponse(data, status=status)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        addUserData(self.request, context)
        context['form'] = StudentRegistersSearchForm()
        context['title_label'] = "INGRESO INTERNACIONAL DE REGISTROS INSTITUCIONAL"
        return context


class StudentRegistersCreateView(PermissionMixin, CreateView):
    permission_required = ('add_studentregisters',)
    model = StudentRegisters
    template_name = 'students/student_registers/create.html'
    form_class = StudentRegistersForm
    success_url = reverse_lazy('students:students_registers_search')

    paises = {
        "BD": "Bangladesh",
        "BE": "Belgium",
        "BF": "Burkina Faso",
        "BG": "Bulgaria",
        "BA": "Bosnia and Herzegovina",
        "BB": "Barbados",
        "WF": "Wallis and Futuna",
        "BL": "Saint Barthelemy",
        "BM": "Bermuda",
        "BN": "Brunei",
        "BO": "Bolivia",
        "BH": "Bahrain",
        "BI": "Burundi",
        "BJ": "Benin",
        "BT": "Bhutan",
        "JM": "Jamaica",
        "BV": "Bouvet Island",
        "BW": "Botswana",
        "WS": "Samoa",
        "BQ": "Bonaire, Saint Eustatius and Saba ",
        "BR": "Brazil",
        "BS": "Bahamas",
        "JE": "Jersey",
        "BY": "Belarus",
        "BZ": "Belize",
        "RU": "Russia",
        "RW": "Rwanda",
        "RS": "Serbia",
        "TL": "East Timor",
        "RE": "Reunion",
        "TM": "Turkmenistan",
        "TJ": "Tajikistan",
        "RO": "Romania",
        "TK": "Tokelau",
        "GW": "Guinea-Bissau",
        "GU": "Guam",
        "GT": "Guatemala",
        "GS": "South Georgia and the South Sandwich Islands",
        "GR": "Greece",
        "GQ": "Equatorial Guinea",
        "GP": "Guadeloupe",
        "JP": "Japan",
        "GY": "Guyana",
        "GG": "Guernsey",
        "GF": "French Guiana",
        "GE": "Georgia",
        "GD": "Grenada",
        "GB": "United Kingdom",
        "GA": "Gabon",
        "SV": "El Salvador",
        "GN": "Guinea",
        "GM": "Gambia",
        "GL": "Greenland",
        "GI": "Gibraltar",
        "GH": "Ghana",
        "OM": "Oman",
        "TN": "Tunisia",
        "JO": "Jordan",
        "HR": "Croatia",
        "HT": "Haiti",
        "HU": "Hungary",
        "HK": "Hong Kong",
        "HN": "Honduras",
        "HM": "Heard Island and McDonald Islands",
        "VE": "Venezuela",
        "PR": "Puerto Rico",
        "PS": "Palestinian Territory",
        "PW": "Palau",
        "PT": "Portugal",
        "SJ": "Svalbard and Jan Mayen",
        "PY": "Paraguay",
        "IQ": "Iraq",
        "PA": "Panama",
        "PF": "French Polynesia",
        "PG": "Papua New Guinea",
        "PE": "Peru",
        "PK": "Pakistan",
        "PH": "Philippines",
        "PN": "Pitcairn",
        "PL": "Poland",
        "PM": "Saint Pierre and Miquelon",
        "ZM": "Zambia",
        "EH": "Western Sahara",
        "EE": "Estonia",
        "EG": "Egypt",
        "ZA": "South Africa",
        "EC": "Ecuador",
        "IT": "Italy",
        "VN": "Vietnam",
        "SB": "Solomon Islands",
        "ET": "Ethiopia",
        "SO": "Somalia",
        "ZW": "Zimbabwe",
        "SA": "Saudi Arabia",
        "ES": "Spain",
        "ER": "Eritrea",
        "ME": "Montenegro",
        "MD": "Moldova",
        "MG": "Madagascar",
        "MF": "Saint Martin",
        "MA": "Morocco",
        "MC": "Monaco",
        "UZ": "Uzbekistan",
        "MM": "Myanmar",
        "ML": "Mali",
        "MO": "Macao",
        "MN": "Mongolia",
        "MH": "Marshall Islands",
        "MK": "Macedonia",
        "MU": "Mauritius",
        "MT": "Malta",
        "MW": "Malawi",
        "MV": "Maldives",
        "MQ": "Martinique",
        "MP": "Northern Mariana Islands",
        "MS": "Montserrat",
        "MR": "Mauritania",
        "IM": "Isle of Man",
        "UG": "Uganda",
        "TZ": "Tanzania",
        "MY": "Malaysia",
        "MX": "Mexico",
        "IL": "Israel",
        "FR": "France",
        "IO": "British Indian Ocean Territory",
        "SH": "Saint Helena",
        "FI": "Finland",
        "FJ": "Fiji",
        "FK": "Falkland Islands",
        "FM": "Micronesia",
        "FO": "Faroe Islands",
        "NI": "Nicaragua",
        "NL": "Netherlands",
        "NO": "Norway",
        "NA": "Namibia",
        "VU": "Vanuatu",
        "NC": "New Caledonia",
        "NE": "Niger",
        "NF": "Norfolk Island",
        "NG": "Nigeria",
        "NZ": "New Zealand",
        "NP": "Nepal",
        "NR": "Nauru",
        "NU": "Niue",
        "CK": "Cook Islands",
        "XK": "Kosovo",
        "CI": "Ivory Coast",
        "CH": "Switzerland",
        "CO": "Colombia",
        "CN": "China",
        "CM": "Cameroon",
        "CL": "Chile",
        "CC": "Cocos Islands",
        "CA": "Canada",
        "CG": "Republic of the Congo",
        "CF": "Central African Republic",
        "CD": "Democratic Republic of the Congo",
        "CZ": "Czech Republic",
        "CY": "Cyprus",
        "CX": "Christmas Island",
        "CR": "Costa Rica",
        "CW": "Curacao",
        "CV": "Cape Verde",
        "CU": "Cuba",
        "SZ": "Swaziland",
        "SY": "Syria",
        "SX": "Sint Maarten",
        "KG": "Kyrgyzstan",
        "KE": "Kenya",
        "SS": "South Sudan",
        "SR": "Suriname",
        "KI": "Kiribati",
        "KH": "Cambodia",
        "KN": "Saint Kitts and Nevis",
        "KM": "Comoros",
        "ST": "Sao Tome and Principe",
        "SK": "Slovakia",
        "KR": "South Korea",
        "SI": "Slovenia",
        "KP": "North Korea",
        "KW": "Kuwait",
        "SN": "Senegal",
        "SM": "San Marino",
        "SL": "Sierra Leone",
        "SC": "Seychelles",
        "KZ": "Kazakhstan",
        "KY": "Cayman Islands",
        "SG": "Singapore",
        "SE": "Sweden",
        "SD": "Sudan",
        "DO": "Dominican Republic",
        "DM": "Dominica",
        "DJ": "Djibouti",
        "DK": "Denmark",
        "VG": "British Virgin Islands",
        "DE": "Germany",
        "YE": "Yemen",
        "DZ": "Algeria",
        "US": "United States",
        "UY": "Uruguay",
        "YT": "Mayotte",
        "UM": "United States Minor Outlying Islands",
        "LB": "Lebanon",
        "LC": "Saint Lucia",
        "LA": "Laos",
        "TV": "Tuvalu",
        "TW": "Taiwan",
        "TT": "Trinidad and Tobago",
        "TR": "Turkey",
        "LK": "Sri Lanka",
        "LI": "Liechtenstein",
        "LV": "Latvia",
        "TO": "Tonga",
        "LT": "Lithuania",
        "LU": "Luxembourg",
        "LR": "Liberia",
        "LS": "Lesotho",
        "TH": "Thailand",
        "TF": "French Southern Territories",
        "TG": "Togo",
        "TD": "Chad",
        "TC": "Turks and Caicos Islands",
        "LY": "Libya",
        "VA": "Vatican",
        "VC": "Saint Vincent and the Grenadines",
        "AE": "United Arab Emirates",
        "AD": "Andorra",
        "AG": "Antigua and Barbuda",
        "AF": "Afghanistan",
        "AI": "Anguilla",
        "VI": "U.S. Virgin Islands",
        "IS": "Iceland",
        "IR": "Iran",
        "AM": "Armenia",
        "AL": "Albania",
        "AO": "Angola",
        "AQ": "Antarctica",
        "AS": "American Samoa",
        "AR": "Argentina",
        "AU": "Australia",
        "AT": "Austria",
        "AW": "Aruba",
        "IN": "India",
        "AX": "Aland Islands",
        "AZ": "Azerbaijan",
        "IE": "Ireland",
        "ID": "Indonesia",
        "UA": "Ukraine",
        "QA": "Qatar",
        "MZ": "Mozambique"
    }

    def load_countries(self):
        for k, v in self.paises.items():
            SysCountries.objects.create(
                code=k,
                name=v,
                name_short=k,
            )

    def get_initial(self):
        super(StudentRegistersCreateView, self).get_initial()

        student_id = self.request.GET.get('student_id') if self.request.method == 'GET' else self.request.POST.get(
            'student_id')

        self.initial = {
            'student': student_id,
            'code_international_register': SysParameters.get_value_formate_next()['format']
        }
        return self.initial

    def get_form(self, *args, **kwargs):
        form = super(StudentRegistersCreateView, self).get_form(*args, **kwargs)

        student_id = self.request.GET.get('student_id') if self.request.method == 'GET' else self.request.POST.get(
            'student_id')
        institution = self.request.user.institution

        # form.fields['certificate'].queryset = SysCountries.objects.none()
        form.fields['student'].queryset = Students.objects.filter(id=student_id, deleted=False)
        form.fields['type_register'].queryset = institution.get_type_register_enabled_list()
        return form

    def post(self, request, *args, **kwargs):
        data = {'errors': [], 'message': "No ha enviado ninguna opcion"}
        status = 500

        action = request.POST['action']

        if action == 'add':
            form = self.get_form()

            if form.is_valid():
                status = 200
                value_new = SysParameters.get_value_formate_next()
                form.instance.institution_id = self.request.user.institution_id
                form.instance.code_international_register = value_new['format']
                form.save()

                institution_quotes_type_register = InstitutionQuotesTypeRegister.objects.get(
                    institution_id=self.request.user.institution_id,
                    type_register_id=form.instance.type_register_id
                )

                institution_quotes_type_register.quotas_balance -= 1
                institution_quotes_type_register.save()

                SysParameters.update_value(value_new['next_value'])

                return JsonResponse(data, status=status)

            data['message'] = 'Error de validacion de formulario.'
            data['errors'] = [FormCommon.get_errors_dict(form)]
            return JsonResponse(data, status=status)

        elif action == 'certificates':
            status = 200
            type_registry_id = request.POST.get('type_registry_id')

            data['certificates'] = [
                model_to_dict(x) for x in Certificates.objects.filter(type_registry_id=type_registry_id)
            ]

            return JsonResponse(data, status=status)

        return JsonResponse(data, status=status)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        addUserData(self.request, context)
        context['form_action'] = 'Crear'
        context['student_id'] = self.request.GET.get('student_id')
        context['success_url'] = self.success_url
        context['back_url'] = self.success_url
        context['title_label'] = "Crear registro de estudiante"
        # self.load_countries()
        return context
