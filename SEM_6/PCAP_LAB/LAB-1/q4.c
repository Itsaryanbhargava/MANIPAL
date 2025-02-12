#include <mpi.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);

    int rank;
    char str[] = "HELLO";
    int len = strlen(str);

    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    if (rank < len) {
        if (isupper(str[rank])) {
            str[rank] = tolower(str[rank]);
        } else {
            str[rank] = toupper(str[rank]);
        }
        printf("Process %d: Toggled character = %c\n,%s", rank, str[rank],str);
    }

    MPI_Finalize();
    return 0;
}
