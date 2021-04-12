$(function() {
    $('.btnReview').click(function() {
        const button = $(this)
        const user_name = button.data('source')
        const showname = button.data('content')
        const title_id = button.data('titleid')
        const type = button.data('type')
        console.log(user_name,showname, title_id)
        $.ajax({
            url: '/review',
            type: 'POST',
            data: {
                'user_name': user_name,
                'showname': showname,
                'title_id':title_id,
                'type': type
            },
            dataType: 'text',
            success: function(response) {
                console.log(response);
                dres(response);
                
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});

function dres(x) {
    // console.log('dres');
    document.open();
    document.write(`${x}`);
    document.close();
}