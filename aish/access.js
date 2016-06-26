(function() {
    const LINK_PREFIX = 'https://www.dropbox.com/s/';
    const CIPHERTEXT = 'F\x04J\x18\x03\x0f\x00YXTDy\x12\x0c\x04F\rG\x10\x07\x18';
    const LINK_SUFFIX = '.js?dl=1';

    // background
    var img_container = document.createElement('div');
    img_container.id = 'bg-image';
    img_container.style.backgroundImage = 'url(access-denied.jpg)';
    document.body.appendChild(img_container);
    var dissolver = document.createElement('div');
    dissolver.id = 'bg-dissolve';
    img_container.appendChild(dissolver);

    // access code
    var key_space = document.createElement('input');
    key_space.id = 'key-space';
    key_space.type = 'password';
    img_container.appendChild(key_space);
    var button = document.createElement('input');
    button.id = 'key-button';
    button.type = 'submit';
    button.value = 'Go!';
    img_container.appendChild(button);

    function red_glow() {
        key_space.style.border = '1px solid red';
        setTimeout(function() {
            key_space.style.border = '1px solid green';
        }, 1000);
    }

    // the unbreakable one-time pad!
    function bytewise_xor(ciphertext, key) {
        var text = '';
        if (ciphertext.length != key.length) {
            console.log('Expected a key length of at least ' + ciphertext.length);
            return '';
        }

        for (i in key) {
            xorred = ciphertext.charCodeAt(i) ^ key.charCodeAt(i);
            text += String.fromCharCode(xorred);
            if (xorred < 32 || xorred > 126) {
                console.log("Reached invalid ASCII range! Wrong key?");
                return '';
            }
        }

        return text;
    }

    function get_content() {
        var script = document.createElement('script');
        key_space.style.border = '1px solid yellow';    // checking script in background
        var result = bytewise_xor(CIPHERTEXT, key_space.value);
        if (!result) {
            red_glow();
            return;
        }

        script.src = LINK_PREFIX + result + LINK_SUFFIX;
        document.head.appendChild(script);

        script.onload = function() {
            if (typeof tags == 'undefined' || typeof style == 'undefined') {
                console.log('Definitely wrong key!');
                document.head.removeChild(script);
                red_glow();
                return;
            }

            // now, 'style' and 'tags' will be in global scope
            document.body.removeChild(img_container);
            document.body.innerHTML += tags;
            let spewer = new SlowPrinter(0, style);

            window.addEventListener('click', function() {
              if (spewer.is_running) {
                spewer.pause();
              } else {
                spewer.resume();
              }
            }, false);
        };
    }

    button.addEventListener('click', get_content, false);
    key_space.addEventListener('keypress', function(e) {    // ENTER
        if (e.keyCode == 13) {
            get_content();
        }
    }, false);

}).call(this);
