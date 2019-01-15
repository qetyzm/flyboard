let minThreadFileAmount = 0;
let maxThreadFileAmount = 4;
let fileCounter = 0;

$(document).ready(function() {
    function makePassword() {
        var text = "";
        var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-=_+[]{};':\",./<>?\\|";

        for (var i = 0; i < 16; i++) {
            text += possible.charAt(Math.floor(Math.random() * possible.length));
        }

        return text;
    }

    $('.cloak').click(function(e) {
        if (e.target != this) {
            return;
        }

        $('.cloak').hide();
    })

    $('.login-button').click(function() {
        $('.cloak').show();
    });

    // Start new thread button action
    $('#start-thread-link').click(function() {
        $('#start-thread-wrapper').hide();
        $('#no-thread-wrapper').show();
        $('#new-thread-creator').show();
    });

    $('#no-thread-link').click(function() {
        $('#start-thread-wrapper').show();
        $('#no-thread-wrapper').hide();
        $('#new-thread-creator').hide();
    });

    // Add BBCode tags
    function addTag(tag) {
        let selection = $('#message-input').getSelection();
        let text = $('#message-input').val();

        $('#message-input').val(
            text.slice(0, selection.start) + "[" + tag + "]" + selection.text + "[/" + tag + "]" + text.slice(selection.end)
        );
    }

    // BBCode buttons
    $('#bold-btn').click(function() {
        addTag("b");
    });
    $('#italic-btn').click(function() {
        addTag("i");
    });
    $('#underline-btn').click(function() {
        addTag("u");
    });
    $('#code-btn').click(function() {
        addTag("code");
    });
    $('#spoiler-btn').click(function() {
        addTag("spoiler");
    });

    // Clear button
    $('#clear-btn').click(function() {
        $('#name-input').val("");
        $('#email-input').val("");
        $('#subject-input').val("");
        $('#message-input').val("");
        $('#embed-input').val("");
    });

    // Save password on change
    $('#password-input').change(function() {
        let password = $('#password-input').val();
        Cookies.set("user_password", password);
    });

    // Generate password cookie if none
    $('#password-input').val(function() {
        let passwordCookie = Cookies.get("user_password");
        
        if (!passwordCookie) {
            let password = makePassword();
            Cookies.set("user_password", password);
            return password;
        } else {
            return passwordCookie;
        }
    });

    function loadButtons() {
        $('#image-btn-separator').hide();
        if (fileCounter <= minThreadFileAmount) {
            $('#add-image-btn').show();
            $('#remove-image-btn').hide();
        } else if (fileCounter >= maxThreadFileAmount) {
            $('#add-image-btn').hide();
            $('#remove-image-btn').show();
        } else if (fileCounter == maxThreadFileAmount) {
            $('#add-image-btn').hide();
            $('#remove-image-btn').hide();
        } else {
            $('#image-btn-separator').show();
            $('#add-image-btn').show();
            $('#remove-image-btn').show();
        }
    }

    // Add image
    $('#add-image-btn').click(function() {
        fileCounter++;
        let fileBoxId = "#file-box-" + fileCounter;

        $('<div/>', {id: fileBoxId, class: "file-box" }).insertBefore('#image-buttons');
        
        $('<input/>', {
            type: "file",
            id: "file-input-" + fileCounter,
        }).appendTo('.file-box:nth-of-type(' + fileCounter + ')');
        $('<input/>', {
            type: "checkbox",
            id: "image-" + fileCounter + "-spoiler-checkbox",
        }).appendTo('.file-box:nth-of-type(' + fileCounter + ')');
        $('<label for="image-' + fileCounter +'-spoiler-checkbox">Spoiler image</label>').appendTo('.file-box:nth-of-type(' + fileCounter + ')');

        loadButtons();
    });

    $('#remove-image-btn').click(function() {
        $('#image-buttons').prev().remove();
        fileCounter--;
        loadButtons();
    });

    loadButtons();

    for (var i = 0; i < minThreadFileAmount; i++) {
        $('#add-image-btn').click();
    }

    $('#new-thread-creator').hide();
    $('#no-thread-wrapper').hide();
});