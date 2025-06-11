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