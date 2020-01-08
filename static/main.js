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

//sign in and out stuff
//these should error on non login pages
function signOut() {
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function () {
        console.log('User signed out.');
    });

    var xrequest = new XMLHttpRequest()
    xrequest.open("GET", "/logout")
    xrequest.onload = function () {
        window.open(xrequest.responseURL, "_self")
    }
    xrequest.send()
}

function onLoad() {
    gapi.load('auth2', function () {
        gapi.auth2.init();
    });
}