#include<stdio.h>
#include<mpi.h>
#include<math.h>

int fib(int n){
    if(n==0)return 0;
    if(n==1)return 1;
    return fib(n-1)+fib(n-2);
}
int fact(int n){
    if(n==0 || n==1)return 1;
    return n*fact(n-1);
}

int main(int argc,char *argv[]){
    int rank,size;

    MPI_Init(&argc,&argv);
    MPI_Comm_rank(MPI_COMM_WORLD,&rank);
    MPI_Comm_size(MPI_COMM_WORLD,&size);

    if(rank%2==0){
        printf("Process %d: Factorial of %d = %d\n", rank, rank, fact(rank));
    }else{
        printf("Process %d: Fibonacci of %d = %d\n", rank, rank, fib(rank));
    }

    MPI_Finalize();
    return 0;
}