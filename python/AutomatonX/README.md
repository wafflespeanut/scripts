## AutomatonX (v0.3.0)

Well, this is my cipher, built completely for (my own) learning purposes. For a few months, I've been learning Python by finding different ways of getting into the cipher, and patching the algorithm so that it gets stronger every time.

It's quite straight-forward (should be easy to understand with my comments). And, it's built by a lot of helper functions, for improving readability. I've written a [blog post](http://wp.me/p3OCmi-qT) on how one of its ancestors (v0.1.4 "Ranger") works. And, there's also a [javascript version](http://wafflespeanut.github.io/scripts/site-old/sentinel/) of it in my Github page!

### Note: I don't update this anymore!

I had a course in cryptography lately. Only then I realized that whatever I've done is one of the most *stupidest* encryption scheme that anyone could possibly imagine. I wanted something nice, not a garbage that'd consume a lot of time & memory. So, I quit...

### How it works?

- During encryption, hexing, sorting, addition, iteration, shifting, XOR'ing, all kinds of things are done by the respective helper functions. During decryption, the reverse processes are carried out by the inverse helper functions.

- I've also added a few enhancements of my own, just to make it harder!

- Some 'tries-catches' have been used to print custom messages for possible causes of the errors, instead of the (ugly) errors themselves.
