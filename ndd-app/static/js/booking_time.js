$(function () {
    window.setTimeout(function () {
        $(".save-msg").fadeTo(500, 0).slideUp(500, function () {
            $(this).remove();
        });
    }, 1500);

    $(function () {
        $("#table-cont").css({ top: $("#filter-date").offset().top + 60 })
    });


    $(function () {
        $("button#print").click(function () {

            $("input.pk").each(function () {

                $('form#PrintTime').append($(this));
            });

            $('form#PrintTime').submit();
        });
    });

});