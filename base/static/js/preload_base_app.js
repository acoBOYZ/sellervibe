function getTheme() {
  if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      return 'night';
  } else {
      return 'winter';
  }
}

// Set the default theme on page load
document.documentElement.setAttribute('data-theme', getTheme());

// Update the theme when the user's color scheme changes
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function() {
  document.documentElement.setAttribute('data-theme', getTheme());
});