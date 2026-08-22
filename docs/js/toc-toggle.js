// trial-docページ（判決文・準備書面）の右目次を、JupyterBook/eneos-saibanと同じ挙動にする
// （案5、2026-08-22採用）。
//   ・初期状態は目次が表示されている
//   ・サイドノート（<aside class="sidenote">）が画面内にある間だけ、目次の一覧を自動で隠す
//   ・「目次 ▾」クリックで手動に切り替え：隠れている時は浮くカードで開く／出ている時は閉じる
//   ・サイドノートの出入りで自動状態が変わったら手動指定はリセット（スクロールすれば元の自動に戻る）
// 対象はbody.trial-docのみ。見た目は docs/css/11-trial.css（.toc-hidden / .toc-overlay）側。
//
// 浮くカードをposition:fixedで座標指定する理由：.md-sidebar__scrollwrap（Material標準）が
// overflow-y:autoで一覧を隠した高さにクリップするため、単純なabsoluteだと見えない（試作1回目で確認）。
document.addEventListener("DOMContentLoaded", function () {
  if (!document.body.classList.contains("trial-doc")) return;
  var sidebar = document.querySelector(".md-sidebar--secondary");
  if (!sidebar) return;
  var title = sidebar.querySelector(".md-nav__title");
  var list = sidebar.querySelector(".md-nav--secondary > .md-nav__list");
  if (!title || !list) return;

  var autoHidden = false;        // サイドノートが見えている＝自動で隠す状態か
  var manual = null;             // null=自動 / "open"=手動で開いた / "closed"=手動で閉じた

  function positionList() {
    var r = title.getBoundingClientRect();
    list.style.left = r.left + "px";
    list.style.width = r.width + "px";
    list.style.top = r.bottom + "px";
  }
  function render() {
    var visible = manual === "open" ? true : manual === "closed" ? false : !autoHidden;
    var overlay = visible && autoHidden;   // サイドノートの上に重ねて出す場合だけ浮くカード
    sidebar.classList.toggle("toc-hidden", !visible);
    sidebar.classList.toggle("toc-overlay", overlay);
    if (overlay) positionList();
    else list.style.left = list.style.width = list.style.top = "";
  }
  function setAutoHidden(next) {
    if (next === autoHidden) return;
    autoHidden = next;
    manual = null;   // 自動状態が切り替わったら手動指定は忘れる（JupyterBookと同じ感覚）
    render();
  }

  // サイドノートの出入りを監視（スクロール／リサイズ時に位置を測る）。
  // IntersectionObserverは非表示タブで通知が止まるなど検証しづらかったため、
  // 単純に毎回測る方式にした（サイドノートは多くても数百件・rAFで間引くので実害なし）。
  var notes = Array.prototype.slice.call(document.querySelectorAll(".sidenote"));
  function anyNoteInView() {
    var vh = window.innerHeight;
    for (var i = 0; i < notes.length; i++) {
      var r = notes[i].getBoundingClientRect();
      if (r.width > 0 && r.bottom > 0 && r.top < vh) return true;   // display:none（スマホ幅）は幅0で除外
    }
    return false;
  }
  function checkNotesNow() {
    setAutoHidden(notes.length > 0 && anyNoteInView());
  }
  // スクロール連打用の間引き（約40ms）。requestAnimationFrameは非表示タブで止まり検証しづらいので
  // setTimeoutにしている。初回判定は checkNotesNow() を直接呼ぶ。
  var checking = false;
  function checkNotes() {
    if (checking) return;
    checking = true;
    setTimeout(function () {
      checkNotesNow();
      checking = false;
    }, 40);
  }

  // 手動開閉
  title.addEventListener("click", function (e) {
    e.preventDefault();
    e.stopPropagation();
    var visibleNow = !sidebar.classList.contains("toc-hidden");
    manual = visibleNow ? "closed" : "open";
    render();
  });
  function closeOverlay() {
    if (manual === "open" && sidebar.classList.contains("toc-overlay")) {
      manual = null;
      render();
    }
  }
  document.addEventListener("click", function (e) {
    if (!sidebar.contains(e.target)) closeOverlay();
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeOverlay();
  });
  // 浮くカードを出している間は、スクロール・リサイズで見出し行の位置に追従させる
  var ticking = false;
  function follow() {
    if (!sidebar.classList.contains("toc-overlay")) return;
    if (ticking) return;
    ticking = true;
    setTimeout(function () { positionList(); ticking = false; }, 40);
  }
  function onScrollOrResize() {
    checkNotes();
    follow();
  }
  window.addEventListener("scroll", onScrollOrResize, { passive: true });
  window.addEventListener("resize", onScrollOrResize);
  // アコーディオン（details）の開閉で中のサイドノートが現れる／消える場合も拾う
  document.addEventListener("toggle", checkNotes, true);

  checkNotesNow();
  render();
});
