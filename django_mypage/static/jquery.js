$(
  function(){
    $("#checkAll").click(function(){$('input:checkbox').not(this).prop('checked', this.checked);});
  }

);




$(function(){
     $("#kw").keyup(
          function(){
              typed_text = $(this).val()

                $('#tr_transactions #description').each(function() {
                  var match = $(this).html().toLowerCase().indexOf(typed_text)
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