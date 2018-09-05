$(function() {
    window.setTimeout(function() {
        $(".alert").fadeTo(500, 0).slideUp(500, function(){
            $(this).remove(); 
        });
    }, 2000);

    $('.no-collapsable').on('click', function (e) {
        e.stopPropagation();
    });

    $("#table-cont").css({top: $("#filter-date").offset().top + 60 });

    $(".class-collapse").css({width: $( window ).width()});

    $("#checkAll").click(function(){
        $('input.check:checkbox').not(this).prop('checked', this.checked);
    });

    

    $('select[name="filter_by"]').change(function() {
        if($(this).val() == "month"){
            $('input#id_date').attr("type", "month")
        }
        else {
            $('input#id_date').attr("type", "date")
        }
        
    });

});