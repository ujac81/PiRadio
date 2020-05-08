# application.coffee -- document ready function - loaded last in base.pug

# Run on document.ready event.
$ ->
    PiRadio.init_variables()
    # disable caching for AJAX

    PiRadio.ajax_setup()

    # hide volume overlay
    $('.vol-over').hide()


    # Load initial status
    PiRadio.do_ajax
        data:
            'action': 'cmd'
            'cmd': 'status'
        success: (data) ->
            PiRadio.handle_status data
            return

    # Actions on player buttons
    $('i.mpc-button').off 'click'
    $('i.mpc-button').on 'click', ->
        PiRadio.do_ajax
            data:
                'action': 'cmd'
                'cmd': $(this)[0].dataset['item']
            success: (data) ->
                PiRadio.handle_status data
                return
        return

    # Actions on volume button
    $('i.vol-button').off 'click'
    $('i.vol-button').on 'click', ->
        $('.vol-over').toggle()
        if $('.vol-over').is(':visible')
            # resize sliders to max height
            h = $('.vol-over').height() - $('.row.vol-head').height() -
                $('.row.vol-sliders').height() + $('.vol-slider').height()
            $('.vol-slider').height(h)
            # get volume
            PiRadio.do_ajax
                data:
                    'action': 'mixer'
                    'cmd': 'vol-status'
                success: (data) ->
                    for key, value of data
                        $('.vol-slider-fill[data-mixer='+key+']').css('top', (100.0-value)+'%')
            return

        return


    # Actions on volume slider
    $('.vol-slider').on 'click', (event) ->
        return if PiRadio.on_slider_change
        PiRadio.on_slider_change = true
        y_off = $(this).offset().top
        pct_inv = ((event.pageY-y_off)/$(this).height()*100.0)
        pct = parseInt(100.0-pct_inv)
        id = $(this).data('mixer')

        PiRadio.do_ajax
            data:
                'action': 'mixer'
                'cmd': 'vol-set'
                channel: id
                value: pct
            success: (data) ->
                $('.vol-slider-fill[data-mixer='+id+']').css('top', (100.0-pct)+'%')
                PiRadio.on_slider_change = false
                return
        return

    return



