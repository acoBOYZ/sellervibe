const header = document.getElementById('navBar')
const logo = document.getElementById('primary-logo')

window.addEventListener('scroll', function () {
  const currentScrollTop = window.pageYOffset || document.documentElement.scrollTop;
  
  if (currentScrollTop >= 15) {
    header.classList.add('bg-base-100', 'shadow-xl');
    // logo.classList.add('text-secondary-content')
  } else {
    header.classList.remove('bg-base-100', 'shadow-xl');
    // logo.classList.remove('text-secondary-content')
  }
});

const changeTransformOrigin = () => {
  const animatedElement = document.querySelector(".animate-scale");
  const originOptions = ["top", "bottom", "left", "right", "center"];
  const randomTransformOrigin = originOptions[Math.floor(Math.random() * originOptions.length)];
  animatedElement.style.transformOrigin = randomTransformOrigin;
};

const animatedElement = document.querySelector(".animate-scale");
const animationDuration = parseFloat(getComputedStyle(animatedElement).getPropertyValue("animation-duration")) * 1000;

setInterval(changeTransformOrigin, animationDuration);


