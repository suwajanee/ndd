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

});