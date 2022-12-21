$(
  function(){
    $("#checkAll").click(function(){$('input:checkbox').not(this).prop('checked', this.checked);});
  }

);


$(function(){
        $("#Add").click(function(){
                var highlighted_elements = $(".highlightable");
                var array = [];

                $(highlighted_elements).each( function () {
                    var val = $(this).attr("value");
                    if (val){  // If value is empty that means we need to pass the description instead
                        array.push(val);
                    } else {
                        array.push($(this).text());  // pass the description (text in between the tags)
                    }


                });

                array = JSON.stringify(array);
                $("#Add").attr('value',  array);
            });
    });


$(function(){
     $("#kw").keyup(
          function(){
              typed_text = $(this).val();

                $('#tr_transactions #description').each(function() {
                  var match = $(this).html().toLowerCase().indexOf(typed_text);
                  if (match > -1){
                      $(this).addClass("highlightable")
                  }else{
                      $(this).removeClass("highlightable")
                  }
                  if (typed_text == ""){
                      $(this).removeClass("highlightable")
                  }

                }
                );
          }
      )}
);