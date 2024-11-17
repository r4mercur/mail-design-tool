$(document).ready(function() {
    let zIndex = 0;

    $('.element').draggable({
        helper: 'clone',
        revert: 'invalid',
    })

    $('#template-area').droppable({
        accept: '.element',
        drop: function (event, ui) {
            const elementType = ui.draggable.data('type');
            let newElement;

            switch (elementType) {
                case 'textbox':
                    newElement = $('<div class="textbox" contenteditable="true" data-type="textbox">Text here</div>');
                    break;
                case 'button':
                    newElement = $('<button class="button" data-type="button">Button</button>');
                    break;
                case 'image':
                    newElement = $('<img src="https://via.placeholder.com/150" class="image" data-type="image" />');
                    break;
            }


            newElement.css({
                position: 'absolute',
                top: ui.offset.top - $(this).offset().top,
                left: ui.offset.left - $(this).offset().left,
                zIndex: zIndex++
            }).draggable({
                containment: '#template-area',
                cursor: 'move'
            }).resizable();


            $(this).append(newElement);
        }
    })

    $('#save').click(function() {
        const elements = [];

        $('#template-area').children().each(function() {
           const $el = $(this);
           const elType = $el.attr('data-type');
           const position = {
               top: $el.css('top'),
               left: $el.css('left')
           };
           const zIndex = $el.css('z-index');

           let elementData = {
                type: elType,
                position: position,
                zIndex: zIndex
              };

           if (elType === 'textbox') {
               elementData.content = $el.html();
           } else if (elType === 'image') {
               elementData.src = $el.attr('src');
           } else if(elType === 'button') {
               elementData.content = $el.text();
           }

           elements.push(elementData);
        });

        const jsonData = JSON.stringify(elements);
        console.log(jsonData);

        // here make the save request to the server with ajax

        // redirect to /mail overview
        // window.location.href = '/mail/list';
    });
})