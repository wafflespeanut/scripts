---
layout: post
published: false
title: "Exploring the human genome (Part 1)"
date: 2017-02-11 23:24:29 +0530
comments: true
categories:
---

It's been 3 months since I've blogged. *A lot* can happen in 3 months. Someone who was once close to you could leave you out of boredom, your dad could no longer work, you could get to the point when you'll no longer be able to get your bachelor's degree, etc. In the midst of this, wonderful things can happen too - you could get invited to the awesome [Mozilla "All Hands!"](https://wiki.mozilla.org/All_Hands/2016_Hawaii), where you get to see [all kinds of interesting people](https://www.flickr.com/photos/mozillaallhands/sets/72157673850712094/with/31521175206/) from allover the world, you get to hang out with some of them, you get to live with them for a week, FUN!!! [^1]

You see? Balance!

Anyway, you may already know that [my work in bioinformatics](https://wafflespeanut.github.io/blog/2016/07/12/new-job-new-field/) is mostly, well, *research*. All these months, I've been writing little tools in Rust (things that help speed up some *boringly* hard analysis). These days, I'm involved in something new, something very interesting! Before we get into that, I'll try to give a general overview of the flow of data (without going way too much biology), what kinds of data we deal with, how we analyze it, where I come in, etc.

<!-- more -->

## Preamble - Reading the DNA

I'm sure you already have an idea about the DNA - the double helix thing, a bunch of ATCGs, the genetic code, the basis of life, etc. We don't have to go into the details, but well, here's a better story for you. To begin, we should go *deeper*, all the way down to the nucleus of a cell.

In there (for humans), we'll find 23 pairs of wiggly thingies (chromosomes, if you want). That's where we'll also find the tightly packed and coiled DNA strand. Each chromosome has a specific set of nucleotides (ACTGs) and are labeled based on their size - one has ~250 million of them, and so it's "Chr. 1", another one has ~50 million of them, and so it's "Chr. 22".[^2] When we say "human genome", we mean the whole thing, starting from the first base of the first chromosome to the last base of the last chromosome.

Even though the DNA is very small, it's rather *long* in its scale. If the size of each nucleotide is around 3Å, then there are ~3 billion of them in total, which means if you stretch the DNA end-to-end, then it will span about 3 meters! So, every cell in your body has ~1 meter of DNA.[^3] Your body [has about 10 trillion cells](https://biology.stackexchange.com/q/3327/3446) and if they produce a DNA in every cycle, then your body alone [produces a light year of DNA](https://calculatedimages.blogspot.in/2015/04/light-years-of-dna.html) in your lifetime! More importantly, that's *almost* the same copy of DNA that began in the embryo.

*... which is a lot!*

We know that the DNA is the basis of all the wonderful mechanisms going on inside, so the first step is to *read* the DNA. That's what we call *sequencing*. It wasn't easy about a decade back, but now, sequencing technologies have improved.

Anyway, the basic process goes something like this. A sample (say, from blood, or liver) goes through a complex preparation and gets loaded into the sequencing machine. Since there are only 4 bases and they bind only with their *mate* (A to T, or C to G, and vice versa), reading a single helix is enough (as we can always *deduce* that if one side was "ATTG...", then the other side would be "TAAC...").

Firstly, the double helix is [unwound](https://en.wikipedia.org/wiki/Nucleic_acid_thermodynamics#Denaturation) and individual strands are separately sequenced. As we're still in the molecular level and identifying the bases is *tough* (limited by our instruments' sensitivity), the sequence is amplified [by making huge copies](https://en.wikipedia.org/wiki/Polymerase_chain_reaction). All you need is a suitable environment and a bunch of [additional ATCGs](https://en.wikipedia.org/wiki/Primer_(molecular_biology)) to stick to the chain.

The interesting catch here is that the sample won't be a straight strand during the process. **It should be split into numerous sequences** (mostly 100 or 1000 bases) and laid into multiple container-like thingies (called *lanes*), and they're are individually collectively amplified. [Special ATCGs](https://en.wikipedia.org/wiki/Dideoxynucleotide) are then used to stop the amplification, which either light up (by fluorescing a color for each base) and a snapshot is taken, or passed through an electrode, where the voltage is recorded. All of these are easier said than done.

[^1]: Well, you could also get allergic to sea food (lobster, in my case) and get "hives", but *meh*...

[^2]: Then, there's the X and Y chromosomes which determine sex.

[^3]: Actually, it's every cell with a nucleus. That's because not all cells have a nucleus - even though the red blood cells, the cells in hair, skin, nail, etc. start with a nucleus (with a DNA), they destroy their nucleus as they mature.
