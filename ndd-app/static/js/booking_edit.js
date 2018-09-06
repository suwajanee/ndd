$(function () {
    window.setTimeout(function () {
        $(".save-msg").fadeTo(500, 0).slideUp(500, function () {
            $(this).remove();
        });
    }, 1500);

    $(function () {
        $("#table-cont").css({ top: $("#filter-date").offset().top + 60 })

        $('select[name="filter_by"]').change(function () {
            if ($(this).val() == "month") {
                $('input#id_date').attr("type", "month")
            }
            else {
                $('input#id_date').attr("type", "date")
            }

        });
    });

});