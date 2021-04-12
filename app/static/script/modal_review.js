$(function() {
    $('#btnSubmitReview').click(function() {
        const button = $(this)
        const user_name = button.data('source')
        const title_id = button.data('content')
        const type = button.data('type')
        console.log(user_name)
        console.log(title_id)
        // console.log($('#inputScore').val())
        $.ajax({
            url: '/submitReview',
            type: 'POST',
            data: {
                'user_name': user_name,
                'title_id': title_id,
                'type': type,
                'rating': $('#inputScore').val(),
                'review': $('#inputReview').val(),
            },
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