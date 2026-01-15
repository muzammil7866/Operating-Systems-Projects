//#include <stdio.h>
//#include <stdlib.h>
//#include <pthread.h>
//
//#define NUM_THREADS 5
//#define INCREMENTS 1000000
//
//int counter = 0;
//pthread_mutex_t lock;
//
//void* increment_counter(void* arg) {
//    for (int i = 0; i < INCREMENTS; i++) {
//        // Critical Section starts
//        pthread_mutex_lock(&lock);
//        counter++;
//        pthread_mutex_unlock(&lock);
//        // Critical Section ends
//    }
//    return NULL;
//}
//
//int main() {
//    pthread_t threads[NUM_THREADS];
//
//    // Initialize the mutex
//    if (pthread_mutex_init(&lock, NULL) != 0) {
//        printf("\n mutex init failed\n");
//        return 1;
//    }
//
//    printf("Starting %d threads with MUTEX PROTECTION, each incrementing counter %d times...\n", NUM_THREADS, INCREMENTS);
//    printf("Expected final counter value: %d\n", NUM_THREADS * INCREMENTS);
//
//    for (int i = 0; i < NUM_THREADS; i++) {
//        if (pthread_create(&threads[i], NULL, increment_counter, NULL) != 0) {
//            perror("Failed to create thread");
//            return 1;
//        }
//    }
//
//    for (int i = 0; i < NUM_THREADS; i++) {
//        pthread_join(threads[i], NULL);
//    }
//
//    printf("Final counter value: %d\n", counter);
//
//    if (counter == NUM_THREADS * INCREMENTS) {
//        printf("SUCCESS: The critical section was protected correctly.\n");
//    }
//    else {
//        printf("FAILURE: Race condition still occurs!\n");
//    }
//
//    pthread_mutex_destroy(&lock);
//
//    return 0;
//}
