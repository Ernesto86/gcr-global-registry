from core.common.form.form_constant import CONSTANT_CLS_BOOTSTRAP, CONSTANT_STANDARD_PRESENT


class FormCommon:

    @staticmethod
    def update_disabled_field(field_list, state=True):
        """
            FUNCION QUE ME PERMITE HACER UN CAMPO COMO SOLO LECTURA
        """
        for key in field_list:
            field = field_list[key]
            field.widget.attrs['disabled'] = state

    @staticmethod
    def update_readonly_field(field_list, state=True):
        """
            FUNCION QUE ME PERMITE HACER UN CAMPO COMO SOLO LECTURA
        """
        for key in field_list:
            field = field_list[key]
            field.widget.attrs['readonly'] = state

    @staticmethod
    def update_required_field(field_list, state=True):
        """
            FUNCION QUE ME PERMITE ATUALIZAR LOS CAMPOS DEACUERDO A UNA CONFIGURACION
        """
        for key in field_list:
            field = field_list[key]
            field.widget.attrs['required'] = state
