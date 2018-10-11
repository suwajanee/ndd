$(function () {

    $("#customerList").css({top: $("#search-box").offset().top + 55 });

    $("#myInput").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#myList a").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });

    $("button.btn-cancel-shipper").click(function(){
        if (confirm('Are you sure?')){
            $(this).next().submit();
        }
        return false;
    });

    $("button.btn-cancel-customer").click(function(){
        if (confirm('Are you sure?')){
            $(this).next().submit();
        }
        return false;
    });

    $(document).on('click', '.add-more', function (e) {
        e.preventDefault();
        var controlForm = $('.control:first'),
            currentEntry = $(this).parents('.entry:first'),
            newEntry = $(currentEntry.clone()).appendTo(controlForm);
        newEntry.find('input').val('');
        newEntry.find('textarea').val('');
        controlForm.find('.entry:not(:first) .add-more')
            .removeClass('add-more').addClass('remove')
            .removeClass('btn-outline-success').addClass('btn-outline-danger')
            .html('<span><i class="fa fa-minus"></i></span>');
    }).on('click', '.remove', function (e) {
        $(this).parents('.entry:first').remove();
        e.preventDefault();
        return false;
    });

});