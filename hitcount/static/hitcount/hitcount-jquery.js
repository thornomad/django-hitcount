$(document).ready(function() {
  /**
   * https://docs.djangoproject.com/en/dev/ref/contrib/csrf/#ajax
   *
   * Remember you will need to ensure csrf tokens by adding:
   * @ensure_csrf_cookie to your views that require this javascript
   *
   * Also, you will probably want to include this with your other sitewide
   * javascript files ... this is just an example.
   */

   if ( typeof hitcountJS === 'undefined' ) {
    // since this is loaded on every page only do something
    // if a hit is going to be counted
    return;
   }

  var hitcountPK = hitcountJS['hitcountPK'];
  var hitcountURL = hitcountJS['hitcountURL'];
  var csrftoken = getCookie('csrftoken');

  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      }
  });

  $.post( hitcountURL, { "hitcountPK" : hitcountPK },
    function(data, status) {

      console.log(data); // just so you can see the response

      if (data.status == 'error') {
        // do something for error?
      }
    }, 'json');
});

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

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
