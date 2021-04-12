$(function() {
    $('#btnSearch').click(function() {
        // console.log('smthing')
        $.ajax({
            url: '/search',
            data: {"name":$('#home_name').html(), "form":$('form').serialize()},
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

    $('#btnPaulQuery').click(function() {
        // console.log('smthing')
        $.ajax({
            url: '/paulQuery',
            type: 'GET',
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

    $('#btnRenderReviewPage').click(function() {
        $.ajax({
            url: '/renderSearchReview',
            type: 'POST',
            dataType: 'text',
            data: {"name":$('#home_name').html()},
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