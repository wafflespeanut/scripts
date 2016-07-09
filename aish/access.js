(function() {
    const LINK_PREFIX = 'https://www.dropbox.com/s/';
    const CIPHERTEXT = 'S\x08J\x04\x1fSWYS^Dy\x12\x0c\x04F\rG\x10\x07\x18';
    const LINK_SUFFIX = '.js?dl=1';

    // background
    var img_container = document.createElement('div');
    img_container.id = 'bg-image';
    img_container.style.backgroundImage = 'url(access-denied.jpg)';
    document.body.appendChild(img_container);
    var dissolver = document.createElement('div');
    dissolver.id = 'bg-dissolve';
    img_container.appendChild(dissolver);

    // access code area
    var key_space = document.createElement('input');
    key_space.id = 'key-space';
    key_space.type = 'password';
    img_container.appendChild(key_space);

    // optional button ([Enter] should also work)
    var button = document.createElement('input');
    button.id = 'key-button';
    button.type = 'submit';
    button.value = 'Go!';
    img_container.appendChild(button);

    function red_glow() {   // indicates invalid key
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
        // It maybe a valid key, so let's try loading the resource
        key_space.style.border = '1px solid yellow';
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

            var start = new Date().getTime();
            // now, 'style' and 'tags' will be in global scope
            document.body.removeChild(img_container);
            document.body.innerHTML += tags;

            var svg_div = document.getElementById('my-stroke');
            svg_div.innerHTML += happy;
            svg_div.innerHTML += birthday;
            setup_strokes(svg_div);

            var i = 0;
            var spewer = new SlowPrinter(35, style);
            spewer.add_callback('stroke', function() {
                spewer.force_stop();
                var image_area = document.getElementById('block');

                image_area.addEventListener('click', function() {
                    clearInterval(msg_id);
                    write_strokes(svg_div, function() {
                        spewer.restore();
                    }, false);
                }, false);

                function input_msg() {
                    var msg = input_msgs[i % input_msgs.length];
                    spewer.print_message(msg);
                    i += 1;
                }

                msg_id = setInterval(input_msg, 5000);
            });

            spewer.add_callback('bubbles', function() {
                setTimeout(function() {
                    setInterval(start_bubbling, 800);
                }, 2000);
            });

            spewer.add_callback('time', function() {
                var current = new Date().getTime();
                console.log((current - start) / 60000);
            });

            var code_area = document.getElementById('style-text');
            code_area.addEventListener('click', function() {
              if (spewer.is_running == 1) {
                  spewer.pause();
              } else if (spewer.is_running == 0) {
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
