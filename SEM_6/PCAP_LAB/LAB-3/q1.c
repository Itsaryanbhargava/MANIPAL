#include<stdio.h>
#include<mpi.h>
#include<string.h>
#include<ctype.h>
#include<math.h>
int factorial(int n){
    if(n==0){
        return 1;
    }else{
        return n*factorial(n-1);
    }

}

int main (int argc, char *argv[]){
    int size,rank,fact;

    MPI_Init(&argc,&argv);
    MPI_Comm_size(MPI_COMM_WORLD,&size);
    MPI_Comm_rank(MPI_COMM_WORLD,&rank);
    
    int num, recv[10],arr[10],recv_val;

    if(rank==0){
        fprintf(stdout,"Enter the numbers: ");
        fflush(stdout);
        for(int i =0;i<size;i++){
            scanf("%d",&arr[i]);
        }
    }
    MPI_Scatter(arr,1,MPI_INT,&recv_val,1,MPI_INT,0,MPI_COMM_WORLD);
    printf("Process %d received number: %d\n",rank,recv_val);
    fact = factorial(recv_val);
    MPI_Gather(&fact,1,MPI_INT,recv,1,MPI_INT,0,MPI_COMM_WORLD);

    if(rank ==0){
        fprintf(stdout,"The factorial of the numbers are: ");
        fflush(stdout);
        for(int i =0;i<size;i++){
            fprintf(stdout,"factorial of the number %d is %d\n",arr[i],recv[i]);
            fflush(stdout);
        }
    }

    
    
    MPI_Finalize();
    return 0;
}