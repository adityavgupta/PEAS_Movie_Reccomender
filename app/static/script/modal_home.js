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

    $('#btnSignOut').click(function() {
        console.log('smthing')
        $.ajax({
            url: '/signOut',
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

    $('#btnDeleteUser').click(function(){
        const button = $(this)
        const user_name = button.data('source')
        
        console.log(user_name)
        $.ajax({
            url: '/deleteUser',
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

    $('#btnGallery').click(function(){
        //console.log(user_name)
        $.ajax({
            url: '/getGallery',
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

    $('#btnGoHome').click(function() {
        $.ajax({
            url: '/goHome',
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
});