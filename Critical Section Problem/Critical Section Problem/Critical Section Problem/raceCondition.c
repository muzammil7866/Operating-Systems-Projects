#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

#define NUM_THREADS 5
#define INCREMENTS 1000000

int counter = 0;

void* increment_counter(void* arg) {
    for (int i = 0; i < INCREMENTS; i++) {
        // Critical Section starts
        counter++; // No synchronization!
        // Critical Section ends
    }
    return NULL;
}

int main() {
    pthread_t threads[NUM_THREADS];

    printf("Starting %d threads, each incrementing counter %d times...\n", NUM_THREADS, INCREMENTS);
    printf("Expected final counter value: %d\n", NUM_THREADS * INCREMENTS);

    for (int i = 0; i < NUM_THREADS; i++) {
        if (pthread_create(&threads[i], NULL, increment_counter, NULL) != 0) {
            perror("Failed to create thread");
            return 1;
        }
    }

    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }

    printf("Final counter value: %d\n", counter);

    if (counter != NUM_THREADS * INCREMENTS) {
        printf("RACE CONDITION DETECTED! The final value is incorrect.\n");
    }
    else {
        printf("No race condition detected this time. Try increasing INCREMENTS.\n");
    }

    return 0;
}
