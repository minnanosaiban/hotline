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

// タブのドロップダウン（「裁判文書公開」等）。開閉そのものはネイティブの
// <details>/<summary>（overrides/partials/tabs-item.html）がブラウザの機能として行うので、
// このJSはあくまで補助（他のドロップダウンが開いていたら閉じる／外側クリックで閉じる）。
// 独自クリック処理で開閉させていた前の版は、開発機では動いたがユーザーの実機Chromeでは
// 反応しなかった（原因不明）ため、確実に動くネイティブな仕組みに切り替えた（2026-09-22）。
// この補助JSが万一効かなくても、開閉・ページ遷移という核心の機能には影響しない。
document.addEventListener("DOMContentLoaded", function () {
  var details = document.querySelectorAll(".md-tabs__dropdown-details");
  if (!details.length) return;

  details.forEach(function (d) {
    d.addEventListener("toggle", function () {
      if (!d.open) return;
      details.forEach(function (other) {
        if (other !== d) other.open = false;
      });
    });
  });

  document.addEventListener("click", function (e) {
    details.forEach(function (d) {
      if (d.open && !d.contains(e.target)) d.open = false;
    });
  });
});
