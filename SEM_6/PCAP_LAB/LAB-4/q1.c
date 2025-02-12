#include<stdio.h>
#include<mpi.h>
#include<string.h>
#include<ctype.h>
#include<math.h>

int factorial(int n){
    if(n==0){
        return 1;
    }
    return factorial(n-1)*n;
}

int main(int argc, char *argv[]){
    int rank,size;

    MPI_Init(&argc,&argv);
    MPI_Comm_rank(MPI_COMM_WORLD,&rank);
    MPI_Comm_size(MPI_COMM_WORLD,&size);

    int n;
    int local_fact;
    int fact_sum;

    if(rank==0){
        fprintf(stdout,"Enter the value of n:");
        fflush(stdout);
        scanf("%d",&n);

        if (n < size) {
            printf("Error: N should be at least the number of processes!\n");
            MPI_Abort(MPI_COMM_WORLD, 1);
        }
    }
    MPI_Bcast(&n,1,MPI_INT,0,MPI_COMM_WORLD);
    if(rank>n){
        local_fact=0;
    }else{
        local_fact = factorial(rank+1);
    }
    

    MPI_Scan(&local_fact,&fact_sum,1,MPI_INT,MPI_SUM,MPI_COMM_WORLD);

    if(rank==size-1){
        fprintf(stdout,"The sum of the factorials of the first %d numbers is %d\n",n,fact_sum);
        fflush(stdout);
    }
    MPI_Finalize();
    return 0;

}