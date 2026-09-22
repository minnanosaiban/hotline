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
// .md-tabs__dropdown は position:fixed にしてあり、開くたびにトリガーの位置から
// top/left をここで計算してインライン style に置く（02-layout.css のコメント参照。
// .md-tabs__list の overflow:auto が横スクロール用に必要で、CSSの仕様上それがあると
// 縦方向も自動でクリップされてしまうため、absolute のままでは祖先の overflow から
// 逃れられなかった。fixed + JS計算なら祖先の影響を受けず、画面右端からのはみ出しも防げる）。
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

  function place(item, trigger) {
    var dd = item.querySelector(".md-tabs__dropdown");
    if (!dd) return;
    var r = trigger.getBoundingClientRect();
    var margin = 8;
    var left = Math.min(r.left, window.innerWidth - dd.offsetWidth - margin);
    left = Math.max(margin, left);
    dd.style.top = Math.round(r.bottom + 10) + "px";
    dd.style.left = Math.round(left) + "px";
  }

  items.forEach(function (item) {
    var trigger = item.querySelector(".md-tabs__link--dropdown");
    if (!trigger) return;
    // リスナーは <li> 全体に付ける（<a> だけだと、スマホでタップした位置が少しでも
    // ずれると外れて反応しないことがあった。2026-09-22、実機で発覚）。
    // ただし開いたあとの中の項目（.md-tabs__dropdown 内）のクリックは、開閉に関与させず
    // 通常のリンク遷移に任せる。
    item.addEventListener("click", function (e) {
      if (e.target.closest(".md-tabs__dropdown")) return;
      e.preventDefault();
      var open = item.classList.toggle("is-open");
      trigger.setAttribute("aria-expanded", String(open));
      if (open) place(item, trigger);
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
