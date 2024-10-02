#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <pthread.h>

typedef struct args {
    pthread_mutex_t *mutex;
    int counter, lower_bound, higher_bound;
} args_t;

static double max_probable_distance(int *buffer, int buffer_len, int n, int decaler) {
    double distance, tmp, tmp2;
    int i, j, ip, jp, d;

    for(i = 0; i < buffer_len; i++) buffer[i] = 0;

    for(i = 0; i < n; i++) {
        for (j = 0; j < n; j++) {
            for (ip = 0; ip < n; ip++) {
                for (jp = 0; jp < n; jp++) {
                    tmp = (double) (i - ip);
                    tmp2 = (double) (j - jp);
                    distance = sqrt((tmp * tmp + tmp2 * tmp2));

                    d = (int) (distance * decaler);
                    buffer[d % buffer_len]++;
                }
            }
        }
    }

    int max_value = -1, max_distance = -1;

    for(i = 0; i < buffer_len; i++) {
        if (buffer[i] > max_value) {
            max_value = buffer[i];
            max_distance = i;
        }
    }

    return ((double) max_distance) / ((double) decaler);
}

static void *job(void *a) {
    static int _id = 0;
    int id = _id++;

    printf("Launch thread %d\n", id);

    args_t *args = (args_t*) a;
    int n;

    #define N_DECIMAL 3

    int decalage = 1;

    int i;

    for(i = 0; i < N_DECIMAL; i++) decalage *= 10;

    int buffer_len = args->higher_bound * decalage + 1;

    int buffer[buffer_len];

    double value;

    while (1) {
        if (pthread_mutex_lock(args->mutex) == -1) {
            printf("Failed to lock mutex\n");
            exit(EXIT_FAILURE);
        }

        n = args->counter;
        args->counter++;

        if (pthread_mutex_unlock(args->mutex) == -1) {
            printf("Failed to unlock mutex\n");
            exit(EXIT_FAILURE);
        }

        if (n > args->higher_bound) break;
        else {
            value = max_probable_distance(buffer, buffer_len, n, decalage);
            printf("For n = %d it gives => %f\n", n, value / ((double) n));
        }
    }

    printf("Shutdown thread %d\n", id);

    return NULL;
}

int main(int argc, char **argv) {
    int n_threads = atoi(argv[1]);
    int lower_bound = atoi(argv[2]);
    int higher_bound = atoi(argv[3]);

    pthread_mutex_t mutex;

    if (pthread_mutex_init(&mutex, 0) == -1) {
        printf("Failed to init mutex\n");
        return EXIT_FAILURE;
    }

    pthread_t threads[n_threads];

    args_t args;
    args.mutex = &mutex;
    args.counter = lower_bound;
    args.lower_bound = lower_bound;
    args.higher_bound = higher_bound;

    for (int i = 0; i < n_threads; i++) {
        if (pthread_create(&threads[i], NULL, job, (void*) &args) == -1) {
            printf("Failed to start thread %d\n", i);
            return EXIT_FAILURE;
        }
    }

    for (int i = 0; i < n_threads; i++) {
        if (pthread_join(threads[i], NULL) == -1) {
            printf("Failed to join thread %d\n", i);
        }
    }

    if (pthread_mutex_destroy(&mutex) == -1) {
        printf("Failed to destroy mutex\n");
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}