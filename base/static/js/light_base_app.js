const header = document.getElementById('navBar')
const logo = document.getElementById('primary-logo')

window.addEventListener('scroll', function () {
  const currentScrollTop = window.pageYOffset || document.documentElement.scrollTop;
  
  if (currentScrollTop >= 15) {
    header.classList.add('bg-base-100', 'shadow-xl');
    logo.classList.add('text-primary')
  } else {
    header.classList.remove('bg-base-100', 'shadow-xl');
    logo.classList.remove('text-primary')
  }
});

lottie.loadAnimation({
  container: document.getElementById('profile-icon-lottie'),
  renderer: 'svg',
  loop: true,
  autoplay: true,
  path: '../../static/img/profile-icon-lottie.json',
  rendererSettings: {
  preserveAspectRatio: 'xMidYMid meet',
  progressiveLoad: false,
  scaleMode: 'noScale',
  hideOnTransparent: true
}
});