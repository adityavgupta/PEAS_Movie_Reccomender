$(function() {
    $('#goSignUp').click(function() {
        console.log('your message');
        $.ajax({
            url: '/renderSignUp',
            // data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                //console.log(response);
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
    $('#goSignIn').click(function() {
        console.log('your message');
        $.ajax({
            url: '/renderSignIn',
            // data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                ///console.log(response);
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