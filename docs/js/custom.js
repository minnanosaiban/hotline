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

// タブのドロップダウン（「裁判文書公開」等）。ホバーではなくクリックで開閉する
// （ホバーだけだと、タップ操作やホバーせずクリックした場合に「ドロップダウンが無い」ように見えるため）。
// 開いた状態は is-open クラスで表す。トリガーの <a href> はそのまま残してあるので、
// このスクリプトが読み込まれない場合は先頭の子ページへの通常のリンクとして動く。
document.addEventListener("DOMContentLoaded", function () {
  var items = document.querySelectorAll(".md-tabs__item--dropdown");
  if (!items.length) return;

  function closeAll(except) {
    items.forEach(function (item) {
      if (item === except) return;
      item.classList.remove("is-open");
      var a = item.querySelector(".md-tabs__link--dropdown");
      if (a) a.setAttribute("aria-expanded", "false");
    });
  }

  items.forEach(function (item) {
    var trigger = item.querySelector(".md-tabs__link--dropdown");
    if (!trigger) return;
    trigger.addEventListener("click", function (e) {
      e.preventDefault();
      var open = item.classList.toggle("is-open");
      trigger.setAttribute("aria-expanded", String(open));
      closeAll(item);
    });
  });

  document.addEventListener("click", function (e) {
    if (!e.target.closest(".md-tabs__item--dropdown")) closeAll();
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeAll();
  });
});
