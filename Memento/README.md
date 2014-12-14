Souvenir (v2.1)
======

This is a little project of mine. An utility to remember everyday memories. For now, it puts your stories in branched directories for later viewing. And, it supports encryption. I've used a simple algorithm (which is less secure, but enough for our purpose) to hex and shift the ASCII values in the files.

Once stored, it doesn't disturb the original story. It decrypts to a temporary file for viewing, which gets deleted in a few seconds. The same goes for updating on the same day - It decrypts to TEMP, appends your story, and finally overwrites the previous story.

It also supports viewing random stories.