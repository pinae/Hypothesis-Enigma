# Hypothesis-Enigma
Python implementation of a Enigma; tested with Hypothesis.

## Dependencies

Use Python in version 3.

We recommend creating a virtual environment:

```bash
python -m venv env
source env/bin/activate
```

Install the dependencies with `pip`:

```bash
pip install -r requirements.txt
```

## Running the tests

Run the tests using pytest:

```bash
python -m pytest
```

The output should look like this:

```text
======================== test session starts =========================
platform linux -- Python 3.6.9, pytest-5.3.5, py-1.8.1, pluggy-0.13.1
rootdir: /home/jme/Code/Hypothesis-Enigma
plugins: hypothesis-5.5.4
collected 6 items                                                                                  

tests/test_enigma.py ....                                      [ 66%]
tests/test_playgroud.py ..                                     [100%]

========================= 6 passed in 3.02s ==========================
```

## Using the `Enigma`

Initialize the `Enigma` with the following parameters 
(according to your code book):

 - `patch_key`: A permutation of the Alphabet of big 
   letters (`'ABCDEFGHIJKLMNOPQRSTUVWXYZ'`)
 - `rotor_selection`: There are 5 possible rotors at 
   position 1, 2 and 3 in the enigma. Supply a list 
   of rotor numbers linke `[0, 1, 2]`. It does not matter 
   if the list is longer because the `Enigma` uses only 
   the first three entries. So you may use a permutation
   of `[0, 1, 2, 3, 4]`.
 - `reflector_selection`: The number of the selected reflector
   rotor. There are three different options with the numbers 
   0, 1 or 2.
 - `r1_pos`: Rotation position of the first rotor. Values 
   between 0 and 26 make sense.
 - `r2_pos`: Rotation position of the second rotor. Values 
   between 0 and 26 make sense.
 - `r3_pos`: Rotation position of the third rotor. Values 
   between 0 and 26 make sense.
   
With the initialized object use `.encrypt()` and `.decrypt()` for 
Strings consisting of big letters only. Your string must match the
regex `r'^[A-Z]+$'`!
