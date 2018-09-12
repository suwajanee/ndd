$(function () {

    window.setTimeout(function() {
        $(".alert").fadeTo(500, 0).slideUp(500, function(){
            $(this).remove(); 
        });
    }, 2000);
    
    
        $(document).on('click', '.add-more', function(e) {
            e.preventDefault();
            var controlForm = $('.control:first'),
            currentEntry = $(this).parents('.entry:first'),
            newEntry = $(currentEntry.clone()).appendTo(controlForm);
            newEntry.find('input').val('');
            controlForm.find('.entry:not(:first) .add-more')
            .removeClass('add-more').addClass('remove')
            .removeClass('btn-success').addClass('btn-danger')
            .html('<span><i class="fa fa-minus"></i></span>');
        }).on('click', '.remove', function(e) {
            $(this).parents('.entry:first').remove();
            e.preventDefault();
            return false;
        });
    

});