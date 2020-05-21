


PiRadio.init_playlist = ->

    $('table.tb-playlist > tbody > tr.selectable > td > table > tbody > tr > td.selectable').on 'click', ->
        $(this).parent().parent().parent().parent().parent().toggleClass 'selected'
        #console.log $(this)
        #pos = $(this).parent().parent().parent().parent().parent().data('id')
        return


    $('td.plaction').on 'click', ->
        PiRadio.action_item = $(this).parent().parent().parent().parent().parent().data('id')
        console.log PiRadio.action_item
        return


    return

PiRadio.view_functions["music-playlist"] = PiRadio.init_playlist