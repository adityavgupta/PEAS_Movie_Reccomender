$('#btnSearchG').click(function() {
    //console.log('smthing')
    $.ajax({
        url: '/searchGallery',
        data: {"form":$('form').serialize()},
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