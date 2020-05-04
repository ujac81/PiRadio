# base.coffee -- functions for base layout (footer)

PiRadio.handle_status = (status) ->

    # remove the current class from play button
    button = $('i.play-button')
    button.removeClass (index, currentClass) ->
        for item in currentClass.split(/\s+/)
            if item.startsWith 'fa-'
                console.log item
                return item
        return ''
    if status.state == 'playing'
        button.addClass 'fa-pause'
    else
        button.addClass 'fa-play'

    return