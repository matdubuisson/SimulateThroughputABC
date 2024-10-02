#!/bin/python3
# Mattéo Dubuisson 11772100

import sys
import matplotlib.pyplot as plt

print(sys.argv)

def wrobin(queues_properties: list):
    n_queues = len(queues_properties)
    n_times = len(queues_properties[0][2])
    buffers = [0.0] * n_queues

    def compute(rate_in: float, index: int, supp_alloc: float = 0.0):
        rate_out = None
        alloc = queues_properties[index][0] + supp_alloc
        buffer_alloc = queues_properties[index][1]

        losse = 0.0

        if rate_in >= alloc:
            buffers[index] += rate_in - alloc
            rate_out = alloc

            if buffers[index] > buffer_alloc: # Throughput to high so try to store in the buffer
                # Can have losses when the buffer is full
                losse = buffers[index] - buffer_alloc
                buffers[index] = buffer_alloc
        elif buffers[index] > 0:
            diff = alloc - rate_in # As rate_in < alloc, there is left throughput to empty a little the buffer

            if diff <= buffers[index]: # Can empty only a part of the buffer
                buffers[index] -= diff
                rate_out = alloc
            else: # Can empty the full buffer
                rate_out = rate_in + buffers[index]
                buffers[index] = 0.0
        else:
            rate_out = rate_in

        return buffers[index], losse, rate_out

    rate_outss = []
    lossess = []
    buffers_valuess = []

    for q in range(n_queues):
        rate_outss.append([0.0] * n_times)
        lossess.append([0.0] * n_times)
        buffers_valuess.append([0.0] * n_times)

    for time in range(n_times):
        available_throughput = 0.0
        askers = []
        askers_alloc = 0.0

        for q in range(n_queues):
            alloc = queues_properties[q][0]
            rate_in = queues_properties[q][2][time]
            buffer, losse, rate_out = compute(rate_in, q)

            if rate_out < alloc:
                available_throughput += alloc - rate_out
                rate_outss[q][time] = rate_out
                lossess[q][time] = losse
                buffers_valuess[q][time] = buffer
            elif buffer > 0:
                askers.append(q)
                askers_alloc += alloc

        for q in askers:
            alloc = queues_properties[q][0]
            supp_alloc = alloc / askers_alloc * available_throughput
            buffer, losse, rate_out = compute(rate_in, q, supp_alloc)

            rate_outss[q][time] = rate_out
            lossess[q][time] = losse
            buffers_valuess[q][time] = buffer

    xs = list(range(n_times))
    fig, axes = plt.subplots(2, n_queues)

    for index in range(n_queues):
        alloc = queues_properties[index][0]
        allocs = [alloc] * n_times
        rate_ins = queues_properties[index][2]
        rate_outs = rate_outss[index]

        axes[0][index].plot(xs, allocs, "--b")
        axes[0][index].plot(xs, rate_ins, "-g")
        axes[0][index].plot(xs, rate_outs, "-y")
        axes[0][index].legend(("max rate_out", "rate_in", "rate_out"))
        axes[0][index].set_xlabel("Time unit [arbitrary]")
        axes[0][index].set_ylabel("Rate according to max rate (max 100%)")

        alloc_buffer = queues_properties[index][1]
        allocs_buffer = [alloc_buffer] * n_times
        losses = lossess[index]
        buffers_values = buffers_valuess[index]

        axes[1][index].plot(xs, allocs_buffer, "--b")
        axes[1][index].plot(xs, buffers_values, "-g")
        axes[1][index].plot(xs, losses, "-r")
        axes[1][index].legend(("buffer size limit", "buffer size", "buffer losse"))
        axes[1][index].set_xlabel("Time unit [arbitrary]")
        axes[1][index].set_ylabel("Buffer size according to max rate (max {0}%)".format(alloc_buffer))

    plt.show()

def launch(scheduler: str, queues_properties: list):
    if scheduler == "wrobin":
        wrobin(queues_properties)
    else:
        raise NotImplementedError("Scheduler {0} not implemented".format(scheduler))

if __name__ == "__main__":
    k = 1
    N = int(k / 0.01 + 1)
    M = 30

    S = M + N

    tmp = [k] * S
    s = 0

    for i in range(S):
        if s < k:
            tmp[i] = s
            s += 0.01

    launch("wrobin", [
        (0.25, 1, [0.25] * S),
        (0.5, 1, [0.5] * S),
        (0.25, 1, tmp),
    ])