'use strict';

const ErrorCommon = {
    CONSTANT: {},
    elem: {},
    repeat: {},
    loadFirst: {},
    fun: {
        getErrors: (errors) => {

            if (!errors) return []

            try {
                const errorsNew = Array.isArray(data?.errors) ? data?.errors : Object.values(data?.errors)

                errorsNew.map(elem => {
                    elem.map(element => element)
                })
            } catch (e) {
                return []
            }
        },
        getExtractErrorList: (errors) => {

            if (Array.isArray(errors))
                1

            if (!errors) return []

            Object.values(data?.errors).map(elem => {
                elem.map(element => element)
            })
        }
    },
    funHTML: {
        getErrors: (errors) => {
            let html = '<ul class="ms-5 d-block">'
            ErrorCommon.fun.getErrors(errors).map(elem => `<li>${elem}</li>`)
            html += '</ul>'
            return html
        },
        showErrorsSimpleFacade: (message, errors) => {
            let errorHtml = ErrorCommon.funHTML.getErrors(errors)

            AppSystem.handleComp.alert.alert.show({
                title: message, content: errorHtml, typeFeature: AppSystem.CONSTANT.typeFeature.danger
            })
        },
        showErrorsOnlyAlert: (message, errors) => {
            let errorHtml = ErrorCommon.funHTML.getErrors(errors)
            alert(errorHtml)
        }
    }
}