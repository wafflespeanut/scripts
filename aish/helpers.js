const INTER_STROKE_DELAY = 150;
const BUBBLE_TIME = 1000;
const BUBBLE_SCALE_FACTOR = 400;

function start_bubbling() {
    var color = 'rgb(' + Math.floor(Math.random() * 255) + ','
                       + Math.floor(Math.random() * 255) + ','
                       + Math.floor(Math.random() * 255) + ')';

    var x = Math.floor(Math.random() * window.innerWidth);
    var y = Math.floor(Math.random() * window.innerHeight);
    var timeout = 200;

    var bubble = document.createElement('div');
    document.body.appendChild(bubble);
    bubble.style.backgroundColor = color;
    bubble.style.left = x + 'px';
    bubble.style.top = y + 'px';
    bubble.className = 'bubble';

    setTimeout(function() {
        bubble.style.transform = 'scale(' + BUBBLE_SCALE_FACTOR + ')';
    }, timeout);

    timeout += BUBBLE_TIME;
    setTimeout(function() {
        bubble.style.opacity = 0;
    }, timeout);

    timeout += BUBBLE_TIME;
    setTimeout(function() {
        document.body.removeChild(bubble);
    }, timeout);
}

// compute the time taken to draw strokes and set necessary attributes for transitioning later
function setup_strokes(node) {
    var delay = 0;
    var trans_timeout = 0;
    var paths = node.querySelectorAll('path');

    for (i = 0; i < paths.length; i++) {
        var length = paths[i].getTotalLength();
        delay += trans_timeout + INTER_STROKE_DELAY;
        trans_timeout = Math.floor(length);
        // so that no dash drawing is performed initially
        paths[i].style.strokeDashoffset = length;
        // ... and nothing's visible (given the spacing)
        paths[i].style.strokeDasharray = length + ',' + length;
        paths[i].style.transition = 'stroke-dashoffset ' + trans_timeout + 'ms ' + delay + 'ms linear';
    }

    paths[paths.length - 1].delay = delay;
}

function write_strokes(node, callback, call_on_end) {
    var paths = node.querySelectorAll('path');

    for (i = 0; i < paths.length; i++) {
        paths[i].style.strokeDashoffset = 0;
    }

    if (call_on_end) {
        // final delay for executing the callback after the strokes are drawn
        setTimeout(callback, paths[paths.length - 1].delay);
    } else {
        callback();
    }

}
