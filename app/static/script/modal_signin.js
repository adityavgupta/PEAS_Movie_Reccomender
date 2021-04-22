$(function() {
    $('#btnSignIn').click(function() {
        $.ajax({
            url: '/signIn',
            data: $('form').serialize(),
            type: 'POST',
            dataType: 'text',
            success: function(response) {
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
