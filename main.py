import numpy as np


# MACROS for the execution
LFSR_enable = 0
MISR_enable = 1


def LFSR(n_bit, taps, seed, n_tv, mode):
    """
    Function that generates test vectors using a Linear Feedback Shift Register (LFSR).
    :param n_bit: int, number of bits in the LFSR
    :param taps: list of int, TAPs configuration (1 for active, 0 for inactive)
    :param seed: list of int, the initial seed for the LFSR
    :param n_tv: int, number of test vectors to generate
    :param mode: string, can be either "1-to-m" or "m-to-1"
    :return: list of lists, list of test vectors
    """
    # list of results with seed as first tv
    results = [np.array(seed)]
    # generation of the T matrix
    T = np.empty((n_bit, n_bit))
    new_taps = [1] + taps
    for i in range(n_bit):
        # add taps to the last col
        T[i][n_bit-1] = new_taps[i]
        # add shift into the matrix
        if i != 0:
            T[i][i-1] = 1

    # check mode
    if mode == "m-to-1":
        # for m-to-1 use the transpose of T
        T = T.T

    # generation of n_tv test vectors
    for i in range(1, n_tv):
        # new empty tv
        new_tv = T @ results[i-1]
        # add new tv
        results.append(new_tv%2)
    # return results
    return results


def MISR(n_bit, taps, seed, responses):
    """
    Function that generates the signature using a Multi-Input Signature Register (MISR).
    :param n_bit: int, number of bits in the LFSR
    :param taps: list of int, TAPs configuration (1 for active, 0 for inactive)
    :param seed: list of int, the initial seed for the LFSR
    :param responses: list of lists, list containing the sequence of responses
    :return: list of lists, list of register status (the last one is the signature)
    """
    # list of results with seed as first tv
    results = [np.array(seed)]
    # generation of the T matrix
    T = np.empty((n_bit, n_bit))
    new_taps = [1] + taps
    for i in range(n_bit):
        # add taps to the last col
        T[i][n_bit-1] = new_taps[i]
        # add shift into the matrix
        if i != 0:
            T[i][i-1] = 1

    # generation of all the status (last is the signature)
    for i in range(1, len(responses)+1):
        # new empty tv
        new_tv = (T @ results[i-1]) + responses[i-1]
        # add new tv
        results.append(new_tv%2)
    # return results
    return results


def main():
    if LFSR_enable:
        ####################################################################################
        ####################################### LFSR #######################################
        ####################################################################################
        n_bit = 5 # number of bits
        taps = [1, 0, 1, 0]  # TAPs configuration
        seed = [1, 1, 0, 1, 0]  # initial seed
        n_tv = 5  # number of test vectors to generate

        # run LFSR
        result = LFSR(n_bit, taps, seed, n_tv, "1-to-m")

        # print results
        print("LFSR test vectors:")
        for i in range(n_tv):
            print(f"tv{i}: " + " ".join(map(str, result[i].astype(int).tolist())))

        ####################################################################################
        ####################################################################################

    if MISR_enable:
        ####################################################################################
        ####################################### MISR #######################################
        ####################################################################################
        n_bit = 5 # number of bits
        taps = [0, 0, 1, 1]  # TAPs configuration (h1:h4)
        seed = [0, 0, 0, 0, 0]  # initial seed (q0:q4)
        responses = [[0, 0, 0, 0, 1],
                     [1, 0, 0, 1, 1],
                     [1, 0, 0, 1, 1]] # sequence of responses (r0:r4)

        # run MISR
        result = MISR(n_bit, taps, seed, responses)

        # print MISR status and signature
        print("MISR status:")
        for i in range(len(responses)):
            print(f"state {i}:    " + " ".join(map(str, result[i].astype(int).tolist())))
            print(f"response {i+1}: " + " ".join(map(str, responses[i])))
            print("=> " + " ".join(map(str, result[i+1].astype(int).tolist())))
            print("-" * 20)

        print(f"Signature: " + " ".join(map(str, result[len(responses)].astype(int).tolist())))

        ####################################################################################
        ####################################################################################

main()