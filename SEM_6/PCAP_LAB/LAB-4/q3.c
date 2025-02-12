#include<stdio.h>
#include<mpi.h>
#include<ctype.h>

int main(int argc, char *argv[]){
    int rank,size;

    MPI_Init(&argc,&argv);
    MPI_Comm_rank(MPI_COMM_WORLD,&rank);
    MPI_Comm_size(MPI_COMM_WORLD,&size);

    int matrix[4][4];
    int row[4];
    int scan_row[4];
    int result[4][4];

    if(size!=4){
        if(rank==0){
            fprintf(stdout,"Error: This program requires exactly 4 processes.\n");
            fflush(stdout);
        }
        MPI_Abort(MPI_COMM_WORLD,1);
    }

    if(rank==0){
        fprintf(stdout,"enter the elements of a 4x4 matrix:");
        fflush(stdout);

        for (int i = 0; i < 4; i++) {
            for (int j = 0; j < 4; j++) {
                scanf("%d", &matrix[i][j]);
            }
        }
    }

    MPI_Scatter(matrix,4,MPI_INT,row,4,MPI_INT,0,MPI_COMM_WORLD);
    MPI_Scan(row,scan_row,4,MPI_INT,MPI_SUM,MPI_COMM_WORLD);
    MPI_Gather(scan_row,4,MPI_INT,result,4,MPI_INT,0,MPI_COMM_WORLD);

    if(rank==0){
        fprintf(stdout,"The matrix is:\n");
        fflush(stdout);
        for(int i =0;i<4;i++){
            for(int j =0;j<4;j++){
                fprintf(stdout,"%d ",result[i][j]);
                fflush(stdout);
            }
            fprintf(stdout,"\n");
            fflush(stdout);
        }
    }
    MPI_Finalize();
    return 0;
}