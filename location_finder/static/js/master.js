$(document).ready(function(){
    $("#one").click(function(){
        //e.preventDefault();
        $('#one').attr("disabled", true);
        $('#two').attr("disabled", false);
    });

    $('#two').on('click', function (file_obj){
        $('#spinner').toggleClass('d-none');
        $('#btn-text').text("Processing...");
        $.post('process/', {'csv_file': file_obj},

    );
    });
});
