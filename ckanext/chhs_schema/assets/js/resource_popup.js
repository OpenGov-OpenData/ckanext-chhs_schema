$('.clickpopup').click(function(e){
  $('#overlay').find('.popup-close-btn').attr('data-resourceurl',$(this).attr('href'))
  $('#overlay').fadeIn(300);
  e.stopImmediatePropagation();
  return false;
});

$('.popup-close-btn').click(function() {
  $('#overlay').fadeOut(300);
  var url = $(this).attr('data-resourceurl');
  window.open(url,'_blank');
});
