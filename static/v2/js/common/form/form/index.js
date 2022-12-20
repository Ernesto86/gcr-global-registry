'use strict';

const FormCommon = {
    CONSTANT: {},
    fun: {
        getErrorList: (errors) => {

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
    }
}