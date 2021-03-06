'use strict';

// IMPORTANT
// Relies on Sortable.JS (https://github.com/RubaXa/Sortable)
// Include script from CDN at top of the file
//<script src="https://cdn.jsdelivr.net/npm/sortablejs@1.6.1/Sortable.min.js"></script>

(function () {
  function SlugField (el) {

    var slugFrom = el.dataset.slug
    var fromField = document.getElementById('id_'+slugFrom)

    if (!el.value) {
      fromField.addEventListener('keyup', function() {
        var slug = window.URLify(this.value)
        el.value = slug
        el.parentNode.parentNode.classList.remove('form__group--inactive')
      })
    }
  }

  /////////////////////////////////////////////////////////////////////////////

  // Bootstrap any file uploaders

  function documentReady () {
    return (document.readyState === 'interactive' || document.readyState === 'complete')
  }

  function bootstrap () {
    document.removeEventListener('readystatechange', bootstrap)

    var slugFields = document.querySelectorAll('[data-slug]')

    for (var i = 0; i < slugFields.length; i++) {
      new SlugField(slugFields[i])
    }
  }

  if (documentReady()) {
    bootstrap()
  } else {
    document.addEventListener('readystatechange', bootstrap)
  }
}())
