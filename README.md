# みんなの裁判

## URL
  - https://minnanosaiban.github.io/hotline/

## git

```
git checkout main
git add ./* _static
git commit -m "Add source files and static assets to main branch"
git push origin main
```

```
git clone https://github.com/minnanosaiban/hotline.git
git remote set-url origin https://github.com/minnanosaiban/hotline.git
jb clean .
jb build .
ghp-import -n -p -f _build/html
```

## メタタグ

```
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="ＥＮＥＯＳの内部通報制度に関する訴訟について">
<meta name="twitter:description" content="従業員からの通報を受けたＥＮＥＯＳは、不正を隠蔽するために、不正を重ねた疑いがあります。">
<meta name="twitter:image" content="https://minnanosaiban.github.io/hotline/_static/logo.png">


<meta property="og:title" content="ＥＮＥＯＳの内部通報制度に関する訴訟について">
<meta property="og:description" content="従業員からの通報を受けたＥＮＥＯＳは、不正を隠蔽するために、不正を重ねた疑いがあります。">
<meta property="og:image" content="https://minnanosaiban.github.io/hotline/_static/logo.png">
<meta property="og:url" content="https://minnanosaiban.github.io/hotline/">

```


https://minnanosaiban.github.io/hotline/google41b9fb8c20b97e3f.html

## sitemap.xml

https://minnanosaiban.github.io/hotline/sitemap.xmlでアクセスできるようする。

```
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://minnanosaiban.github.io/hotline/index.html</loc>
    <lastmod>2024-08-19</lastmod>
    <changefreq>monthly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://minnanosaiban.github.io/hotline/eneos_allegation</loc>
    <lastmod>2024-08-19</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://minnanosaiban.github.io/hotline/eneos_compliance</loc>
    <lastmod>2024-08-19</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://minnanosaiban.github.io/hotline/whistleblower_protection_act</loc>
    <lastmod>2024-08-19</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://minnanosaiban.github.io/hotline/2024allegation</loc>
    <lastmod>2024-08-19</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://minnanosaiban.github.io/hotline/2024background</loc>
    <lastmod>2024-08-19</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://minnanosaiban.github.io/hotline/2021judicial_interpretation</loc>
    <lastmod>2024-08-19</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://minnanosaiban.github.io/hotline/2021judgment</loc>
    <lastmod>2024-08-19</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://minnanosaiban.github.io/hotline/2021allegation</loc>
    <lastmod>2024-08-19</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://minnanosaiban.github.io/hotline/2021background</loc>
    <lastmod>2024-08-19</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>

```



## robots.txt

https://minnanosaiban.github.io/hotline/robots.txtでアクセスできるようにする

```
User-agent: *
Disallow: /private/
Allow: /public/
Sitemap: https://minnanosaiban.github.io/hotline/sitemap.xml
```
