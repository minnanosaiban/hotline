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

function toggleMenu() {
  const menu = document.getElementById("mobileMenu");
  menu.style.display = (menu.style.display === "block") ? "none" : "block";
}

function toggleindex() {
  const menu = document.getElementById("mobilemokuji");
  const icon = document.getElementById("mokuji-icon");
  const isVisible = window.getComputedStyle(menu).display !== "none";
  if (isVisible) {
    menu.style.display = "none";
    icon.classList.remove("fa-sort-down");
    icon.classList.add("fa-caret-right");
  } else {
    menu.style.display = "block";
    icon.classList.remove("fa-caret-right");
    icon.classList.add("fa-sort-down");
  }
}