## mkdocs

```shell
mkdocs build --clean
mkdocs build
mkdocs serve
mkdocs gh-deploy --force
git add .
git reset site/
git commit -m "Update main branch (excluding site/)"
git push -f origin main
```