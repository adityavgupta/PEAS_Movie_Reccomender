$(function() {
    $('.btnReview').click(function() {
        const button = $(this)
        const user_name = button.data('source')
        const showname = button.data('content')
        console.log(user_name,showname)
        $.ajax({
            url: '/review',
            type: 'POST',
            data: {
                'user_name': user_name,
                'showname': showname,
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