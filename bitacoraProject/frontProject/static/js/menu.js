/* Set the width of the sidebar to 250px and the left margin of the page content to 250px */
function openNav() {
    var mq = window.matchMedia( "(mim-width: 450px)" );
  if (mq.matches) {
    document.getElementById("mySidebar").style.width = "250px";
    document.getElementById("main").style.marginLeft = "250px";
  }
  else {
    document.getElementById("mySidebar").style.width = "250px";
    document.getElementById("main").style.marginLeft = "50px";
  }
  
}

/* Set the width of the sidebar to 0 and the left margin of the page content to 0 */
function closeNav() {
  document.getElementById("mySidebar").style.width = "0";
  document.getElementById("main").style.marginLeft = "0";
}

