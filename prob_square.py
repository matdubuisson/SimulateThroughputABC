def max_proba_distance(N, decimal=3):
    m = {}

    for i in range(N):
        for j in range(N):
            for ip in range(N):
                for jp in range(N):
                    distance = round(( (i - ip)**2 + (j-jp) **2 ) ** (1/2), decimal)

                    if m.get(distance, None) == None:
                        m[distance] = 1
                    else:
                        m[distance] += 1

    max_value = None
    max_distance = None

    for distance in m.keys():
        value = m[distance]

        if max_distance == None or max_value < value:
            max_distance = distance
            max_value = value

    # Normalization
    return round(max_distance / N, 5), max_value

for n in range(4, 2**6, 2):
    print(max_proba_distance(n))