/**
 * Created by EL on 19/4/2020.
 */
(function (b) {
    b.toast = function (a, h, g, l, k) {
        b("#toast-container").length || (b("body").prepend('<div id="toast-container" aria-live="polite" aria-atomic="true"></div>'), b("#toast-container").append('<div id="toast-wrapper"></div>'));
        var c = "", d = "", e = "text-muted", f = "", m = "object" === typeof a ? a.title || "" : a || "Notice!";
        h = "object" === typeof a ? a.subtitle || "" : h || "";
        g = "object" === typeof a ? a.content || "" : g || "";
        k = "object" === typeof a ? a.delay || 3E3 : k || 3E3;
        switch ("object" === typeof a ? a.type || "" : l || "info") {
            case "info":
                c = "bg-info";
                f = e = d = "text-white";
                break;
            case "success":
                c = "bg-success";
                f = e = d = "text-white";
                break;
            case "warning":
            case "warn":
                c = "bg-warning";
                f = e = d = "text-white";
                break;
            case "error":
            case "danger":
                c = "bg-danger", f = e = d = "text-white"
        }
        a = '<div class="toast" role="alert" aria-live="assertive" aria-atomic="true" data-delay="' + k + '">' + ('<div class="toast-header ' + c + " " + d + '">') + ('<strong class="mr-auto">' + m + "</strong>");
        a += '<small class="' + e + '">' + h + "</small>";
        a += '<button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close">';
        a += '<span aria-hidden="true" class="' + f + '">&times;</span>';
        a += "</button>";
        a += "</div>";
        "" !== g && (a += '<div class="toast-body"><h5>', a += g, a += "</h5></div>");
        a += "</div>";
        b("#toast-wrapper").append(a);
        b("#toast-wrapper .toast:last").toast("show")
    }
})(jQuery);

function fnToast(ms,tipo,time) {
    var TYPES = ['', 'warning', 'success', 'error','info'];
    $.toast({
        title: 'Mensaje de SAyA.',
        //subtitle: datenow,
        content: ms,
        type: TYPES[tipo||2],
        delay: time || 5000
    });
}
