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
        type_feature: {
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
        alert: {
            CONSTANT: {
                alertSuffix: 'Alert',
                titleSuffix: 'titleAlert',
                contentSuffix: 'contentAlert'
            },
            getConstructId: function (id, suffix) {
                return `${AppSystem.handleComp.CONSTANT.prefix}${id}${suffix}`
            },
            onlyShow: function ({id = ''}) {
                const $alert = document.getElementById(this.getConstructId(id, this.CONSTANT.alertSuffix))
                $alert.classList.remove('d-none')
            },
            show: function (data = {}) {
                const {id = '', title = '', content = '', type_feature = AppSystem.CONSTANT.type_feature.info, withTitleDefault = true} = data

                const $alert = document.getElementById(this.getConstructId(id, this.CONSTANT.alertSuffix))
                const $title = document.getElementById(this.getConstructId(id, this.CONSTANT.titleSuffix))
                const $content = document.getElementById(this.getConstructId(id, this.CONSTANT.contentSuffix))

                let titleDefault = ''

                if (type_feature === AppSystem.CONSTANT.type_feature.primary) {
                    titleDefault = 'Informacion'
                } else if (type_feature === AppSystem.CONSTANT.type_feature.secondary) {
                    titleDefault = 'Informacion'
                } else if (type_feature === AppSystem.CONSTANT.type_feature.success) {
                    titleDefault = 'Exitoso'
                } else if (type_feature === AppSystem.CONSTANT.type_feature.danger) {
                    titleDefault = 'Error'
                } else if (type_feature === AppSystem.CONSTANT.type_feature.warning) {
                    titleDefault = 'Alerta'
                } else if (type_feature === AppSystem.CONSTANT.type_feature.info) {
                    titleDefault = 'Informacion'
                } else if (type_feature === AppSystem.CONSTANT.type_feature.light) {
                    titleDefault = 'Informacion'
                } else if (type_feature === AppSystem.CONSTANT.type_feature.dark) {
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
                const $alert = document.getElementById(this.getConstructId(id, this.CONSTANT.alertSuffix))
                $alert.classList.add('d-none')
            }
        }
    }
}