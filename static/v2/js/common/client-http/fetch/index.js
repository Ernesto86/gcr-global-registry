'use strict';


class SuccessResponse {
    static KIND_STATIC = 'success'

    constructor(code = 0, message = "", data = {}) {
        this.kind = SuccessResponse.KIND_STATIC
        this.code = code
        this.message = message
        this.data = data
    }
}

class ErrorResponse {
    static KIND_STATIC = 'error'

    constructor(code = 0, message = "", data = {}) {
        this.kind = ErrorResponse.KIND_STATIC
        this.code = code
        this.message = message
        this.data = data
    }
}


const ClientHttpFetch = {
    CONSTANT: {
        verboseMethod: {
            POST: Symbol('POST'),
            GET: Symbol('GET'),
            PUT: Symbol('PUT'),
            PATH: Symbol('PATH'),
            DELETE: Symbol('DELETE'),
        },
        statusCode: {
            ErrorNetwork: 0,
            ErrorUnknown: 50012,
            // 1xx informational response
            Continue: 100,
            SwitchingProtocols: 101,
            ProcessingWebDAV: 102,
            EarlyHints: 103,
            // 2xx success
            OK: 200,
            Created: 201,
            Accepted: 202,
            NonAuthoritativeInformation: 203,
            NoContent: 204,
            ResetContent: 205,
            PartialContent: 206,
            MultiStatus: 207,
            AlreadyReported: 208,
            IMUsed: 226,
            // 3xx redirection
            MultipleChoices: 300,
            MovedPermanently: 301,
            FoundPreviously: 302,
            SeeOther: 303,
            NotModified: 304,
            UseProxy: 305,
            SwitchProxy: 306,
            TemporaryRedirect: 307,
            PermanentRedirect: 308,
            // 4xx client errors
            BadRequest: 400,
            Unauthorized: 401,
            PaymentRequired: 402,
            Forbidden: 403,
            NotFound: 404,
            MethodNotAllowed: 405,
            NotAcceptable: 406,
            ProxyAuthenticationRequired: 407,
            RequestTimeout: 408,
            Conflict: 409,
            Gone: 410,
            LengthRequired: 411,
            PreconditionFailed: 412,
            PayloadTooLarge: 413,
            URITooLong: 414,
            UnsupportedMediaType: 415,
            RangeNotSatisfiable: 416,
            ExpectationFailed: 417,
            ImATeapot: 418,
            MisdirectedRequest: 421,
            UnprocessableEntity: 422,
            LockedWebDAV: 423,
            FailedDependency: 424,
            TooEarly: 425,
            UpgradeRequired: 426,
            PreconditionRequired: 428,
            TooManyRequests: 429,
            RequestHeaderFieldsTooLarge: 431,
            UnavailableForLegalReasons: 451,
            // 5xx server errors
            InternalServerError: 500,
            NotImplemented: 501,
            BadGateway: 502,
            ServiceUnavailable: 503,
            GatewayTimeout: 504,
            HTTPVersionNotSupported: 505,
            VariantAlsoNegotiates: 506,
            InsufficientStorage: 507,
            LoopDetected: 508,
            NotExtended: 510,
            NetworkAuthenticationRequired: 511,


        }
    },
    fun: {
        isNoConnectionNetwork: (value) => false,
        isInformationalResponses: (value) => value >= 100 && value <= 199,
        isSuccessfulResponses: (value) => value >= 200 && value <= 299,
        isRedirectionMessages: (value) => value >= 300 && value <= 399,
        isClientErrorResponses: (value) => value >= 400 && value <= 499,
        isServerErrorResponses: (value) => value >= 500 && value <= 599,
        isErrorNetwork: (value) => value === this.ErrorNetwork,
        isErrorUnknown: (value) => value === this.ErrorUnknown,
        isErrorNoVerbose: function (value) {
            if (this.isErrorNetwork(value)) return true

            if (this.isErrorUnknown(value)) return true

            return false
        }
    },
    exec: async (url, data, configExtra = {}) => {
        const {
            method = ClientHttpFetch.CONSTANT.verboseMethod.POST.description,
        } = configExtra

        let options = {
            method,
            credentials: 'include',
            headers: {
                'Accept': 'application/json',
                'X-CSRFToken': Cookies.get('csrftoken')
            }
        }

        try {
            if (method === ClientHttpFetch.CONSTANT.verboseMethod.GET.description)
                url += '?' + (new URLSearchParams(data)).toString()
            else
                options.body = data instanceof FormData ? data : JSON.stringify(data)

            const response = await fetch(url, options)

            const status = response.status

            if (!response.ok)
                throw response

            const responseJson = await response.json()

            return new SuccessResponse(status, responseJson.message, responseJson)

        } catch (error) {
            c("Error http client fetch: ", error)

            try {
                if (error instanceof Response) {

                    let responseJson = {}
                    let message = ""

                    try {
                        responseJson = await error.json()
                        message = responseJson.message
                    } catch (errorParse) {
                        message = error.statusText
                    }

                    // if (error.status === ClientHttpFetch.CONSTANT.statusCode.Forbidden) {
                    //     if (message)
                    //         message = "Tiene prohibición para realizar la siguiente accion."
                    // }


                    c("data error response: ", responseJson)

                    return new ErrorResponse(error.status, message, responseJson)

                } else {

                    return new ErrorResponse(ClientHttpFetch.CONSTANT.statusCode.ErrorNetwork, "Error de red", {})

                }

            } catch (errorUnknown) {

                return new ErrorResponse(ClientHttpFetch.CONSTANT.statusCode.ErrorUnknown, "Error desconocido", {})

            }
        }
    },
}

