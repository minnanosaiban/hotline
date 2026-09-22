/*
 * doc-accordion.js
 * trial/index.md の書面アコーディオン（<details class="doc-acc" data-md="md/x.md.txt" data-pdf="…">）に、
 * .pdf / .md / 要約 のボタンと開閉マークを付ける。書面の本文は MkDocs がビルド時に HTML へ入れてあるので、
 * ここでは取得しない（検索エンジン・ページ内検索・Xカードにそのまま出る）。
 *
 *  - .pdf … data-pdf があれば有効。無ければグレー（court-calendar の訴訟資料一覧と同じ）
 *  - .md  … 「コピーする／ダウンロード」の2択。元は data-md の生ファイル（docs/trial/md/x.md.txt が静的に公開される）を取得する。
 *           hotline 形式（:N X#id: マーカー、またはそれを焼き込んだ <p class="padN …"> 段落）の本文は平文の Markdown に戻す。
 *           サイドノート作成ツールの「ウェブ用」書き出しはそのまま。
 *  - 要約 … data-summary があれば有効（ポップアップ）。無ければグレー
 *  - data-no-md … .pdf・要約は出すが、.md のアイコン自体を出さない（原文にこちらの注記を書き足した書面など）
 *  - #アンカー（書面の中の <a name> や書面id）で開いたとき、閉じている書面を開いてその位置へ移動する
 *  - サイドノート（段落の直後の <aside>）を、注番号 <sup>N</sup> の直後へ移して、参照している行と揃える
 */
(function () {
  'use strict';

  var SITE_TITLE = 'ＥＮＥＯＳの内部通報制度をめぐる訴訟';
  var MARKER_RE = /^[ \t]*:([0-9])(?:h2|h3|h|i|d)(?:#[A-Za-z0-9_\-]+)?:[ \t]*/;

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; });
  }

  // ---------------------------------------------------------------- 本文の md（.md ボタン）
  // hotline 形式かどうか。元の :N X#id: マーカーのほか、マーカーを <p class="padN …"> の段落へ焼き込んだ形（今の11書面）も含む。
  function isLegacy(text) {
    return /^[ \t]*:[0-9](?:h2|h3|h|i|d)(?:#[A-Za-z0-9_\-]+)?:/m.test(text) ||
      /^<p class="[^"]*\b(?:pad[0-9]|hg-idt|idt|doc)\b[^"]*"/m.test(text);
  }
  // 本文・ノートの「●」は、表示ではアイコン <i class="bi bi-dot"></i> にしてある。.md には元の文字「●」で渡す。
  var DOT_ICON_RE = /<i class="bi bi-dot"><\/i>/g;
  // サイドノート（<aside>）は、「> 」で始まる引用にして、対応する段落の直後に残す。<br> は行の区切り。
  function noteToMarkdown(inner) {
    return inner.replace(/\n/g, ' ').split(/<br\s*\/?>/i).map(function (line) {
      return line.replace(DOT_ICON_RE, '●')
        .replace(/<i class="[^"]*arrow-right[^"]*"><\/i>/gi, '→').replace(/<i class="[^"]*arrow-left[^"]*"><\/i>/gi, '←')
        .replace(/<\/?(?:b|strong)>/gi, '**').replace(/<\/?[a-z][^>]*>/gi, '').replace(/[ \t]{2,}/g, ' ').trim();
    }).filter(Boolean).map(function (line) { return '> ' + line; }).join('\n');
  }
  // hotline 形式を平文の Markdown へ。インデント・ぶら下げの体裁は落ち、1つ1つの段落になる。
  function toPlainMarkdown(text) {
    return String(text).replace(/^﻿/, '').replace(/\r\n?/g, '\n').trim().split(/\n{2,}/).map(function (block) {
      var note = /^\s*<aside\b[^>]*>([\s\S]*)<\/aside>\s*$/i.exec(block);
      if (note) return noteToMarkdown(note[1]);
      var m = MARKER_RE.exec(block);
      var t = (m ? block.slice(m[0].length) : block).replace(/\n/g, ' ');
      return t
        .replace(DOT_ICON_RE, '●')
        .replace(/<a name="[^"]*"><\/a>/g, '')
        .replace(/<br\s*\/?>/gi, '  \n')
        .replace(/<\/?(?:b|strong)>/gi, '**')
        .replace(/<\/?(?:p|div|span)\b[^>]*>/gi, ' ')
        .replace(/[ \t]{2,}(?!\n)/g, ' ')
        .trim();
    }).filter(Boolean).join('\n\n');
  }
  var cache = {};
  function fetchText(url) {
    if (!cache[url]) {
      cache[url] = fetch(url).then(function (r) {
        if (!r.ok) throw new Error(r.status + ' ' + url);
        return r.text();
      }).catch(function (e) { delete cache[url]; throw e; });
    }
    return cache[url];
  }
  function titleOf(d) { return d.getAttribute('data-title') || d.querySelector('.doc-title').textContent.trim(); }
  function sideOf(d) {           // 直前の見出し（原告側／被告側／…）
    var rows = d.closest('.doc-rows'), h = rows && rows.previousElementSibling;
    return h && h.classList.contains('doc-side') ? h.textContent.trim() : '';
  }
  function docMarkdown(d) {
    var url = new URL(d.getAttribute('data-md'), location.href).href;
    return fetchText(url).then(function (text) {
      var body = isLegacy(text) ? toPlainMarkdown(text) : String(text).replace(/\r\n?/g, '\n').trim();
      var head = '# ' + titleOf(d) + '\n\n' + [SITE_TITLE, sideOf(d), titleOf(d)].filter(Boolean).join('／') + '\n' +
        '掲載ページ: ' + location.origin + location.pathname + '#' + d.id;
      if (isLegacy(text) && /<aside\b/i.test(text)) head +='\n注: 「> 」で始まる行は、右の余白に並べているサイドノート（相手方の書面での認否）です。';
      return head + '\n\n' + body + '\n';
    });
  }
  function copyText(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) return navigator.clipboard.writeText(text);
    return new Promise(function (resolve, reject) {
      var ta = document.createElement('textarea');
      ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
      document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy') ? resolve() : reject(new Error('copy failed')); } catch (e) { reject(e); }
      ta.remove();
    });
  }
  function downloadText(name, text) {
    var a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([text], { type: 'text/markdown;charset=utf-8' }));
    a.download = name;
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
  }
  function flash(btn, label) {
    var orig = btn.innerHTML;
    btn.classList.add('copied');
    btn.innerHTML = '<i class="bi bi-check2" aria-hidden="true"></i>' + label;
    setTimeout(function () { btn.classList.remove('copied'); btn.innerHTML = orig; }, 1600);
  }

  // ---------------------------------------------------------------- 要約ポップアップ
  function openSummary(d) {
    var dlg = document.getElementById('doc-sum-dialog');
    if (!dlg) {
      dlg = document.createElement('dialog');
      dlg.id = 'doc-sum-dialog';
      dlg.className = 'doc-sum md-typeset';
      dlg.innerHTML = '<p class="doc-sum-title"></p><p class="doc-sum-text"></p><p class="doc-sum-src"></p>' +
        '<form method="dialog"><button class="dbtn">閉じる</button></form>';
      dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });   // 外側クリックで閉じる
      document.body.appendChild(dlg);
    }
    dlg.querySelector('.doc-sum-title').textContent = titleOf(d);
    dlg.querySelector('.doc-sum-text').textContent = d.getAttribute('data-summary');
    var model = d.getAttribute('data-summary-model'), date = d.getAttribute('data-summary-date');
    var srcEl = dlg.querySelector('.doc-sum-src');
    srcEl.hidden = !(model || date);                       // 手で書いた要約には出所を出さない（court-calendar と同じ）
    srcEl.textContent = ['AI要約', model, date].filter(Boolean).join('　');
    dlg.showModal();
  }

  // ---------------------------------------------------------------- 行にボタンを付ける
  function btnHtml(d) {
    var pdf = d.getAttribute('data-pdf');
    var pdfBtn = pdf
      ? '<a class="dbtn pdf" href="' + esc(pdf) + '" target="_blank" rel="noopener"><i class="bi bi-file-earmark-pdf" aria-hidden="true"></i>.pdf</a>'
      : '<span class="dbtn off"><i class="bi bi-file-earmark-pdf" aria-hidden="true"></i>.pdf</span>';
    // data-no-md: .pdf・要約は出すが、.md（コピー／ダウンロード）のアイコン自体を出さない
    var mdBtn = d.hasAttribute('data-no-md') ? '' : d.getAttribute('data-md')
      ? '<span class="dmdwrap"><button type="button" class="dbtn" data-mdtoggle><i class="bi bi-clipboard" aria-hidden="true"></i>.md</button>' +
        '<span class="dmdmenu" hidden>' +
        '<button type="button" data-mdcopy><i class="bi bi-clipboard" aria-hidden="true"></i>コピーする</button>' +
        '<button type="button" data-mddl><i class="bi bi-download" aria-hidden="true"></i>ダウンロード</button>' +
        '</span></span>'
      : '<span class="dbtn off"><i class="bi bi-clipboard" aria-hidden="true"></i>.md</span>';
    var sumBtn = d.getAttribute('data-summary')
      ? '<button type="button" class="dbtn" data-sumopen><i class="bi bi-stars" aria-hidden="true"></i>要約</button>'
      : '<span class="dbtn off"><i class="bi bi-stars" aria-hidden="true"></i>要約</span>';
    return '<span class="doc-btns">' + pdfBtn + mdBtn + sumBtn + '</span>';
  }
  function enhanceRow(d) {
    var summary = d.querySelector(':scope > summary');
    if (!summary || summary.querySelector('.doc-title')) return;
    var title = summary.textContent.trim();
    d.setAttribute('data-title', title);
    // data-plain: 書面ではない行（「高裁判決の根拠」の各行など）。PDF・.md・要約のボタンは付けない
    summary.innerHTML = '<span class="doc-title">' + esc(title) + '</span>' + (d.hasAttribute('data-plain') ? '' : btnHtml(d)) +
      '<i class="doc-chev bi bi-chevron-down" aria-hidden="true"></i>';
  }

  // ---------------------------------------------------------------- サイドノートを注番号の直後へ
  // float:right のノートは「置かれた位置」から右余白に出るので、段落の後ろに置いたままだと次の段落の高さに出てしまう。
  // 注番号 <sup>N</sup> の直後に入れれば、その注を参照している行と揃う。番号が見つからなければ段落の先頭に入れる。
  function alignSidenotes() {
    [].slice.call(document.querySelectorAll('.doc-body aside.sn-note, .doc-body aside.sidenote')).reverse().forEach(function (a) {
      var prev = a.previousElementSibling;
      while (prev && prev.tagName === 'ASIDE') prev = prev.previousElementSibling;
      if (!prev || prev.tagName !== 'P') return;
      var numEl = a.querySelector('.sn-note-num, .num');
      var num = numEl ? numEl.textContent.trim() : '', ref = null;
      [].slice.call(prev.querySelectorAll('sup')).forEach(function (sup) { if (!ref && sup.textContent.trim() === num) ref = sup; });
      if (ref) ref.parentNode.insertBefore(a, ref.nextSibling);
      else prev.insertBefore(a, prev.firstChild);
    });
  }

  // ---------------------------------------------------------------- #アンカーで書面を開く
  // 開くと高さが変わるので再スクロールする。さらに Web フォントの読み込みで本文の高さが後から変わり、
  // 移動先が固定ヘッダーの下へずれることがあるため、フォント読み込みの完了後にも一度だけ位置を取り直す
  // （読み手が既に自分でスクロールし始めていたら、取り直さない）。
  var userMoved = false;
  ['wheel', 'touchstart', 'keydown', 'mousedown'].forEach(function (ev) {
    window.addEventListener(ev, function () { userMoved = true; }, { passive: true, once: true });
  });
  function goTo(el) {
    el.scrollIntoView({ block: 'start' });
    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(function () { if (!userMoved) el.scrollIntoView({ block: 'start' }); });
    }
  }
  function reveal() {
    var id = decodeURIComponent(location.hash.replace(/^#/, ''));
    if (!id) return;
    var el = document.getElementById(id) || document.getElementsByName(id)[0];
    if (!el) return;
    var opened = false;
    for (var d = el.closest('details'); d; d = d.parentElement && d.parentElement.closest('details')) {
      if (!d.open) { d.open = true; opened = true; }
    }
    if (opened) setTimeout(function () { goTo(el); }, 0);
  }

  // ---------------------------------------------------------------- 起動
  document.addEventListener('DOMContentLoaded', function () {
    var rows = document.querySelectorAll('details.doc-acc');
    if (!rows.length) return;
    rows.forEach(enhanceRow);
    alignSidenotes();
    reveal();
    window.addEventListener('hashchange', reveal);

    document.addEventListener('click', function (e) {
      var t = e.target.closest && e.target.closest('[data-mdtoggle],[data-mdcopy],[data-mddl],[data-sumopen]');
      if (!t) {                                       // メニューの外をクリックしたら閉じる
        if (!(e.target.closest && e.target.closest('.dmdwrap'))) document.querySelectorAll('.dmdmenu').forEach(function (m) { m.hidden = true; });
        return;
      }
      e.preventDefault(); e.stopPropagation();        // summary の中のボタンなので、開閉させない
      var d = t.closest('details.doc-acc');
      if (t.hasAttribute('data-mdtoggle')) {
        var menu = t.parentElement.querySelector('.dmdmenu'), willOpen = menu.hidden;
        document.querySelectorAll('.dmdmenu').forEach(function (m) { m.hidden = true; });
        menu.hidden = !willOpen;
      } else if (t.hasAttribute('data-sumopen')) {
        openSummary(d);
      } else {
        var isCopy = t.hasAttribute('data-mdcopy');
        docMarkdown(d).then(function (md) {
          if (isCopy) return copyText(md).then(function () { flash(t, 'コピーしました'); });
          downloadText((titleOf(d)).replace(/[\\\/:*?"<>|]/g, '_') + '.md', md);
          flash(t, '保存しました');
        }).catch(function () { alert('本文を取得できませんでした。通信環境をご確認のうえ、再読み込みしてください。'); });
      }
    });
  });
})();
