# -*- coding: utf-8 -*-
import unittest
from hypothesis import given
from hypothesis.strategies import SearchStrategy, integers, from_regex, permutations, lists, one_of
from enigma import Enigma


def radiogram() -> SearchStrategy:
    normal_word = from_regex(r'[A-Z]{1,15}', fullmatch=True)
    name = normal_word.map(lambda w: "X" + w + "X" + w + "X")
    sentence = lists(elements=one_of(normal_word, name), min_size=1, max_size=12).map(lambda x: "".join(x) + "X")
    return lists(sentence, min_size=1, max_size=5).map(lambda s: "".join(s))


class EnigmaTestCase(unittest.TestCase):
    def check_enigma(self, plaintext: str, r1p: int = 0, r2p: int = 0, r3p: int = 0):
        enigma = Enigma(r1_pos=r1p, r2_pos=r2p, r3_pos=r3p)
        cipher_text = enigma.encrypt(plaintext)
        self.assertNotEqual(plaintext, cipher_text)
        self.assertEqual(plaintext, enigma.decrypt(cipher_text))

    def test_hello_world(self):
        self.check_enigma("HELLOWORLD")

    def test_real_example(self):
        plaintext = "DASOBERKOMMANDODERWEHRMAQTGIBTBEKANNTXAACHENXAACHENXISTGERETTETX" + \
                    "DURQGEBUENDELTENEINSATZDERHILFSKRAEFTEKONNTEDIEBEDROHUNGABGEWENDET" + \
                    "UNDDIERETTUNGDERSTADTGEGENXEINSXAQTXNULLXNULLXUHRSIQERGESTELLTWERDENX"
        patch_key = 'DBNATLIHGVZFMCOUYRSEPJXWQK'
        r1p = 16
        r2p = 26
        r3p = 8
        enigma = Enigma(patch_key=patch_key, rotor_selection=[0, 3, 2], reflector_selection=1,
                        r1_pos=r1p, r2_pos=r2p, r3_pos=r3p)
        cipher_text = enigma.encrypt(plaintext)
        self.assertEqual('YTCBORYNCVSQAWDTMVVDMVVCLWSPNPVKLLWUIAVUVDAYUIWUTCZWMTDWUGBQZCJ' +
                         'ZBFJNBYQZVZPPTXDQJQQFMBXXFXPYEROURJPFNCUYDZOZMVGPEYJYKPHDLGKNOB' +
                         'TJGMMMEMVLOIWWOBTZNERYOJOWCDZLVEVVPYPHNSYNCQXKIAGOWVSEWPXPCMXPW' +
                         'APVYFHLYCK', cipher_text)
        self.assertEqual(plaintext, enigma.decrypt(cipher_text))

    @given(integers(min_value=0, max_value=26),
           integers(min_value=0, max_value=26),
           integers(min_value=0, max_value=26),
           from_regex(r'[A-Z]', fullmatch=True))
    def test_same_characters_different_sequence(self, r1p: int, r2p: int, r3p: int, repeated_char: str):
        enigma = Enigma(r1_pos=r1p, r2_pos=r2p, r3_pos=r3p)
        cipher_text = enigma.encrypt(repeated_char[0]*26)
        for test_char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            self.assertNotEqual(cipher_text, test_char*26)
        self.assertEqual(repeated_char[0]*26, enigma.decrypt(cipher_text))

    @given(integers(min_value=0, max_value=26),
           integers(min_value=0, max_value=26),
           integers(min_value=0, max_value=26),
           permutations(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')),
           permutations(list(range(5))),
           integers(min_value=0, max_value=2),
           radiogram())
    def test_encrypt_decrypt(self, r1p: int, r2p: int, r3p: int, patch_key: str,
                             rotor_selection: list, reflector_selection: int, plaintext: str):
        enigma = Enigma(r1_pos=r1p, r2_pos=r2p, r3_pos=r3p, patch_key=patch_key,
                        rotor_selection=rotor_selection, reflector_selection=reflector_selection)
        cipher_text = enigma.encrypt(plaintext)
        self.assertNotEqual(cipher_text, plaintext)
        self.assertEqual(plaintext, enigma.decrypt(cipher_text))


if __name__ == '__main__':  # pragma: no mutate
    print("100 Beispiele für Funksprüche:")  # pragma: no cover
    for _ in range(100):  # pragma: no cover
        print(" -", radiogram().example())  # pragma: no cover
    unittest.main()  # pragma: no cover
