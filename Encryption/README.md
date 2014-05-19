Zombipher (yeah, it's quite a mess!)
======

This is my encryption cipher, built completely for learning purposes (fired by the elegance of encryption). Over the past few weeks, I've been learning new stuff in Python by finding different ways of getting into the cipher, and patching the algorithm so that it becomes stronger every time.

It's quite straight-forward. And, it's built by a lot of helper functions, for improving readability. The sieve() for generating primes is borrowed from rosettacode.org.

How it works?
======
- The pursuit began with dissolving the key into the phrase with the help of prime numbers. The sieve() of Eratosthenes looked elegant for my purpose.

- Firstly, the text and the key are turned to hexadecimal things using hexed()

- Then, they're sorted using the primes. The hexed key is inserted into the nth prime number index, while the remaining chars in the phrase are shifted. Sometimes, a few chars are neglected but, that's not a problem.

- Since the output array from combine() is mostly made of numbers, and it's independent of the key, add() was implemented to make a complication. It starts from the last character of the key (which is a number), it takes the numbers from the combined array, adds it to the ASCII value of the chosen char from the key, and finally overwrites the original value with the last digit of the answer. Here also, a few chars are neglected (Not to worry...)

- Now, the iteration part. "Security level" is just a fancy name given to this horror. As a fewchars (in the key) are left during the first combine() step, iterating the encrypted phrase again and again makes this secure (I'm sure that even two iterations is secure enough!). Longer iterations could lead to merciless outputs, which kills your processor.

- Once the iterations are complete, eit() puts the output into shift(). As we've got a 255 char-long ASCII table, the characters in the ciphertext are shifted by the ASCII value of each char in the key, so that we get a "zombified" ciphertext.

- The shift() function can sometimes peek into foreign characters (for instance, using entirely symbols for both text and key gives unnecessary non-ASCII output, which can't be interpreted by the program later, during decryption). To prevent that, the zombified text is hexed, which does fixes the problem.

- The reverse processes are carried out by char(), extract(), sub(), dit() functions for decryption.

- I've also added a few 'tries' to print custom messages for possible causes of the errors instead of the errors themselves.

The cipher caught me this way. If at least one iteration is allowed, the encrypted text has a lot of similar characters. A few dissimilarities here and there are what determine the output. As far as I can see, there are no bugs. But like I said, it isn't entirely invasion-free. There could be a hole somewhere. Whenever I come across one, I'll try to patch it ASAP...