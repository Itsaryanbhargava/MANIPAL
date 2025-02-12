#include<stdio.h>
#include<mpi.h>
#include<math.h>

int main(int argc, char*argv[]){
    int rank,size;

    MPI_Init(&argc,&argv);
    MPI_Comm_rank(MPI_COMM_WORLD,&rank);
    MPI_Comm_size(MPI_COMM_WORLD,&size);

    int a =3;
    int b =2;

    switch(rank){
        case 0:
            printf("Process %d: %d + %d = %d\n", rank, a, b, a+b);
            break;
        case 1:
            printf("Process %d: %d - %d = %d\n", rank, a, b, a-b);
            break;
        case 2:
            printf("Process %d: %d * %d = %d\n", rank, a, b, a*b);
            break;
        case 3:
            printf("Process %d: %d / %d = %d\n", rank, a, b, a/b);
            break;
        case 4:
            printf("Process %d: %d %% %d = %d\n", rank, a, b, a%b);
            break;
        default:
            printf("Process %d: Invalid operation\n", rank);
            break;
    }
    MPI_Finalize();
    return 0;
    
    
}