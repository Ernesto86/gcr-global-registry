'use strict';

const CrudCommon = {
    CONSTANT: {},
    elem: {},
    repeat: {},
    loadFirst: {},
    fun: {},
    fetch: {
        submitForm: async (
            {
                formData,
                path = location.pathname,
                method = ClientHttpFetch.CONSTANT.verboseMethod.POST.description
            }
        ) => {
            AppSystem.fun.showLoadingSimpleFacade()

            const {code, message, data, ...stateExtra} = await ClientHttpFetch.exec(
                path,
                formData,
                method
            )

            AppSystem.fun.hiddenLoadingUi()

            if (ErrorResponse.KIND_STATIC === stateExtra.kind)
                ErrorCommon.funHTML.showErrorsSimpleFacade(message, data?.errors)

            return {code, message, data, stateExtra}
        },
        submitFormOnlyLoading: async (
            {
                formData,
                path = location.pathname,
                method = ClientHttpFetch.CONSTANT.verboseMethod.POST.description
            }
        ) => {
            AppSystem.fun.showLoadingUi()

            const {code, message, data, ...stateExtra} = await ClientHttpFetch.exec(
                path,
                formData,
                method
            )

            AppSystem.fun.hiddenLoadingUi()

            if (ErrorResponse.KIND_STATIC === stateExtra.kind)
                ErrorCommon.funHTML.showErrorsOnlyAlert(message, data?.errors)

            return {code, message, data, stateExtra}
        },
        delete: async (
            {
                dataFetch = {},
                path = location.pathname,
            }
        ) => {

            AppSystem.fun.showLoadingUi()

            const {code, message, data, ...stateExtra} = await ClientHttpFetch.exec(
                path,
                dataFetch,
                {method: ClientHttpFetch.CONSTANT.verboseMethod.DELETE.description}
            )

            AppSystem.fun.hiddenLoadingUi()

            if (ErrorResponse.KIND_STATIC === stateExtra.kind)
                ErrorCommon.funHTML.showErrorsOnlyAlert(message, data?.errors)
            // AppSystem.handleComp.alert.alert.show({
            //     title: message,
            //     typeFeature: AppSystem.CONSTANT.typeFeature.danger
            // })

            return {code, message, data, stateExtra}
        },

    },
    axios: {}
}