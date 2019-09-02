// Sidenav and DatePicker JS
$(document).ready(function(){
    $('.sidenav').sidenav();
});
$(document).ready(function(){
    $('.datepicker').datepicker({format:'yyyy-mm-dd'});
});

// Like images function
$( "img[name=cardImage]" ).click(function() {
  $this = $(this)
  var image_id = $this[0].id;
  var id_image = '#like-'+image_id
  $.ajax({
      url: 'like-picture',
      method: 'POST',
      data: {
        'image_id': image_id
      },
      dataType: 'json',
      success: function (data) {
        $(id_image).html(data['likes'])
      }
    });
});

// CSRF ajax protection
$.ajaxSetup({
beforeSend: function(xhr, settings) {
 function getCookie(name) {
     var cookieValue = null;
     if (document.cookie && document.cookie != '') {
         var cookies = document.cookie.split(';');
         for (var i = 0; i < cookies.length; i++) {
             var cookie = jQuery.trim(cookies[i]);
             // Does this cookie string begin with the name we want?
             if (cookie.substring(0, name.length + 1) == (name + '=')) {
                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                 break;
             }
         }
     }
     return cookieValue;
 }
 if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
     // Only send the token to relative URLs i.e. locally.
     xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
 }
}
});
