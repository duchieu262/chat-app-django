$("#join").click(function(){
  $("#join-form").toggle(300);
});




$(".expand-button").click(function() {
  $("#profile").toggleClass("expanded");
	$("#contacts").toggleClass("expanded");
});

$(".messages").animate({ scrollTop: $(document).height() }, "fast");
$(document).ready(function(){

  $("#search-input").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#user-list li").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });

  $("#search-room").on("keyup", function() {
    console.log("search")
    var value = $(this).val().toLowerCase();
    $("#list-room a").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});

function confirmSubmit()
{
  var agree=confirm("Are you sure you want to leave this room?");
  if (agree)
    return true ;
  else
    return false ;
}