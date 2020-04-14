# base.coffee -- functions for base layout (footer)

PiRadio.handle_status = (status) ->
    if status.status
        console.log 'TRUE'
    else
        console.log 'FALSE'

    if status.status
        if status.state == 'playing'
            $('i.footer-button[data-button="play"]').hide()
            $('i.footer-button[data-button="pause"]').show()
        else
            $('i.footer-button[data-button="pause"]').hide()
            $('i.footer-button[data-button="play"]').show()
    else
        $('i.footer-button[data-button="pause"]').hide()
        $('i.footer-button[data-button="play"]').show()


    return