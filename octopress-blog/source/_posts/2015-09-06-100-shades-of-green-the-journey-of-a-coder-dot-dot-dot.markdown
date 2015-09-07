---
layout: post
title: "100 shades of green: The journey of a coder..."
date: 2015-09-07 18:33:18 +0530
comments: true
categories: Coding
---

I've been involved in coding for about a year now. I've danced with Python *(a lot!)* and nowadays, I'm playing with Rust, although I've also done some basic C & Javascript. Anyways, I get a lot of questions from my fellow undergrads about how I got into coding in the first place, and yesterday, [Manish](https://manishearth.github.io/) gave me the idea to blog about it. Since my commit streak has also reached 100 days (with 1001 commits), I think now's a great time to share my story with y'all...

<small>On a side note, this post is intended for those readers who've barely seen a computer in their school days (like me), though I assure you it will be interesting for others as well.</small>[^1]

<!-- more -->

## Good ol' days with the computer...

When I got my first computer, all I ever wanted to do was play games. Apart from that, I loved to paint (you know, lines, squares, circles, colors, wheee...). Though I did encounter C in my school days, I didn't know the purpose of it, because I simply didn't realize the powers of coding. The only thing that attracted me was HTML (4), because it can do some pretty stuff - by that way, I realized that a bunch of characters can actually *make* colors in a computer.

I discovered many things during my high school days, but the only thing that mattered the most was that characters in computers can do more than just coloring - that was the time when I played with matrices and generated prime numbers in C (basic stuff you learn in high-school). That was also the time when I had developed this weird desire to fiddle around the things which are hidden from plain sight. I just don't like it that way.

For instance, take the beautiful "Microsoft Windows XP" (the OS of my first computer) - the `C:\\` drive is forbidden by default, and it has a lot of files which are unknown to me. I had a friend who shared my trait of fiddling around with unknown files. Since his father owned an internet cafe, whenever we're lost, or screw up something (or get screwed up by a virus), we get a solution almost immediately. Later, we take those problems to our school, so that we can screw up the computers in our labs (because our teachers were quite despicable!).

That was the time when we also got interested in the command prompt (which I terribly hate nowadays). As an example, this tiny snippet which recursively walks inside a path and hides the contents was used often by us to drive the teachers and students crazy (for a month!).[^2]

``` bat
attrib [path] +h +r +s /s /d
```

## As a newbie to the internet...

It wasn't until college when I got my first laptop along with a *pathetic* excuse for an internet connection. By the end of my first year, a great deal of things had happened.

I got into Stack Exchange, [which had some great impacts on my personality](http://wp.me/p3OCmi-D) over the years. At the start, I had the motivation to explore the system, interact with a lot of users, and learn to contribute, but once that became handy, I got bored. Yeah, reading stuff in the internet, participating in a great community is awesome and all, but I needed something more - something that could keep me equipped when I'm bored of reading.

I got excited about math and wanted to solve problems - it was right about time when I discovered [Project Euler](https://projecteuler.net/). It demanded the users to code to solve the problems. I'm sure every newbie coder gets interested in those problems, because it demands only the solution for a particular problem, which means you should first guess an algorithm (mostly bruteforce), try to implement it (when you learn more about the language - with the help of [Stackoverflow](https://stackoverflow.com/), of course), get the answer and then you can refine the algorithm (unlike SPOJ or Code Chef, which are designed to concentrate more on algorithms and data structures). In those days, I used C.

My sophomore year began with [blogging](https://wafflescrazypeanut.wordpress.com) - when I was mostly writing about physics-ish stuff or my favorite experiences (or ranting about something). At this point, I got to know about *Mathematica* and its glories. Luckily, the Wolfram community has offered plenty of documentation for it, that I was able to learn its basics pretty quickly. Now, I had no reason to use C for solving the problems, since *Mathematica* had all the built-in functions available in hand. I used it to generate plots and some simple animations, which I later embedded in my blog posts. One thing led to another and soon, I was making animations for teaching my classmates to visualize things.[^3]

Later, I got fond of a markup language - which affected me so much, that I got addicted to just see its *beauty*. It was the awesome LaTeX! I used to prepare notes for some of my courses, just because I felt happier to read all those silly formulas in LaTeX. Once I got to know about its clockworks, I began using [LyX](http://lyx.org) and [Geogebra](http://geogebra.org) to speed things up.

## Into an easy, aesthetic, powerful, interpreted language...

Along the way, I discovered Github. I didn't understand the point of it at first, and so I assumed it as a "dropbox for coders" - I never imagined the concept of version-control or open-source. Anyways, the repositories served nicely as a *backup place* for all my code.

I'm a *perfectionist*, alright? I admire the beauty of things when they're neat, but I often struggle to maintain their clean state as time progresses. Since I realized that LaTeX seemed to consume most of my time, note-taking also finally came to an end. And, *Mathematica* (the only language I was currently working with) seemed too abstract, since it hides the details from my view. Now, I wanted to know how things work behind the cloak, but I also don't wanna fall back to C. *(meh)*

When I was a sophomore, I hang out a lot in our h-bar chatroom and most often, I could hear about Python. When I asked about it, they told me that the scientific community is using Python most of the time (from handling the data to plotting the results), especially because it's easy. *"Hmm, looks like something I should try out..."*, and I got curious like that.

By then, I somehow got interested in cryptography. After reading about the [Caesar](https://en.wikipedia.org/wiki/Caesar_cipher) & [Vigènere](https://en.wikipedia.org/wiki/Vigenère_cipher) ciphers, I got a desire to create my own cipher (that often happens if you get too excited about cryptography), and that little stunt consumed the whole vacation of my sophomore year. This is the point where an endless discovery was going on. As days passed, some new idea keeps popping up, and I immediately implemented it. Man, I was totally productive! As a free perk, I also translated the code to Javascript (by which I learned some HTML5, JS along with a bit of CSS). This is also where my life as a coder began...



[^1]: If you had grown in my locality (in your childhood), then all you know is that a computer (which you often see in school) is *"something"* where you can only type, draw, and play games - nothing more! Our books said that Charles Babbage was the "father of computer", and so we thought he's the one who made this thing. I'm not embarrassed to say that we were never curious!

[^2]: We learned that from a virus (and that too because we never believed in the concept of an anti-virus (since everything is just the cause & effect of code). This command is often utilized by a harmless worm which infects pen drives.

[^3]: It was required for a course, where we draw instantaneous vector diagrams of parts of machines. I had even [made some (not so bad) videos](https://www.youtube.com/playlist?list=PLpqCCxmTKpa1NBYfoEJlKb8X4fq0Pf6N9) for the junior undergrads using those animations.
