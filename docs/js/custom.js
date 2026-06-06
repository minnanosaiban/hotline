document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll('nav a[href^="http"]').forEach(function (link) {
    link.setAttribute("target", "_blank");
    link.setAttribute("rel", "noopener noreferrer");
  });
  document.querySelectorAll('main a[href^="http"]').forEach(function (link) {
    if (!link.href.includes(location.hostname)) {
      link.setAttribute("target", "_blank");
      link.setAttribute("rel", "noopener noreferrer");
    }
  });
});

// 本文内リンク（.acc-open）から対象のアコーディオン(details)を開いてスクロール
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll('a.acc-open[href^="#"]').forEach(function (link) {
    link.addEventListener("click", function (e) {
      var target = document.getElementById(link.getAttribute("href").slice(1));
      if (!target) return;
      e.preventDefault();
      if (target.tagName.toLowerCase() === "details") target.open = true;
      target.scrollIntoView({ behavior: "smooth", block: "start" });
      if (history.replaceState) history.replaceState(null, "", link.getAttribute("href"));
    });
  });
  // 直接 #id 付きのURLで開いた場合も details を展開する
  function openDetailsFromHash() {
    if (!location.hash || location.hash.length < 2) return;
    var target = document.getElementById(location.hash.slice(1));
    if (target && target.tagName.toLowerCase() === "details") {
      target.open = true;
      target.scrollIntoView({ block: "start" });
    }
  }
  openDetailsFromHash();
  window.addEventListener("hashchange", openDetailsFromHash);
});

function toggleindex() {
  const menu = document.getElementById("mobilemokuji");
  const icon = document.getElementById("mokuji-icon");
  const isVisible = window.getComputedStyle(menu).display !== "none";
  if (isVisible) {
    menu.style.display = "none";
    icon.classList.remove("fa-sort-down");
    icon.classList.add("fa-caret-right");
  } else {
    menu.style.display = "block";
    icon.classList.remove("fa-caret-right");
    icon.classList.add("fa-sort-down");
  }
}
