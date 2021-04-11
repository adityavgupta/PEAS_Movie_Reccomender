$(function() {
    $('.btnReview').click(function() {
        $.ajax({
            url: '/signIn',
            data: {"name":$('#home_name').html(), "form":$('form').serialize()},
            type: 'POST',
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
});

function dres(x) {
    console.log('dres');
    document.open();
    document.write(`${x}`);
    document.close();
}