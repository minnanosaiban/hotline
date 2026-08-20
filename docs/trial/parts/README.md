# parts/ — 書面の部品ファイル置き場

このフォルダのファイルは、`mkdocs.yml`の`exclude_docs`により**単独ページとしては公開されない**。
trial/agm系のページ本体（whistleblower.md等）から、

```
:include: parts/ファイル名.md
```

という1行で読み込んで使う（overrides/hooks/doc_indent.pyが展開する。部品内の`:N X:`マーカーも
展開される。includeの入れ子は不可・1段のみ）。

運用：sidenote-pdf-docの「hotline書き出し」ボタンがこのフォルダへ部品ファイルを直接保存する
（書面を修正したら再書き出し＝同名ファイルの上書きだけで反映される）。
新しい書面を追加した時だけ、ページ本体に`:include:`行を1行足す。
