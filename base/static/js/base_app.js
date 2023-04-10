const themeButtons = document.querySelectorAll('[data-set-theme]');
          
themeButtons.forEach(function(button) {
  button.addEventListener('click', function () {
    const newTheme = this.getAttribute('data-set-theme');
    document.documentElement.setAttribute('data-theme', newTheme);

    themeButtons.forEach(function(otherButton) {
      const activeClass = otherButton.getAttribute('data-act-class');
      if (otherButton === button) {
        otherButton.classList.add(activeClass);
      } else {
        otherButton.classList.remove(activeClass);
      }
    });
  });
});

const header = document.getElementById('navBar')
const logo = document.getElementById('primary-logo')

window.addEventListener('scroll', function () {
  const currentScrollTop = window.pageYOffset || document.documentElement.scrollTop;
  
  if (currentScrollTop >= 15) {
    header.classList.add('bg-base-100', 'shadow-2xl');
    logo.classList.add('text-primary')
  } else {
    header.classList.remove('bg-base-100', 'shadow-2xl');
    logo.classList.remove('text-primary')
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

// get the progress bar element
const progressBar = document.getElementById("progress").querySelector(".bg-primary");

// show the progress bar when a new page starts loading
document.addEventListener("DOMContentLoaded", () => {
  progressBar.style.width = "0%";
  progressBar.parentElement.parentElement.style.display = "block";
});

// hide the progress bar when the page finishes loading
window.addEventListener("load", () => {
  progressBar.parentElement.parentElement.style.display = "none";
});

// update the progress bar as the page loads
document.addEventListener("readystatechange", () => {
  if (document.readyState === "loading") {
      progressBar.style.width = "10%";
  } else if (document.readyState === "interactive") {
      progressBar.style.width = "50%";
  } else if (document.readyState === "complete") {
      progressBar.style.width = "100%";
  }
});