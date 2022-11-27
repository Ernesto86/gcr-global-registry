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

    @staticmethod
    def update_all_field(lt_field, with_place_holder=False):
        """
            FUNCION QUE ME PERMITE ATUALIZAR LOS CAMPOS DEACUERDO A UNA CONFIGURACION
        """
        for key in lt_field:
            field = lt_field[key]

            class_cls = field.widget.attrs.get('class')
            style = field.widget.attrs.get('style')

            class_cls = f' {class_cls} {CONSTANT_CLS_BOOTSTRAP} ' if class_cls else CONSTANT_CLS_BOOTSTRAP
            if class_cls.__contains__('cls_decimal'):
                class_cls = f'{class_cls} input-large text-right'

            if hasattr(field, 'choices'):
                class_cls += ' select2 '
                if style:
                    style += ' width: 100%; '
                else:
                    style = ' width: 100%; '

            field.widget.attrs.update({
                'class': class_cls,
                'placeholder': f'{CONSTANT_STANDARD_PRESENT if with_place_holder else ""} {field.label.lower()}',
                'style': style
            })
