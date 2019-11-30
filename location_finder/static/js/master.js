$(document).ready(function(){
    $("#one").on('click', function(){
        //e.preventDefault();
        $('#one').attr("disabled", true);
        $('#two').attr("disabled", false);
    });

    $('#two').on('click', function (){
        var d = $('#two').attr('downloadable');
        if (d === 'false') {
            $('#two').attr('downloadable', 'true');
            $('#spinner').toggleClass('d-none');
            $('#btn-text').text("Processing...");
            var fname = $('#two').attr('filename');
            $.ajax({
                url: 'process/',
                data: {'csv_file': fname},
                success: function (response, status, xhr) {
                    $('#spinner').toggleClass('d-none');
                    $('#btn-text').text("Upload another file");

                    text=response
                    var disposition = xhr.getResponseHeader('Content-Disposition');
                    if (disposition && disposition.indexOf('attachment') !== -1) {
                        var filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
                        var matches = filenameRegex.exec(disposition);
                        if (matches != null && matches[1]) {
                            filename = matches[1].replace(/['"]/g, '');
                            }
                        }
                    download(filename, text);
                    $('#btn-text').text("Upload another file");
                    }
                })

            } else {
                
                $('#one').attr("disabled", false);
                $('#two').attr("disabled", true);
                $('#btn-text').text("Start Processing");
            }
    });
});

function download(filename, text) {
  var element = document.createElement('a');
  element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
  element.setAttribute('download', filename);

  element.style.display = 'none';
  document.body.appendChild(element);

  element.click();

  document.body.removeChild(element);
}
