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

                return errors

            } catch (e) {
                return []
            }
        },
        getExtractErrorList: (errors) => {
        }
    },
    funHTML: {
        getErrors: (errors) => {

            // TODO: getErrors  MEJORAR - REFACTORIZAR

            let html = '<ul class="ms-5 d-block">'
            ErrorCommon.fun.getErrors(errors).map(elem => {
                if (typeof elem === 'string' || elem instanceof String) {

                    html += `<li>${elem}</li>`

                } else if (Array.isArray(elem)) {

                    let html2 = '<ul class="ms-5 d-block">'

                    elem.map(element2 => {

                        html2 += `<li>${element2}</li>`

                    })

                    html2 += '</ul>'

                    html += `<li>${html2}</li>`

                } else if (typeof elem === 'object' && elem !== null) {

                    Object.keys(elem).map(key => {

                        html += `<li>${key}</li>`

                        let html2 = '<ul class="ms-5 d-block">'

                        elem[key].map(element2 => {
                            html2 += `<li>${element2}</li>`
                        })

                        html2 += '</ul>'
                        html += `<li>${html2}</li>`

                    })
                }
            })
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

            let errorsList = [
                message,
                ...ErrorCommon.fun.getErrors(errors)
            ].join(', ')

            alert(errorsList)
        }
    }
}