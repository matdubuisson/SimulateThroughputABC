#!/bin/python3
# Mattéo Dubuisson 11772100

import matplotlib.pyplot as plt

BUFFER_SIZE = 300

def compute(bufferA:float, bufferB:float, bufferC:float, allocA:float, allocB:float, allocC:float, rate_inA:float, rate_inB:float, rate_inC:float) -> tuple:
    def compute(bufferX:float, allocX:float, rate_inX:float):
        losseX = 0

        if rate_inX >= allocX:
            bufferX += rate_inX - allocX
            rate_inX = allocX

            if bufferX > BUFFER_SIZE:
                losseX = bufferX = BUFFER_SIZE
                bufferX = BUFFER_SIZE
        elif bufferX > 0 and rate_inX < allocX:
            diff = allocX - rate_inX
            
            if diff <= bufferX:
                bufferX -= diff
                rate_inX = allocX
            else:
                rate_inX += bufferX
                bufferX = 0

        return bufferX, allocX, rate_inX, losseX

    bufferA, allocA, rate_inA, losseA = compute(bufferA, allocA, rate_inA)
    bufferB, allocB, rate_inB, losseB = compute(bufferB, allocB, rate_inB)
    bufferC, allocC, rate_inC, losseC = compute(bufferC, allocC, rate_inC)

    A = max(allocA, rate_inA)
    B = max(allocB, rate_inB)
    C = max(allocC, rate_inC)

    d = A + B + C
    
    rate_outA = rate_inA / d * 100
    rate_outB = rate_inB / d * 100
    rate_outC = rate_inC / d * 100

    # Actually here the rates in are the 'real rate in' according to allocation throughput and buffer occupancy
    return bufferA, allocA, rate_inA, losseA, rate_outA, bufferB, allocB, rate_inB, losseB, rate_outB, bufferC, allocC, rate_inC, losseC, rate_outC

bufferA = bufferB = bufferC = 0
rate_inA = allocA = 25
rate_inB = allocB = 50
allocC = 25

bufferA_lst = []
bufferB_lst = []
bufferC_lst = []

allocA_lst = []
allocB_lst = []
allocC_lst = []

rate_inA_lst = []
rate_inB_lst = []
rate_inC_lst = []

losseA_lst = []
losseB_lst = []
losseC_lst = []

rate_outA_lst = []
rate_outB_lst = []
rate_outC_lst = []

size_bufferA_lst = []
size_bufferB_lst = []
size_bufferC_lst = []

domain = list(range(0, allocC + 1, 1))
domain.extend([allocC + 10] * 40)
for rate_inC in domain:
    bufferA, allocA, _, losseA, rate_outA, bufferB, allocB, _, losseB, rate_outB, bufferC, allocC, _, losseC, rate_outC = compute(bufferA, bufferB, bufferC, allocA, allocB, allocC, rate_inA, rate_inB, rate_inC)
    
    bufferA_lst.append(bufferA)
    bufferB_lst.append(bufferB)
    bufferC_lst.append(bufferC)

    allocA_lst.append(allocA)
    allocB_lst.append(allocB)
    allocC_lst.append(allocC)
    
    rate_inA_lst.append(rate_inA)
    rate_inB_lst.append(rate_inB)
    rate_inC_lst.append(rate_inC)

    losseA_lst.append(losseA)
    losseB_lst.append(losseB)
    losseC_lst.append(losseC)

    rate_outA_lst.append(rate_outA)
    rate_outB_lst.append(rate_outB)
    rate_outC_lst.append(rate_outC)

    size_bufferA_lst.append(BUFFER_SIZE)
    size_bufferB_lst.append(BUFFER_SIZE)
    size_bufferC_lst.append(BUFFER_SIZE)

xs = list(range(0, len(rate_inA_lst), 1))

fig, axes = plt.subplots(2, 3)

axes[0][0].plot(xs, allocA_lst, "--b")
axes[0][0].plot(xs, rate_inA_lst, "-g")
axes[0][0].plot(xs, rate_outA_lst, "-y")
axes[0][0].legend(("max rate_out", "rate_in", "rate_out"))
axes[0][0].set_xlabel("Time unit [arbitrary]")
axes[0][0].set_ylabel("Rate according to max rate (max 100%)")

axes[1][0].plot(xs, size_bufferA_lst, "--b")
axes[1][0].plot(xs, bufferA_lst, "-g")
axes[1][0].plot(xs, losseA_lst, "-r")
axes[1][0].legend(("buffer size limit", "buffer size", "buffer losse"))
axes[1][0].set_xlabel("Time unit [arbitrary]")
axes[1][0].set_ylabel("Buffer size according to max rate (max {0}%)".format(BUFFER_SIZE))

axes[0][1].plot(xs, allocB_lst, "--b")
axes[0][1].plot(xs, rate_inB_lst, "-g")
axes[0][1].plot(xs, rate_outB_lst, "-y")
axes[0][1].legend(("max rate_out", "rate_in", "rate_out"))
axes[0][1].set_xlabel("Time unit [arbitrary]")
axes[0][1].set_ylabel("Rate according to max rate (max 100%)")

axes[1][1].plot(xs, size_bufferB_lst, "--b")
axes[1][1].plot(xs, bufferB_lst, "-g")
axes[1][1].plot(xs, losseB_lst, "-r")
axes[1][1].legend(("buffer size limit", "buffer size", "buffer losse"))
axes[1][1].set_xlabel("Time unit [arbitrary]")
axes[1][1].set_ylabel("Buffer size according to max rate (max {0}%)".format(BUFFER_SIZE))

axes[0][2].plot(xs, allocC_lst, "--b")
axes[0][2].plot(xs, rate_inC_lst, "-g")
axes[0][2].plot(xs, rate_outC_lst, "-y")
axes[0][2].legend(("max rate_out", "rate_in", "rate_out"))
axes[0][2].set_xlabel("Time unit [arbitrary]")
axes[0][2].set_ylabel("Rate according to max rate (max 100%)")

axes[1][2].plot(xs, size_bufferC_lst, "--b")
axes[1][2].plot(xs, bufferC_lst, "-g")
axes[1][2].plot(xs, losseC_lst, "-r")
axes[1][2].legend(("buffer size limit", "buffer size", "buffer losse"))
axes[1][2].set_xlabel("Time unit [arbitrary]")
axes[1][2].set_ylabel("Buffer size according to max rate (max {0}%)".format(BUFFER_SIZE))

plt.show()