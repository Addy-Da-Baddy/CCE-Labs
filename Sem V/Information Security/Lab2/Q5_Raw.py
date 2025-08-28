# AES-192 step-by-step (educational)
# - input key interpreted as hex; expanded to 24 bytes by appending first 8 bytes
# - prints key schedule and intermediate states

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# ---------- constants ----------
SBOX = [
0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76,
0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0,
0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15,
0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75,
0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84,
0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf,
0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8,
0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2,
0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73,
0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb,
0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79,
0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08,
0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a,
0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e,
0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf,
0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16
]

RCON = [0x00,0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1B,0x36,0x6C,0xD8,0xAB]

# ---------- helpers ----------
def bytes2matrix(b):
    # column-major: state[row][col] = b[4*col + row]
    return [[b[row + 4*col] for col in range(4)] for row in range(4)]

def matrix2bytes(m):
    return bytes([m[row][col] for col in range(4) for row in range(4)])

def sub_bytes(state):
    for r in range(4):
        for c in range(4):
            state[r][c] = SBOX[state[r][c]]

def shift_rows(state):
    for r in range(4):
        state[r] = state[r][r:] + state[r][:r]

def xtime(a):
    return ((a << 1) ^ 0x1b) & 0xff if (a & 0x80) else (a << 1) & 0xff

def gmul(a,b):
    # finite field multiplication
    res = 0
    while b:
        if b & 1:
            res ^= a
        a = xtime(a)
        b >>= 1
    return res & 0xff

def mix_single_column(col):
    a0,a1,a2,a3 = col
    return [
        (gmul(2,a0) ^ gmul(3,a1) ^ a2 ^ a3) & 0xff,
        (a0 ^ gmul(2,a1) ^ gmul(3,a2) ^ a3) & 0xff,
        (a0 ^ a1 ^ gmul(2,a2) ^ gmul(3,a3)) & 0xff,
        (gmul(3,a0) ^ a1 ^ a2 ^ gmul(2,a3)) & 0xff
    ]

def mix_columns(state):
    for c in range(4):
        col = [state[r][c] for r in range(4)]
        newc = mix_single_column(col)
        for r in range(4):
            state[r][c] = newc[r]

def add_round_key(state, round_key_matrix):
    for r in range(4):
        for c in range(4):
            state[r][c] ^= round_key_matrix[r][c]

def rot_word(w): return w[1:]+w[:1]
def sub_word(w): return [SBOX[b] for b in w]

# ---------- key expansion for AES-192 ----------
def key_expansion_192(key24):
    Nk = 6
    Nb = 4
    Nr = 12
    # words as lists of 4 ints
    words = [list(key24[4*i:4*i+4]) for i in range(Nk)]
    i = Nk
    while len(words) < Nb * (Nr + 1):
        temp = words[-1].copy()
        if i % Nk == 0:
            temp = sub_word(rot_word(temp))
            temp[0] ^= RCON[i//Nk]
        # note: for Nk>6 there is an extra condition i%Nk==4 but Nk==6 here
        word = [ (words[i-Nk][j] ^ temp[j]) & 0xff for j in range(4) ]
        words.append(word)
        i += 1
    # build round keys (each 16 bytes -> matrix)
    round_keys = []
    for r in range(Nr+1):
        rkbytes = b''.join(bytes(w) for w in words[4*r:4*(r+1)])
        round_keys.append(bytes2matrix(rkbytes))
    return round_keys

# ---------- main ----------

# input and key handling
plaintext = "Top Secret Data"
key_hex = "FEDCBA9876543210FEDCBA9876543210"  # provided by user (16 bytes hex)
key_raw = bytes.fromhex(key_hex)             # 16 bytes
# expand to 24 bytes deterministically (append first 8 bytes)
key192 = key_raw + key_raw[:8]               # 24 bytes used for AES-192

print("Using AES-192 key (hex):", key192.hex())
print("Plaintext (raw):", plaintext)
padded = pad(plaintext.encode('utf-8'), 16)
print("Padded plaintext (hex):", padded.hex())
block = padded[:16]  # single-block example

# derive round keys and print them
round_keys = key_expansion_192(key192)
print("\nRound keys (Nr=12) [hex]:")
for r,kmat in enumerate(round_keys):
    print(f"Round {r:02d} key:", matrix2bytes(kmat).hex())

# initial state
state = bytes2matrix(block)
print("\nInitial State (hex):", matrix2bytes(state).hex())

# initial AddRoundKey
add_round_key(state, round_keys[0])
print("After AddRoundKey (round 0):", matrix2bytes(state).hex())

# main rounds 1..11
for rnd in range(1, 12):
    print(f"\n--- Round {rnd} ---")
    # SubBytes
    sub_bytes(state)
    print("After SubBytes:        ", matrix2bytes(state).hex())
    # ShiftRows
    shift_rows(state)
    print("After ShiftRows:       ", matrix2bytes(state).hex())
    # MixColumns (skip for final round which is rnd==12 but here rnd in 1..11)
    if rnd != 12:
        mix_columns(state)
        print("After MixColumns:      ", matrix2bytes(state).hex())
    # AddRoundKey
    add_round_key(state, round_keys[rnd])
    print("After AddRoundKey:     ", matrix2bytes(state).hex())

# final round (Nr=12) -> note loop above covers rounds 1..11 (mix columns included)
# we now perform final round steps (SubBytes, ShiftRows, AddRoundKey with round_keys[12])
# But because above loop ran up to rnd=11 inclusive including mixcolumns, we now run final round:
print("\n--- Final Round 12 ---")
sub_bytes(state)
print("After SubBytes:        ", matrix2bytes(state).hex())
shift_rows(state)
print("After ShiftRows:       ", matrix2bytes(state).hex())
add_round_key(state, round_keys[12])
cipher_block = matrix2bytes(state)
print("After AddRoundKey (12):", cipher_block.hex())

# verify with PyCryptodome AES-192 (ECB) decryption to recover plaintext
cipher_lib = AES.new(key192, AES.MODE_ECB)
# ciphertext produced by our routine
ciphertext = cipher_block
# decrypt and unpad via library
decrypted_padded = cipher_lib.decrypt(ciphertext)
recovered = unpad(decrypted_padded, 16).decode('utf-8')
print("\nCiphertext (hex):", ciphertext.hex())
print("Recovered plaintext (via PyCryptodome decrypt):", recovered)
