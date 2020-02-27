# -*- coding: utf-8 -*-
class Enigma:
    def __init__(self, patch_key: str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
                 rotor_selection: list = [0, 1, 2], reflector_selection: int = 0,
                 r1_pos: int = 0, r2_pos: int = 0, r3_pos: int = 0):
        self.position = 0
        self.pk = patch_key
        self.al = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        rotors = ['EKMFLGDQVZNTOWYHXUSPAIBRCJ',
                  'AJDKSIRUXBLHWTMCQGZNPYFVOE',
                  'BDFHJLCPRTXVZNYEIWGAKMUSQO',
                  'ESOVPZJAYQUIRHXLNFTGKDCMWB',
                  'VZBRGITYUPSDNHLXAWMJQOFECK']
        reflectors = ['EJMZALYXVBWFCRQUONTSPIKHGD',
                      'YRUHQSLDPXNGOKMIEBFZCWVJAT',
                      'FVPJIAOYEDRZXWGCTKUQSBNMHL']
        self.r1 = rotors[rotor_selection[0]]
        self.r2 = rotors[rotor_selection[1]]
        self.r3 = rotors[rotor_selection[2]]
        self.re = reflectors[reflector_selection]
        self.r1p = r1_pos
        self.r2p = r2_pos
        self.r3p = r3_pos
        self.c_offset = int('A'.encode('ascii')[0])

    def reset(self, new_pos: int = 0):
        self.position = new_pos

    def encrypt_char(self, c: str) -> str:
        step0 = self.pk[int(c.encode('ascii')[0]) - self.c_offset]
        step1 = self.r1[(int(step0.encode('ascii')[0]) - self.c_offset +
                         (self.position // len(self.al)**2) + self.r1p) % len(self.al)]
        step2 = self.r2[(int(step1.encode('ascii')[0]) - self.c_offset +
                         (self.position // len(self.al)) + self.r2p) % len(self.al)]
        step3 = self.r3[(int(step2.encode('ascii')[0]) - self.c_offset +
                         self.position + self.r3p) % len(self.al)]
        step4 = self.re[int(step3.encode('ascii')[0]) - self.c_offset]
        step5 = self.r3[(int(step4.encode('ascii')[0]) - self.c_offset +
                         self.position + self.r3p) % len(self.al)]
        step6 = self.r2[(int(step5.encode('ascii')[0]) - self.c_offset +
                         (self.position // len(self.al)) + self.r2p) % len(self.al)]
        step7 = self.r1[(int(step6.encode('ascii')[0]) - self.c_offset +
                         (self.position // len(self.al)**2) + self.r1p) % len(self.al)]
        step8 = self.pk[int(step7.encode('ascii')[0]) - self.c_offset]
        self.position += 1
        return step8

    def decrypt_char(self, c: str) -> str:
        step0 = self.al[self.pk.index(c[0]) % len(self.al)]
        step1 = self.al[(self.r1.index(step0[0]) - (self.position // len(self.al)**2) - self.r1p) % len(self.al)]
        step2 = self.al[(self.r2.index(step1[0]) - (self.position // len(self.al)) - self.r2p) % len(self.al)]
        step3 = self.al[(self.r3.index(step2[0]) - self.position - self.r3p) % len(self.al)]
        step4 = self.al[self.re.index(step3[0]) % len(self.al)]
        step5 = self.al[(self.r3.index(step4[0]) - self.position - self.r3p) % len(self.al)]
        step6 = self.al[(self.r2.index(step5[0]) - (self.position // len(self.al)) - self.r2p) % len(self.al)]
        step7 = self.al[(self.r1.index(step6[0]) - (self.position // len(self.al)**2) - self.r1p) % len(self.al)]
        step8 = self.al[self.pk.index(step7[0]) % len(self.al)]
        self.position += 1
        return step8

    def encrypt(self, plain_text: str, start_pos: int = 0) -> str:
        self.reset(start_pos)
        return "".join([self.encrypt_char(c) for c in plain_text])

    def decrypt(self, cipher_text: str, start_pos: int = 0) -> str:
        self.reset(start_pos)
        return "".join([self.decrypt_char(c) for c in cipher_text])
