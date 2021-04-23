$(function() {
    $('#btnReviewSearch').click(function() {
        const button = $(this)
        const user_name = button.data('uname')
        $.ajax({
            url: '/searchReview',
            data: {"name":user_name, "form":$('form').serialize()},
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

    $('.btnUpdateReview').click(function() {
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
                'update_type': 'Update'
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

    $('.btnDeleteReview').click(function() {
        const button = $(this)
        const user_name = button.data('source')
        const showname = button.data('content')
        const title_id = button.data('titleid')
        const type = button.data('type')
        console.log(user_name,showname, title_id)
        $.ajax({
            url: '/deleteReview',
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
    })
});