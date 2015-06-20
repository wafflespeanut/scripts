## Remembrancer (v0.3.0)

This is a little project of mine - an utility to remember everyday memories. For now, it puts your stories (with a MD5-hashed filename) in a directory for later viewing. It supports some basic encryption. I've used a simple algorithm to hex and shift the ASCII values in the files, which is similar to a *hexed* 256-char Caesar cipher with a byte-wise XOR<sup>[1]</sup>. It can also detect incorrect passwords.

Once stored, it doesn't disturb the original story (unless you play around). It decrypts to a temporary file for viewing, which gets deleted in two seconds. While updating stories, it just appends your story to the previous story.

I've also added a function that hexes the password into a local file, so that instead of typing the password each time you write/view some story, you can save it by signing in. It also supports viewing random stories. And, the cool part - you can search your stories for specific words (between a range of dates). Currently, I'm trying to minimize the time it takes to search. Since Python is high-level, I'm planning to link it to Rust.

<sup>[1]: **It's not at all secure!**. And, that's not my goal either. This is just to prevent people from peeking into the stories using text editors. But, if someone's really involved, then he'll be able to crack it in a few days.</sup>

### Changelog

v0.3.0: Remembrancer
- Smart search for specific words in stories
- Old tree-node method is now deprecated. All stories are now present in the specified directory
- Story names are hashed with MD5 (to obscure the file names).
- Fixed a major flaw in the cipher. All these days, this has been consuming more time & memory. It's now been updated to a mixup of 256-char Caesar and byte-wise XOR.
- Functions: hashed(), hashDate(), write(), diary(), search(), CXOR()

v0.2.2: [Memorandum](https://github.com/Wafflespeanut/Python/tree/8850c831c10955b5c32d2710abfbfef916031792/Memorandum)
- Passwords can be stored locally (after 10-layer hexing)
- Write stories for someday you've missed
- Sign-in / Sign-out options for easier use
- Functions: check(), diary(), day()

v0.2.1: [Souvenir](https://github.com/Wafflespeanut/Python/tree/937d48dc3bc8608530253fc392594a90a4d59078/Memento)
- View random stories
- TEMP is deleted after a timeout (to keep things safe)
- One-time password for updating stories
- Fixed a faulty code in encryption
- Can detect incorrect passwords
- Functions: random(), temp(), protect()

v0.2.0: [Memento](https://github.com/Wafflespeanut/Python/tree/7f2572857bbe86b2598d27ab7872017a580351ff/Memento) *(has some bugs)*
- Added a simple encryption method which hexes and shifts the ASCII values (to make it really "private" - further protection is of your own)
- Added a function for viewing stories on a given day
- A TEMP file is created for viewing/updating any story, leaving the original files undisturbed
- Functions: hexed(), char(), zombify(), shift(), protect(), write()

v0.1.0: [Private Diary](https://github.com/Wafflespeanut/Python/tree/64a9c8dd2470ec309a439a41568778187bbe8bb7/Private%20Diary)
- Creates timestamped folders and text files for stories
- Writes the stories for every [RETURN] stroke, which indicates a paragraph
- Functions: new(), diary()
