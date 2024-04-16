/* --------------------------------------------------------
fade
-------------------------------------------------------- */
$(function () {
  $(window).scroll(function () {
    $('.u-fade').each(function () {
      var targetElement = $(this).offset().top;
      var scroll = $(window).scrollTop();
      var windowHeight = $(window).height();
      if (scroll > targetElement - windowHeight + 0) {
        $(this).css('opacity', '1');
        $(this).css('transform', 'translateY(0)');
      }
    });
  });
});


/* --------------------------------------------------------
scroll
-------------------------------------------------------- */
$(function () {
  $('a[href^="#"]').click(function () {
    let speed = 700;
    let href = $(this).attr("href");
    let target = $(href == "#" || href == "" ? 'html' : href);
    let position = target.offset().top;
    $("html, body").animate({ scrollTop: position }, speed, "swing");
    return false;
  });
});