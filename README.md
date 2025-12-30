## mkdocs

```shell
git clone https://github.com/minnanosaiban/hotline.git
git remote set-url origin https://github.com/minnanosaiban/hotline.git
```

```shell
mkdocs build --clean
mkdocs build
mkdocs serve
```

```shell
mkdocs gh-deploy --force
git add .
git reset site/
git commit -m "Update main branch (excluding site/)"
git push -f origin main
```

