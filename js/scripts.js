$('.photo img').jail({
  effect: 'fadeIn'
});

if (location.hash){

  var windowHeight = $(window).height();
  var elementHeight = $(location.hash).height();
  var elementPosition = $(location.hash).position();
  var elementTop = elementPosition.top;
  var toScroll = (windowHeight / 2) - (elementHeight / 2);

  setTimeout(function() {
    window.scroll(0, (elementTop - toScroll));
  }, 1);
}

$('#labels-button').click(function(){
  event.preventDefault();
  $(this).toggleClass('active');
  $('.ribbon').toggleClass('hidden');
});

$('.anchor').click(centerAnchor);

function centerAnchor(e){
  e.preventDefault();
  window.location.hash = $(this).attr('href');

  var windowHeight = $(window).height();
  var elementHeight = $(location.hash).height();
  var elementPosition = $(location.hash).position();
  var elementTop = elementPosition.top;
  var toScroll = (windowHeight / 2) - (elementHeight / 2);

  window.scroll(0, (elementTop - toScroll));
}

$('body').on('touchstart.dropdown', '.dropdown-menu', function (e) { e.stopPropagation(); });

function imgError(image) {
  image.onerror = "";
  image.src = "/img/placeholder.png";
  return true;
}
