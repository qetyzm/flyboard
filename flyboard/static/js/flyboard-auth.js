function initAuth(messages, urls) {
    $('.logout-button').click(function(){
        $.ajax({
            url: urls['auth.logout'],
            type: "POST",
            success: function() {
                location.reload();
            },
            error: function(response) {
                alert(messages["something_went_wrong"])
            }
        })
    });

    $('#login-btn').click(function() {
        let username = $('#login-username-input').val();
        let password = $('#login-password-input').val();

        if (!username) {
            alert(messages["username_please"]);
            return;
        } else if (!password) {
            alert(messages["password_please"]);
            return;
        }

        let loginData = {
            "username": username,
            "password": password
        }

        $.ajax({
            url: urls['auth.login'],
            type: "POST",
            contentType: "application/json",
            dataType: "json",
            data: JSON.stringify(loginData),
            success: function(response) {
                if (response['valid'] == false) {
                    alert(response['message']);
                    return;
                }
                location.reload();
            },
            error: function(response) {
                alert(messages["something_went_wrong"])
            }
        });
    });
}