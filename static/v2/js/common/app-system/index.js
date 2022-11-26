'use strict';

const AppSystem = {
    CONSTANT: {
        actionType: {
            add: 'add',
            edit: 'edit'
        },
        loadingType: {
            one: 'one',
            two: 'two',
            three: 'three',
        },
        typeFeature: {
            primary: 'primary',
            secondary: 'secondary',
            success: 'success',
            danger: 'danger',
            warning: 'warning',
            info: 'info',
            light: 'light',
            dark: 'dark',
        }
    },
    elem: {
        $loadingUi: document.getElementById('id-loadContent'),
        $loadingUi2: document.getElementById('id-loadContent2'),
        $loadingUi3: document.getElementById('id-loadContent3'),
    },
    repeat: {},
    loadFirst: {},
    fun: {
        showLoadingUi: function (loadingType = AppSystem.CONSTANT.loadingType.one) {
            if (loadingType === AppSystem.CONSTANT.loadingType.one)
                return AppSystem.elem.$loadingUi.classList.remove('d-none')
            if (loadingType === AppSystem.CONSTANT.loadingType.two)
                return AppSystem.elem.$loadingUi2.classList.remove('d-none')
            if (loadingType === AppSystem.CONSTANT.loadingType.three)
                return AppSystem.elem.$loadingUi3.classList.remove('d-none')
        },
        hiddenLoadingUi: function (loadingType = AppSystem.CONSTANT.loadingType.one) {
            if (loadingType === AppSystem.CONSTANT.loadingType.one)
                return AppSystem.elem.$loadingUi.classList.add('d-none')
            if (loadingType === AppSystem.CONSTANT.loadingType.two)
                return AppSystem.elem.$loadingUi2.classList.add('d-none')
            if (loadingType === AppSystem.CONSTANT.loadingType.three)
                return AppSystem.elem.$loadingUi3.classList.add('d-none')
        }
    },
    handleComp: {
        CONSTANT: {
            prefix: 'id-',
        },
        fun: {
            getConstructId: function (id, suffix) {
                return `${AppSystem.handleComp.CONSTANT.prefix}${id}${suffix}`
            }
        },
        alert: {
            alert: {
                CONSTANT: {
                    alertSuffix: 'Alert',
                    titleSuffix: 'titleAlert',
                    contentSuffix: 'contentAlert'
                },
                onlyShow: function ({id = ''}) {
                    const $alert = document.getElementById(AppSystem.handleComp.fun.getConstructId(id, AppSystem.handleComp.alert.alert.CONSTANT.alertSuffix))
                    $alert.classList.remove('d-none')
                },
                show: function (data = {}) {
                    const {id = '', title = '', content = '', typeFeature = AppSystem.CONSTANT.typeFeature.info, withTitleDefault = true} = data

                    const $alert = document.getElementById(AppSystem.handleComp.fun.getConstructId(id, AppSystem.handleComp.alert.alert.CONSTANT.alertSuffix))
                    const $title = document.getElementById(AppSystem.handleComp.fun.getConstructId(id, AppSystem.handleComp.alert.alert.CONSTANT.titleSuffix))
                    const $content = document.getElementById(AppSystem.handleComp.fun.getConstructId(id, AppSystem.handleComp.alert.alert.CONSTANT.contentSuffix))

                    let titleDefault = ''

                    if (typeFeature === AppSystem.CONSTANT.typeFeature.primary) {
                        titleDefault = 'Informacion'
                    } else if (typeFeature === AppSystem.CONSTANT.typeFeature.secondary) {
                        titleDefault = 'Informacion'
                    } else if (typeFeature === AppSystem.CONSTANT.typeFeature.success) {
                        titleDefault = 'Exitoso'
                    } else if (typeFeature === AppSystem.CONSTANT.typeFeature.danger) {
                        titleDefault = 'Error'
                    } else if (typeFeature === AppSystem.CONSTANT.typeFeature.warning) {
                        titleDefault = 'Alerta'
                    } else if (typeFeature === AppSystem.CONSTANT.typeFeature.info) {
                        titleDefault = 'Informacion'
                    } else if (typeFeature === AppSystem.CONSTANT.typeFeature.light) {
                        titleDefault = 'Informacion'
                    } else if (typeFeature === AppSystem.CONSTANT.typeFeature.dark) {
                        titleDefault = 'Informacion'
                    }

                    if (title.length) {
                        $title.innerHTML = title
                    } else {
                        if (withTitleDefault)
                            $title.innerHTML = titleDefault
                    }

                    $content.innerHTML = content
                    $alert.classList.remove('d-none')
                },
                hidden: function ({id = ''}) {
                    const $alert = document.getElementById(AppSystem.handleComp.fun.getConstructId(id, AppSystem.handleComp.alert.alert.CONSTANT.alertSuffix))
                    $alert.classList.add('d-none')
                }
            }
        },
        card: {
            cardWidgetValue: {
                CONSTANT: {
                    valueSuffix: 'CardWidgetValue',
                },
                changeValue: function (data = {}) {
                    const {id = '', value = ''} = data
                    const $h3 = document.getElementById(AppSystem.handleComp.fun.getConstructId(id, AppSystem.handleComp.card.cardWidgetValue.CONSTANT.valueSuffix))
                    $h3.innerHTML = value
                }
            },
        },
    }
}