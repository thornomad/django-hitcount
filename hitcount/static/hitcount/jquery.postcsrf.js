(function($) {

  $.postCSRF = function(url, data, callback, type) {

    function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie !== '') {
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

    var csrftoken = getCookie('csrftoken');

    // shift arguments if data argument was omitted
    if ($.isFunction(data)) {
      type = type || callback;
      callback = data;
      data = undefined;
    }

    return $.ajax(jQuery.extend({
      url: url,
      type: "POST",
      dataType: type,
      data: data,
      success: callback,
      beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      }
    }, jQuery.isPlainObject(url) && url));
  };

}(jQuery));


// $.postCSRF("%s", {
//   hitcountPK: "%s"
// });

// $.postCSRF("%s",
//   { hitcountPK : "%s" }).done(function(data){
//   console.log('got it to work!');
//   console.log(data);
// }).fail(function(data){
//   console.log('failed');
//   console.log(data);
// });
// });
