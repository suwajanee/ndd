$(document).ready(function () {

    window.setTimeout(function () {
        $(".alert").fadeTo(500, 0).slideUp(500, function () {
            $(this).remove();
        });
    }, 2000);

    $('.no-collapsable').on('click', function (e) {
        e.stopPropagation();
    });

    $("#table-cont").css({
        top: $("#filter-date").offset().top + 60
    })

    $(".class-collapse").css({
        width: $(window).width()
    })

    $('select[name="filter_by"]').change(function () {
        if ($(this).val() == "month") {
            $('input#id_date').attr("type", "month")
        } else {
            $('input#id_date').attr("type", "date")
        }

    });

    $("button.action").click(function () {

        if ($("input.check:checked").length != 0) {
            $("input.check:checked").each(function () {

                var input = $("<input>")
                    .attr("type", "hidden")
                    .attr("name", "check").val($(this).val());
                $('form#action').append($(input));
            });
        } else {
            alert("เลือกงานที่ต้องการ");
            return false;
        }

        var action = $('select[name="action"]').val();

        if (action == 'delete') {
            if (confirm('Are you sure?')) {
                $('form#action').attr("action", "{% url 'agent-transport-delete-multiple' %}");
                $('form#action').submit();
            }
        }
        return false;

    });

    $("#checkAll").click(function () {
        $('input.check:checkbox').not(this).prop('checked', this.checked);
    });

});


