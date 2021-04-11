$(function() {
    $('#btnSubmit').click(function() {
        console.log("j");
        $.ajax({
            url: '/watched',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});