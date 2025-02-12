#include<stdio.h>
#include<mpi.h>
#include<string.h>
#include<ctype.h>

int countsi(int row[],int target){
    int count =0;
    for(int i =0;i<3;i++){
        if(row[i]==target){
            count+=1;
        }
    }
    return count;
}

int main(int argc, char *argv[]){
    int rank,size;
    
    MPI_Init(&argc,&argv);
    MPI_Comm_rank(MPI_COMM_WORLD,&rank);
    MPI_Comm_size(MPI_COMM_WORLD,&size);

    if (size != 3) {
        if (rank == 0) {
            fprintf(stdout, "Error: This program requires exactly 3 processes.\n");
            fflush(stdout);
        }
        MPI_Abort(MPI_COMM_WORLD, 1);
    }

    int matrix[3][3];
    int local_count;
    int global_count;
    int target;

    if(rank==0){
        fprintf(stdout,"Enter the values of the 3x3 matrix:");
        fflush(stdout);

        for(int i =0;i<3;i++){
            for(int j =0;j<3;j++){
                scanf("%d",&matrix[i][j]);
            }
        }

        printf("Enter the element to search for: ");
        scanf("%d", &target);
    }
    MPI_Bcast(&target,1,MPI_INT,0,MPI_COMM_WORLD);
    MPI_Bcast(matrix, 3 * 3, MPI_INT, 0, MPI_COMM_WORLD);

    local_count = countsi(matrix[rank],target);

    MPI_Scan(&local_count,&global_count,1,MPI_INT,MPI_SUM,MPI_COMM_WORLD);

    if(rank==size-1){
        fprintf(stdout,"The number of times %d occurs in the matrix is %d\n",target,global_count);
        fflush(stdout);
    }
    MPI_Finalize();
    return 0;
}