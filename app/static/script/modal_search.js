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
                'type': type,
                'update_type': 'Create'
            },
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
});

$(function() {
    $('.btnImpression').click(function() {
        const button = $(this)
        const user_name = button.data('source')
        const showname = button.data('content')
        const title_id = button.data('titleid')
        const type = button.data('type')
        const impression = button.data('impression')
        console.log(user_name,showname, title_id)
        $.ajax({
            url: '/leaveImpression',
            type: 'POST',
            data: {
                'user_name': user_name,
                'showname': showname,
                'title_id':title_id,
                'type': type,
                'impression':impression,
                'transaction_type': 'Update'
            },
            dataType: 'text',
            success: function(response) {
                console.log(response);
                //dres(response);
                
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});
