Zombipher (yeah, it's quite a mess!)
======

This is my encryption cipher, built completely for learning purposes (fired by the elegance of encryption). Over the past few weeks, I've been learning new stuff in Python by finding different ways of getting into the cipher, and patching the algorithm so that it becomes stronger every time.

It's quite straight-forward. And, it's built by a lot of my own helper functions. Only the "Sieve of Eratosthenes" for generating primes is borrowed from rosettacode.org.

CURRENT BUG: Problems with Unicode symbols! Unable to encrypt/decrypt when several punctuation sequences are present. Possibly due to the recently implemented shift().

How it works?
======
- The pursuit began with dissolving the key into the phrase with the help of prime numbers. The sieve() looked elegant for my purpose.

- Firstly, the text and the key are turned to hexadecimal things using hexed()

- Then, they're sorted using the primes. The hexed key is inserted into the nth prime number index, while the remaining chars in the phrase are shifted. If the key exceeds the length of the phrase, a few chars from the key are neglected (which is overcome by the next function)

- Since the output array from combine() is mostly made of numbers, and it's independent of the key, add() was implemented to make a complication. It does this. Starting from the last character of the key (which is a number), it takes the numbers from the combined array, adds it to the ASCII value of the chosen char from the key, and finally overwrites the original value with the last digit of the answer. A few chars are neglected here (which could also be overcome)

- Now, the iteration part. "Security level" is just a fancy name given to this horror. As a few key chars are left during the first combine() step, iterating the encrypted phrase again and again makes this secure (I'm sure that even two iterations is secure enough!). More than 10 iterations could lead to a long output, which consumes too much time.

- Once the iterations are complete, eit() puts the output into shift(). As we've got a 255 char-long ASCII table, the characters in the ciphertext are shifted by the ASCII value of each char in the key, so that we get a "zombified" ciphertext.

- The reverse processes are carried out by char(), extract(), sub(), dit() functions for decryption.

- I've also added a few 'tries' to print custom messages for possible causes of the errors instead of the errors themselves.

The cipher caught me this way. If at least one iteration is allowed, the encrypted text has a lot of similar characters. A few dissimilarities here and there is what determines the output. As far as I can see, there's no resemblance of the real text, nor the key. Like I said, it isn't entirely bug-free. But, whenever I come across one, I'll patch it ASAP...