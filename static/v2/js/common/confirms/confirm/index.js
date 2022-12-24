'use strict';


const ConfirmCommon = {
    CONSTANT: {
        theme: 'bootstrap',
        title: 'Confirmación',
        icon: 'fas fa-info-circle',
        content: '¿Esta seguro de realizar la siguiente acción?',
    },
    fun: {},
    exec: (props = {}) => {
        const {
            theme = ConfirmCommon.CONSTANT.theme,
            title = ConfirmCommon.CONSTANT.title,
            icon = ConfirmCommon.CONSTANT.icon,
            content = ConfirmCommon.CONSTANT.content,
            columnClass = 'small',
            typeAnimated = true,
            cancelButtonClass = 'btn-primary',
            draggable = true,
            dragWindowBorder = false,
            confirmCallback = null,
            btnInfoText = 'Si',
            btnDangerText = 'No',
            btnInfoClass = 'btn-primary w-25',
            cancelCallback = null,
            btnDangerClass = 'btn-danger w-25',
        } = props

        $.confirm({
            theme,
            title,
            icon,
            content,
            columnClass,
            typeAnimated,
            cancelButtonClass,
            draggable,
            dragWindowBorder,
            buttons: {
                confirm: {
                    text: btnInfoText,
                    btnClass: btnInfoClass,
                    action: function () {
                        if (confirmCallback)
                            confirmCallback()
                    }
                },
                cancel: {
                    text: btnDangerText,
                    btnClass: btnDangerClass,
                    action: function () {
                        if (cancelCallback)
                            cancelCallback()
                    }
                },
            }
        });
    },
}

