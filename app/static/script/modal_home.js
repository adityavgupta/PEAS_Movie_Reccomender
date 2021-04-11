$(function() {
    $('#btnSearch').click(function() {
        console.log('smthing')
        $.ajax({
            url: '/search',
            data: $('form').serialize(),
            type: 'POST',
            dataType: 'text',
            success: function(response) {
                console.log(response);
                
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});