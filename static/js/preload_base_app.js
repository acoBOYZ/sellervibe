function getTheme() {
  if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      // return 'night';
      return 'forest';
  } else {
      // return 'winter';
      return 'corporate';
  }
}

document.documentElement.setAttribute('data-theme', getTheme());

window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function() {
  document.documentElement.setAttribute('data-theme', getTheme());
});