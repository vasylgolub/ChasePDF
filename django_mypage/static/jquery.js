$(function () {
    $(':checkbox').change(function () {

        if ($(this).is(':checked')) {
            $('#remove_btn').attr('class', 'button-83 btn btn-primary btn-sm');
        } else {
            $('#remove_btn').attr('class', 'button-83 btn btn-primary btn-sm disabled');
        }

    });
});


$(function () {
    $("#checkAll").click(function () {
        $('input:checkbox').not(this).prop('checked', this.checked);
    });
});


// when we choose a file to upload, this gets triggered
$(function () {
    // $('#submit_file').addClass('disabled');
    $(".fileToUpload").on('change', function () {
        // $("#submit_file").addClass("spot");
        $("#submit_file").removeClass("disabled");
    });
});


// display loading icon when the form is submitted
$(function() {
  $(".fileToUpload").submit(function(event) {
        $('#submit_text').remove();
        $('#submit_file').prop('disabled', true);

       $('#submit_file').html(
        `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...`
      );
  });
});



// $(function(){
//     // $(".description_main_table").change(function(){
//     //     console.log("ciaoo")
//     // });
//     var all = $(".highlightable").map(function()
//     {
//         return this.innerHTML;
//     }).get();
//     console.log('ciao')
//     console.log(all);
// });


$(function () {
    $("#Add").click(function () {
        var highlighted_elements = $(".highlightable");
        var array = [];

        $(highlighted_elements).each(function () {
            var val = $(this).attr("value");
            if (val) {  // If value is empty that means we need to pass the description instead
                array.push(val);
            } else {
                array.push($(this).text());  // pass the description (text in between the tags)
            }


        });

        array = JSON.stringify(array);
        $("#Add").attr('value', array);
    });
});


// Typed key will be searched in each text in the list and highlighted if matched
$(function () {
        $("#kw").keyup(function () {
            typed_text = $(this).val().toLowerCase();

            $('#tr_transactions #description').each(function () {
                var match = $(this).html().toLowerCase().indexOf(typed_text);
                if (match > -1) {
                    $('table').removeClass('table-striped');
                    $(this).addClass("highlightable");
                    $('#Add').removeClass('disabled');
                } else {
                    $(this).removeClass("highlightable");

                }
            });
            if ($(".highlightable")[0] === undefined) {
                $('#Add').addClass('disabled');
            }
             if (typed_text === "") {
                    $('.highlightable').removeClass("highlightable");
                    $('table').addClass('table-striped');
                    $('#Add').addClass('disabled');
                }


        })
    }
);