#include <mpi.h>
#include <stdio.h>

int main(int argc, char* argv[]) {
    MPI_Init(&argc, &argv);

    int rank, size, number;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    if (rank == 0) {
        printf("Enter a number in process 0: ");
        scanf("%d", &number);
        MPI_Send(&number, 1, MPI_INT, rank + 1, 0, MPI_COMM_WORLD);
    } else {
        MPI_Recv(&number, 1, MPI_INT, rank - 1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        number += 1;
        if (rank < size - 1) {
            MPI_Send(&number, 1, MPI_INT, rank + 1, 0, MPI_COMM_WORLD);
        }
    }

    if (rank == size - 1) {
        printf("Process %d received final value: %d\n", rank, number);
    }

    MPI_Finalize();
    return 0;
}
