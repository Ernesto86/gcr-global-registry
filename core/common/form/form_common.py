from core.common.form.form_constant import CONSTANT_CLS_BOOTSTRAP, CONSTANT_STANDARD_PRESENT, \
    CONSTANT_CLS_CHECKBOX_BOOTSTRAP


class FormCommon:
    CLS_BACKGROUND_READONLY = "bg-secondary bg-opacity-10"

    @staticmethod
    def get_errors_dict(form):
        errors = {}
        for key, value in form.errors.items():
            field = form.fields[key]
            errors[field.label] = value
        return errors

    @staticmethod
    def update_disabled_field(fields, is_list=False):
        """
            HACER UN CAMPO COMO DESACTIVADO
        """
        if is_list:
            for field in fields:
                field.widget.attrs['disabled'] = True
        else:
            for key in fields:
                field = fields[key]
                field.widget.attrs['disabled'] = True

    @staticmethod
    def update_readonly_field(fields, is_list=False):
        """
            HACER UN CAMPO COMO SOLO LECTURA
        """
        if is_list:
            for field in fields:
                FormCommon.update_dictionary_class_readonly(field)
        else:
            for key in fields:
                field = fields[key]
                FormCommon.update_dictionary_class_readonly(field)

    @staticmethod
    def update_dictionary_class_readonly(field):
        class_cls = field.widget.attrs.get('class')
        class_cls = f"{class_cls} {FormCommon.CLS_BACKGROUND_READONLY}" if class_cls else FormCommon.CLS_BACKGROUND_READONLY
        field.widget.attrs.update({
            'readonly': 'readonly',
            'class': class_cls,
        })

    @staticmethod
    def update_required_field(fields, state=True, is_list=False, excludes: tuple = ()):
        """
            ATUALIZAR LOS CAMPOS DEACUERDO A UNA CONFIGURACION
        """
        if is_list:
            for field in fields:
                field.widget.attrs['required'] = state
        else:
            for key in fields:
                field = fields[key]
                if key not in excludes:
                    field.widget.attrs['required'] = state

    @staticmethod
    def update_all_field(fields, with_place_holder=False, with_place_holder_cover=True):
        """
            ATUALIZAR LOS CAMPOS DEACUERDO A UNA CONFIGURACION
        """
        for key in fields:
            field = fields[key]
            settings = {}

            class_cls = field.widget.attrs.get('class')
            style = field.widget.attrs.get('style')

            if field.widget.input_type == 'checkbox':
                class_cls = f' {class_cls} {CONSTANT_CLS_CHECKBOX_BOOTSTRAP} ' if class_cls else CONSTANT_CLS_CHECKBOX_BOOTSTRAP
            # TODO: en algun momento realizar pruebas para cambir la condicional if hasattr(field, 'choices'):
            # elif field.widget.input_type == 'select':
            #     pass
            else:
                class_cls = f' {class_cls} {CONSTANT_CLS_BOOTSTRAP} ' if class_cls else CONSTANT_CLS_BOOTSTRAP

            if class_cls.__contains__('cls_decimal'):
                class_cls = f'{class_cls} input-large text-right'

            if hasattr(field, 'choices'):
                class_cls += ' select2 '
                if style:
                    style += ' width: 100%; '
                else:
                    style = ' width: 100%; '

            if with_place_holder_cover:
                settings = {
                    'placeholder': f'{CONSTANT_STANDARD_PRESENT if with_place_holder else ""} {field.label.lower()}',
                }

            field.widget.attrs.update({
                'class': class_cls,
                'style': style,
                **settings
            })
