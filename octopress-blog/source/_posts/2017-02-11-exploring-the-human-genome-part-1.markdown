---
layout: post
title: "Exploring the human genome (Part 1)"
date: 2017-02-11 23:24:29 +0530
comments: true
categories:
---

It's been 3 months since I've blogged. *A lot* can happen in 3 months. Someone who was once close to you could leave you, your dad could lose his job (trembling your financial support), you could get to the point when you'll no longer want your bachelor's degree, etc.

In the midst of this, wonderful things can happen too - you could get invited to the awesome [Mozilla "All Hands!"](https://wiki.mozilla.org/All_Hands/2016_Hawaii), where you get to see [all kinds of interesting people](https://www.flickr.com/photos/mozillaallhands/sets/72157673850712094/with/31521175206/) from allover the world, you get to hang out with some of them, you get to live with them for a week, FUN!!! [^1] Once you get back, you get the promise of a *superior* distraction - a nice little project that could keep you distracted for months!

You see? Balance!

Anyway, you may already know that [my work in bioinformatics](https://wafflespeanut.github.io/blog/2016/07/12/new-job-new-field/) is mostly, well, *research*. All these months, I've been writing little tools in Rust (things that help speed up some *boring* analysis). These days, I'm involved in something new, something very interesting! Before we get into that, I'll try to give a general overview of the flow of data (without going way too much biology), what kinds of data we deal with, how we analyze it, where I come in, etc.

<!-- more -->

## Preamble - Reading the DNA...

I'm sure you already have an idea about the DNA - the double helix thing, a bunch of ATCGs, the genetic code, the basis of life, etc. We don't have to go into all the details, but well, here's a better story for you. To begin, we should go *deeper*, all the way down to the nucleus of a cell.

In there (for humans), we'll find 23 pairs of wiggly thingies (chromosomes, if you want). That's where we'll also find the tightly packed and coiled DNA strand. Each chromosome has a specific set of nucleotides (ACTGs) and are labeled based on their size - one has ~250 million of them, and so it's "Chr. 1", another one has ~50 million of them, and so it's "Chr. 22".[^2]

A genome is a collection of all the genes. A gene is just a sequence of bases used to manufacture a protein (more on this next time). When we say "human genome", we mean the whole thing, starting from the first base of the first chromosome to the last base of the last chromosome, which contains all the genes necessary for a human being.

Even though the DNA is very small, it's rather *long* in its scale. If the size of each nucleotide is around 3Å, then there are ~3 billion of them in total, which means if you stretch the DNA end-to-end, then it will span about 1 meter! So, every cell in your body has ~1 meter of DNA.[^3] Your body [has about 10 trillion cells](https://biology.stackexchange.com/q/3327/3446) and if they produce a DNA in every cycle, then your body alone [produces a light year of DNA](https://calculatedimages.blogspot.in/2015/04/light-years-of-dna.html) in your lifetime! More importantly, that's *almost* the same copy of DNA that began in the embryo.

*... which is a lot!*

We know that the DNA is the basis of all the wonderful mechanisms going on inside, so the first step is to *read* the DNA. That's what we call *sequencing*. The basic process goes something like this. A sample (say, from blood, or liver) goes through a complex preparation and gets loaded into the sequencing machine. Since there are only 4 bases and they bind only with their *mate* (A to T, or C to G, and vice versa), reading a single helix is enough (as we can always *deduce* that if one side was "ATTG...", then the other side would be "TAAC...").

Firstly, the double helix is [unwound](https://en.wikipedia.org/wiki/Nucleic_acid_thermodynamics#Denaturation) and individual strands are separately sequenced. As we're still in the molecular level, identifying the bases is *tough* (limited by the sensitivity of our instruments), and so, the sequence is amplified [by making huge copies](https://en.wikipedia.org/wiki/Polymerase_chain_reaction). All you need is a suitable environment and a bunch of [additional ATCGs](https://en.wikipedia.org/wiki/Primer_%28molecular_biology%29) to stick to the chain.

The interesting catch here is that the DNA sample won't be a single straight strand during the process. **It should be split into numerous sequences** (ranging from 100 to a few thousand bases) and laid into multiple container-like thingies (*lanes*), where they're *individually* amplified and *collectively* sequenced. Now, [special ATCGs](https://en.wikipedia.org/wiki/Dideoxynucleotide) are used to stop the amplification, which light up (by fluorescing a color for each base) as they attach themselves to a particular nucleotide. Sensitive photoelectric devices are then used to take snapshots of these lights in the lanes.

Each color indicates the presence of the corresponding nucleotide, and *voila!* DNA sequencing! Here's a [wonderful TED lesson](https://www.youtube.com/watch?v=MvuYATh7Y74) to visualize this.

## The Reference Genome

Remember that we had to slice the DNA into fragments? Once the sample has been *read*, the sequencing machine generates a [FASTQ](https://en.wikipedia.org/wiki/FASTQ_format) file, which looks something like this,

    $ head -8 demo_blood.fastq
    @ERR009127.307 IL22_2005:8:1:5:1941 length=36
    GCAGACCCAGCGGGGCATGGGCGGACAGAGCCGCAC
    +
    <B?<@BB>>3BB>))<>43)94@=11=A?@=@B:/-
    @ERR009127.308 IL22_2005:8:1:5:944 length=36
    GGCGAACGCTTCGCTGGCCATTTAGGAGCTCTGCTC
    +
    B@AAAA=ABBB@B@BBB><;<A;<9<<;<;=<A;;3

Every 4 lines in this file is a "read". People are usually interested in the second line (the sequence fragment) and the fourth line (the ASCII-encoded quality of individual bases) in each read. The [quality score](https://en.wikipedia.org/wiki/Phred_quality_score) is much like the machine's confidence on a particular base.

For example, the last base in the first sequence "C" has a value 45 ('minus' in ASCII) whereas in the second sequence, it's 51 (number '3' in ASCII), which means we're relatively more confident about "C" in the second sequence. The scale is logarithmic and so, you can't expect an ASCII value more than 100 to show up all the time in reality.

Even though we've done so much to get this FASTQ file, it won't be of any use by itself, since it doesn't have the necessary information like where the particular sequence *was* in the sample, which means we've no idea what gene we're looking at, which isn't really useful.

So, we should reconstruct the DNA!

[Assembly of DNA](https://en.wikipedia.org/wiki/Sequence_assembly) is a *big deal*, because you have to figure out where a sequence belongs to. It's like shredding a novel into bits of paper (which contain nothing more than a few words) and re-creating it back from the bits. This takes a *long* time! And, it's error-prone. Years have passed since [the first attempt](https://en.wikipedia.org/wiki/Human_Genome_Project), and yet, we don't know some parts of our own genome.

Building a DNA from the FASTQ file every time we read a sample would be rather *silly*. So, people have spent years to land on a basic template DNA. This is called the *reference genome*. It's incomplete, but it's accurate enough. Every species has its own reference genome. The human's is the largest - [a horrible 3GB file!](http://hgdownload.cse.ucsc.edu/downloads.html#human) It serves as a template because all humans share more than 99% of the genome. In other words, we differ only by a few million bases.

This is what the reference genome looks like...

    $ head -5 ~/data/BWAIndex/hs37d5.fa
    >chr1 dna:chromosome chromosome:GRCh37:1:1:249250621:1
    NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
    NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
    NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
    NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN

It begins with "chr1" indicating the first chromosome (and its range - 1 to 249,250,621). Note that it begins with a lot of Ns. "N" indicates that we've no idea what base occupies that position (like I said, parts are still incomplete). Let's seek to a span with some data...

    $ sed -n '200,204p' ~/data/BWAIndex/hs37d5.fa
    TCAGCCTTTTCTTTGACCTCTTCTTTCTGTTCATGTGTATTTGCTGTCTCTTAGCCCAGA
    CTTCCCGTGTCCTTTCCACCGGGCCTTTGAGAGGTCACAGGGTCTTGATGCTGTGGTCTT
    CATCTGCAGGTGTCTGACTTCCAGCAACTGCTGGCCTGTGCCAGGGTGCAAGCTGAGCAC
    TGGAGTGGAGTTTTCCTGTGGAGAGGAGCCATGCCTAGAGTGGGATGGGCCATTGTTCAT
    CTTCTGGCCCCTGTTGTCTGCATGTAACTTAATACCACAACCAGGCATAGGGGAAAGATT

## Stitching the DNA...

Our *quest* is always to answer questions like, "Where the changes have happened?", "Why they happened there?", "Does/Doesn't it cause any disease/disorder?", etc. Now that we have a digital version of the reference genome, the next checkpoint is to [align](https://en.wikipedia.org/wiki/Sequence_alignment) the reads from our FASTQ file to the reference.

This is where things get a bit more interesting, because it's a string searching problem, and an [approximate one](https://en.wikipedia.org/wiki/Approximate_string_matching) in that.

[^1]: Well, you could also get allergic to sea food (lobster, in my case) and get "hives", but *meh*...

[^2]: Then, there's the X and Y chromosomes which determine sex.

[^3]: Actually, it's every cell with a nucleus. That's because not all cells have a nucleus - even though the red blood cells, the cells in hair, skin, nail, etc. start with a nucleus (with a DNA), they destroy their nucleus as they mature.
