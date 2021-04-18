$(function() {
    $('#btnSubmit').click(function() {
        console.log("j");
        $.ajax({
            url: '/insertwatched',
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

    $('#btnUpdate').click(function() {
        $.ajax({
            url: '/updatewatched',
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

    $('#btnLookup').click(function() {
        console.log('Look it up')
        $.ajax({
            url: '/searchwatched',
            data: $('form').serialize(),
            type: 'POST',
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