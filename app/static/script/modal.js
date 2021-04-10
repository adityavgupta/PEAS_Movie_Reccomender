$(function() {
    $('#goSignUp').click(function() {
        $.ajax({
            url: '/renderSignUp',
            // data: $('form').serialize(),
            type: 'GET',
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
            type: 'GET',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});