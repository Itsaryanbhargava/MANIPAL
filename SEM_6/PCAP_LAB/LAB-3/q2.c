#include<stdio.h>
#include<stdlib.h>
#include<mpi.h>
#include<string.h>
#include<ctype.h>

int main(int argc,char*argv[]){
    int rank,size;
    
    int m=2;
    MPI_Init(&argc,&argv);
    MPI_Comm_rank(MPI_COMM_WORLD,&rank);
    MPI_Comm_size(MPI_COMM_WORLD,&size);
    MPI_Status status;

    double avg = 0;
    double result[m];

    int arr[size*m];
    int temp[m];

    if(rank==0){
        fprintf(stdout,"enter %d elements",size*m);
        fflush(stdout);

        for(int i =0;i<size*m;i++){
            
            scanf("%d",&arr[i]);
            
        }
    }
    MPI_Scatter(arr,m,MPI_INT,temp,m,MPI_INT,0,MPI_COMM_WORLD);

    for(int i =0;i<m;i++){
        avg+=temp[i];
    }
    avg/=m;

    MPI_Gather(&avg,1,MPI_DOUBLE,result,1,MPI_DOUBLE,0,MPI_COMM_WORLD);

    if(rank==0){
        double final=0;
        for(int i =0;i<size;i++){
            final+=result[i];
        }
        final/=size;
        fprintf(stdout,"The average of the numbers is %f",final);
        fflush(stdout);
    }
    MPI_Finalize();
    return 0;

    

    
}