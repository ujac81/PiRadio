# application.coffee -- document ready function - loaded last in base.pug

# Run on document.ready event.
$ ->
    PiRadio.init_variables()
    # disable caching for AJAX

    PiRadio.ajax_setup()



    # footer-items:
    $('i.footer-button[data-item="pause"]').hide()

    $('i.footer-button').off 'click'
    $('i.footer-button').on 'click', ->
        PiRadio.do_ajax
            data:
                'action': 'cmd'
                'cmd': $(this)[0].dataset['item']
            success: (data) ->
                console.log data
                return
        return

    console.log('Ready')

    return



