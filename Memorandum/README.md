## Memorandum (v2.2)

This is a little project of mine. An utility to remember everyday memories. For now, it puts your stories in branched directories for later viewing. And, it supports encryption. I've used a simple algorithm (which is less secure, but enough for this purpose) to hex and shift the ASCII values in the files. It can also detect incorrect passwords.

Once stored, it doesn't disturb the original story. It decrypts to a temporary file for viewing, which gets deleted in two seconds. The same goes for updating on the same day - It decrypts to TEMP, appends your story, and finally overwrites the previous story.

I've added a function that hexes the password into a local file if you get bored of typing the password each time you write/view some story. It also supports viewing random stories...

### Changelog

v2.2: Memorandum
- Passwords can be stored locally (after 10-layer hexing)
- Write stories for someday you've missed
- Sign-in / Sign-out options for easier use
- Functions: check(), diary()

v2.1: [Souvenir](https://github.com/Wafflespeanut/Python/tree/937d48dc3bc8608530253fc392594a90a4d59078/Memento)
- View random stories
- TEMP is deleted after a timeout (to keep things safe)
- One-time password for updating stories
- Fixed a faulty code in encryption
- Can detect incorrect passwords
- Functions: random(), temp(), protect()

v2.0: [Memento](https://github.com/Wafflespeanut/Python/tree/7f2572857bbe86b2598d27ab7872017a580351ff/Memento) *(has some bugs)*
- Added a simple encryption method which hexes and shifts the ASCII values (to make it really "private" - further protection is of your own)
- Added a function for viewing stories on a given day
- A TEMP file is created for viewing/updating any story, leaving the original files undisturbed
- Functions: hexed(), char(), zombify(), shift(), protect(), write()

v1.0: [Private Diary](https://github.com/Wafflespeanut/Python/tree/64a9c8dd2470ec309a439a41568778187bbe8bb7/Private%20Diary)
- Creates timestamped folders and text files for stories
- Writes the stories for every [RETURN] stroke, which indicates a paragraph
- Functions: new(), diary()