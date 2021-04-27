$(function() {
    $('#btnSearchG').click(function() {
        //console.log('smthing')
        $.ajax({
            url: '/searchGallery',
            data: {"form":$('form').serialize()},
            type: 'POST',
            dataType: 'text',
            success: function(response) {
                console.log(response);
                document.open();
                document.write(`${response}`);
                document.close();
                
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

    $('.btnDeleteS').click(function() {
        //console.log('smthing')
        const button = $(this)
        const user_name = button.data('source')
        const showname = button.data('content')
        const title_id = button.data('titleid')
        const type = button.data('type')
        const section = button.data('section')
        console.log(user_name,showname, title_id,type,section)
        $.ajax({
            url: '/delFromGallery',
            type: 'POST',
            data: {
                'user_name': user_name,
                'showname': showname,
                'title_id':title_id,
                'type': type,
                'section': section,
            },
            dataType: 'text',
            success: function(response) {
                console.log(response);
                // document.open();
                // document.write(`${response}`);
                // document.close();
                
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});