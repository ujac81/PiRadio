# application.coffee -- document ready function - loaded last in base.pug

# Run on document.ready event.
$ ->
    PiRadio.init_variables()
    # disable caching for AJAX

    PiRadio.ajax_setup()


    PiRadio.do_ajax
        data:
            'action': 'cmd'
            'cmd': status
        success: (data) ->
            PiRadio.handle_status data
            return

    $('i.footer-button').off 'click'
    $('i.footer-button').on 'click', ->
        PiRadio.do_ajax
            data:
                'action': 'cmd'
                'cmd': $(this)[0].dataset['item']
            success: (data) ->
                PiRadio.handle_status data
                return
        return

    console.log('Ready')

    return



