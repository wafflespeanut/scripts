---
layout: post
title: "Drawing an ASCII sketch"
date: 2017-02-28 18:46:53 +0530
comments: true
categories: [Python, Coding, Leisure]
---

Every once in a while, I get a (seemingly) nice and interesting idea (thanks to a wonderful female creature, who's always been my *muse*), and whenever I get one, I go straight to researching more about it, allocating most of my free time, so that I finish it up ASAP and show it to her. Last time, it was a [CSS spewing thingy](https://github.com/Wafflespeanut/AISH). This time, it was about generating an ASCII sketch of the image input.

I'm sure you'd have seen all those "Image to ASCII converter", "ASCII art generator", and all sorts of boring variants of this online. But, I'll tell you where they all fail and how I managed to bring up a decent sketch in ASCII. It took me about 3 hours to come up with a basic sketch, and then a few more for making it more generic and [launching it in Heroku](https://ascii-gen.herokuapp.com/).

<!-- more -->

## Mapping ASCII values over RGB

Let's say I want to draw the ASCII sketch of this JPEG image...[^1]

![sample](/images/ascii/sample.jpg)

I always tend to hack on stuff with Python. And, it has an [amazing image library](https://en.wikipedia.org/wiki/Python_Imaging_Library) to play with images. In Python, we can do something like this,

{% highlight python %}
>>> from PIL import Image
>>> img = Image.open('sample.jpg')
>>> px = img.load()
>>> px[0, 0]
(72, 94, 91)
{% endhighlight %}

So, we now have all those 3-tuple RGB values in a 2D array. The first step would be to convert these RGB values to intensities[^2] (i.e., *grayscale*, since the final ASCII art will look very similar to its grayscale version). It's [very easy](https://en.wikipedia.org/wiki/Grayscale#Luma_coding_in_video_systems), and PIL eases this a bit more,

{% highlight python %}
>>> img = img.convert('L')
>>> px = img.load()
>>> px[0, 0]
87
{% endhighlight %}

Next stop is to have a bunch of characters sorted with respect to their pixel densities (like `' '` (space) for white, `'.'` (dot) for gray, `'#'` for black and so on), and simply map these characters over the grayscale image. Once we have the character map, we can do something like this...

{% highlight python %}
>>> width, height = img.size
>>> for j in xrange(height):
...     print ''.join(CHARS[px[i, j] % len(CHARS)] for i in xrange(width))
{% endhighlight %}

Looks very simple, right?

Now, all we need to do is find `CHARS` (the character map). I found a [wonderful implementation](https://github.com/ajalt/pyasciigen/blob/48a5e5ffa5d2ab28637a4724e5b1ce0609b982dd/asciigen.py#L84) for sorting the characters. Just what I wanted. It loads the printable characters, draws them in an image, and sorts them according to the pixel density of their render. This means, "space" has zero pixels (for example), and so it will be the first thing you'll find in the sorted list.

Let's see how our image turns out using this mapping...

![screwed](/images/ascii/screwed.png)

That's pretty screwed up. *Bad luck, huh?*

This is because most of the images we find everyday have a wide variety of gradients allover them. We don't see all of them, because they're gradients of different colors. In this case however, since we've converted them to grayscale intensities, different gradients overlap, and we get this intense *spew* of **all** the gradients!

People work around this by clamping ranges of values to some character instead of using the entire ASCII table (like, the color range "light gray to white" all map to "space"). But, that's still a workaround. It doesn't help much.

Let's see if we can tune this, by extracting necessary details from the image.


[^1]: Okay, I know what you're thinking, but FYI, that's definitely *not* the girl I talked about!

[^2]: We *can* however use the color data to get weighted colors and apply them over the final ASCII values, but meh...
