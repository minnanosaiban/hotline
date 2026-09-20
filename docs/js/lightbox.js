// 画像クリックで拡大（GLightbox）。mkdocs-glightbox プラグインがビルド時にやっていたことを、ページ内のスクリプトで行う。
// リンクに包まれていない <img> を <a class="glightbox"> で包み、GLightbox に拾わせる。
// agm のカルーセルは Swiper がスライドを複製するので、複製の前（このスクリプトは Swiper より先に読む）に包んでおく。
(function () {
  document.querySelectorAll(".md-content__inner img").forEach(function (img) {
    if (img.closest("a") || img.classList.contains("off-glb")) return;
    var a = document.createElement("a");
    a.className = "glightbox";
    a.setAttribute("data-type", "image");
    a.setAttribute("data-width", "90%");
    a.setAttribute("data-height", "auto");
    a.setAttribute("data-desc-position", "bottom");
    a.setAttribute("href", img.getAttribute("src"));
    img.replaceWith(a);
    a.appendChild(img);
  });
  if (window.GLightbox) {
    window.GLightbox({ touchNavigation: true, loop: false, zoomable: true, draggable: true, openEffect: "zoom", closeEffect: "zoom", slideEffect: "slide" });
  }
})();
