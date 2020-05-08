# base.coffee -- functions for base layout (footer)

PiRadio.handle_status = (status) ->

    # remove the current class from play button
    button = $('i.play-button')
    button.removeClass (index, currentClass) ->
        for item in currentClass.split(/\s+/)
            if item.startsWith 'fa-'
                return item
        return ''
    if status.state == 'playing'
        button.addClass 'fa-pause'
    else
        button.addClass 'fa-play'

    # set marquee text and modify animation duration
    marquee = $('span#marquee')
    if marquee.length == 1
        if 'marquee' of status
            marquee.html(status.marquee)
        marquee.css 'animation-duration', marquee.html().length / 6 +"s"

    return