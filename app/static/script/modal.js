$(function() {
    $('#goSignUp').click(function() {
        console.log('your message');
        $.ajax({
            url: '/renderSignUp',
            // data: $('form').serialize(),
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

$(function() {
    $('#goSignIn').click(function() {
        $.ajax({
            url: '/renderSignIn',
            // data: $('form').serialize(),
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