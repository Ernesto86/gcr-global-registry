"use strict"

const CrudCommon = {
  CONSTANT: {},
  elem: {},
  repeat: {},
  loadFirst: {},
  fun: {},
  fetch: {
    submitForm: async ({
      formData,
      path = location.pathname,
      configExtra = {
        method: ClientHttpFetch.CONSTANT.verboseMethod.POST.description,
      },
    }) => {
      AppSystem.fun.showLoadingSimpleFacade()

      const dataJson = await ClientHttpFetch.exec(path, formData, configExtra)

      const { code, message, data, ...stateExtra } = dataJson

      AppSystem.fun.hiddenLoadingUi()

      if (ErrorResponse.KIND_STATIC === stateExtra.kind)
        ErrorCommon.funHTML.showErrorsSimpleFacade(message, data?.errors)

      return dataJson
    },
    fetchFormOnlyLoading: async ({
      formData,
      path = location.pathname,
      method = ClientHttpFetch.CONSTANT.verboseMethod.POST.description,
    }) => {
      AppSystem.fun.showLoadingUi()

      const dataJson = await ClientHttpFetch.exec(path, formData, method)

      const { code, message, data, ...stateExtra } = dataJson

      AppSystem.fun.hiddenLoadingUi()

      if (ErrorResponse.KIND_STATIC === stateExtra.kind)
        ErrorCommon.funHTML.showErrorsOnlyAlert(message, data?.errors)

      return dataJson
    },
    delete: async ({
      dataFetch = {},
      path = location.pathname,
      configExtra = {
        method: ClientHttpFetch.CONSTANT.verboseMethod.DELETE.description,
      },
    }) => {
      AppSystem.fun.showLoadingUi()

      const dataJson = await ClientHttpFetch.exec(path, dataFetch, configExtra)

      const { code, message, data, ...stateExtra } = dataJson

      AppSystem.fun.hiddenLoadingUi()

      if (ErrorResponse.KIND_STATIC === stateExtra.kind)
        ErrorCommon.funHTML.showErrorsOnlyAlert(message, data?.errors)
      // AppSystem.handleComp.alert.alert.show({
      //     title: message,
      //     typeFeature: AppSystem.CONSTANT.typeFeature.danger
      // })

      return dataJson
    },
  },
  axios: {},
}
