# ajax.coffee -- AJAX related stuff

# Disable caching for AJAX -- required for safari browser
# TODO: safari still not working....
PiRadio.ajax_setup = ->

    $.ajaxSetup
        type: 'POST',
        headers:
            "cache-control": "no-cache"

    $.ajaxSetup
        type: 'GET',
        headers:
            "cache-control": "no-cache"

    return


# Perform AJAX post request
PiRadio.do_ajax = (req) ->
    data = req.data or {}
    data.timeStamp = new Date().getTime()  # avoid caching
    data.csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken')[0].value
    $.ajax
        url: '/main/ajax/cmd/'
        data: data
        method: if req.method then req.method else 'POST'
        dataType: 'json'
        success: (data) ->
            req.success(data) if req.success
            return
        error: (jqXHR) ->
            # Call error function if given, otherwise indicate AJAX error
            if req.error
                req.error()
            else
                console.log 'AJAX ERROR'
                console.log jqXHR
            return
    return