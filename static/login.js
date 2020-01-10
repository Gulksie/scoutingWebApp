function onSignIn(user) {
    var profile = user.getBasicProfile()

    var toSend = {
        name: profile.getName(),
        email: profile.getEmail(),
        ID: user.getAuthResponse().id_token
    }

    var xrequest = new XMLHttpRequest()
    xrequest.open("POST", "{{ url_for('loginPage') }}")
    xrequest.setRequestHeader("Content-Type", "application/json")
    xrequest.setRequestHeader("Login-Type", "google-signin")
    xrequest.onload = function () {
        window.open(xrequest.responseURL, "_self")
    }
    xrequest.send(JSON.stringify(toSend))
}