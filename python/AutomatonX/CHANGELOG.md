### Changelog

v0.3.0: AutomatonX
- Dumped useless functions
- Made use of inbuilt XOR (reducing computing time)
- Key insertion is deprecated (major flaw exterminated!)
- Usage of some timers have been dropped
- `FILE()` can be used to encrypt/decrypt files and `RUN()` can be used to play with it directly
- Functions: `CXOR(), combine(), extract(), zombify(), RUN(), FILE()`

v0.2.1: [Automaton](https://github.com/Wafflespeanut/scripts/blob/9a583d54bd9f6dab2255e873f7c7bbc4fc943108/Encryption/Sentinel)
- Added timer for each phase
- Phrase and key is XORed (resulting in unknown characters)
- Hexing during epilog is deprecated
- Functions: `binkill(), CXOR()`

v0.2.0: [Sentinel](https://github.com/Wafflespeanut/scripts/blob/581574ddd9c59cf0f45b933548aa2f2dc64203ae/Encryption/Sentinel) *(Till now, some garbage functions were used)*
- Changed the basis of random keys
- Corrected some functions with improved algorithm
- Alpha-numeric random keys
- Simplified version [available in Javascript](https://wafflespeanut.github.io/Sentinel)
- Functions: `keypnum(), pop(), extract()`

v0.1.4: [Ranger](https://github.com/Wafflespeanut/scripts/blob/49bfe59bb4baa753678e6fbb4b29ad665459963c/Encryption/Ranger)
- Replaced all possible errors with custom messages
- Variable ciphertext outputs
- An iteration is carried out using a random key
- Functions: `keypnum(), pop(), find(), slicing()`

v0.1.3: [Zombipher](https://github.com/Wafflespeanut/scripts/blob/3200ac598593c4abc7e9b3e899ad6889333c83ba/Encryption)
- Added "try-except" to print custom messages instead of disgusting errors
- Enhanced user interface
- Loops added to neglect wrong inputs
- Hexed outputs to eliminate a bug!
- Functions: `zombify()`

v0.1.2: [Zombifier](https://github.com/Wafflespeanut/scripts/blob/cef60840ba2273ca2a0c3fb6943f927fcc7af01f/Encryption)
- Ciphertext is shifted based on key
- Added user interface
- Functions: `shift(), zombify()`

v0.1.1: [Keydepher](https://github.com/Wafflespeanut/scripts/blob/d45d3dd783389c11de5e66cbcacbee0724e643f0/Encryption)
- Key is dissolved into the phrase (key-dependent cipher)
- Iterated ciphertext outputs
- Functions: `add(), sub(), eit(), dit()`

v0.1.0: [Sorter](https://github.com/Wafflespeanut/scripts/blob/00ea11b8068e874fb86c84bc1d466b25053194b9/Encryption) *(It doesn't encrypt anything!)*
- Just hexing and shuffling (key-independent)
- Iterated shuffled outputs
- Functions: `sieve(), hexed(), combine(), char(), extract()`
