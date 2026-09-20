// 質問パネルのカルーセル（.qa-carousel）初期化。
// Swiper本体（CDN）は overrides/hooks/add_blog_class.py が agm/index.md にのみ注入している。
// ページ内に .qa-carousel が複数あっても forEach で全部拾うので、
// 同じHTML構造（.qa-carousel.swiper > .swiper-wrapper > .swiper-slide + .swiper-pagination）を
// 別ページに増やすだけで、この初期化コードは変更なしに使い回せる。
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".qa-carousel").forEach(function (el) {
    new Swiper(el, {
      slidesPerView: 1.3,
      spaceBetween: 20,
      centeredSlides: true,
      loop: true,
      autoplay: { delay: 3500, disableOnInteraction: false },
      speed: 900,
      pagination: { el: el.querySelector(".swiper-pagination"), clickable: true },
      breakpoints: {
        768: { slidesPerView: 2.2, spaceBetween: 28 },
      },
    });
  });
});
