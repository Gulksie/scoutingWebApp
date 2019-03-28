//main file for javascript functions

//expand and retract hamburger menu in header on mobile
function changeHamburger() {
    var x = document.getElementById("navBarMobile");
    if (x.style.display === "block") {
        x.style.display = "none";
    } else {
        x.style.display = "block";
    }
}