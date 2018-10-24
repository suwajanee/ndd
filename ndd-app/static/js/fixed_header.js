window.onload = function () {
  var tableCont = document.querySelector('#table-cont')
  /**
   * scroll handle
   * @param {event} e -- scroll event
   */
  function scrollHandle(e) {
    var scrollTop = this.scrollTop;
    this.querySelector('thead').style.transform = 'translateY(' + scrollTop + 'px)';
  }

  tableCont.addEventListener('scroll', scrollHandle)

  var filterDate = document.querySelector('#upper-part');

  tableCont.style.top = filterDate.offsetTop + 60 + 'px';
}


