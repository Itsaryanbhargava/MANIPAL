#include<stdio.h>
#include<mpi.h>
#include<string.h>
#include<ctype.h>

void toggle(char *word){
    for(int i =0;word[i]!='\0';i++){
        if(isupper(word[i])){
            word[i]=tolower(word[i]);
        }else if(islower(word[i])){
            word[i]=toupper(word[i]);
        }
    }
}

int main(int argc, char *argv[]){
    int rank,size;

    MPI_Init(&argc,&argv);
    MPI_Comm_rank(MPI_COMM_WORLD,&rank);
    MPI_Comm_size(MPI_COMM_WORLD,&size);
    MPI_Status status;
    int num;

    if(rank==0){
        for(int i =1;i<size;i++){
            printf("enter a number:");
            scanf("%d",&num);
            MPI_Send(&num,1,MPI_INT,i,0,MPI_COMM_WORLD);
        }
    }else{
        MPI_Recv(&num,1,MPI_INT,0,0,MPI_COMM_WORLD,&status);
        printf("Process %d received number: %d\n",rank,num);
    }


    MPI_Finalize();
    return 0;
}