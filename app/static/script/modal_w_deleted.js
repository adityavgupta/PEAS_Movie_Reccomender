$(function() {
    $('#btnDelete').click(function() {
        console.log("ugh");
        $.ajax({
            url: '/w_deleted',
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