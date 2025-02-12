#include<stdio.h>
#include<mpi.h>
#include<ctype.h>
#include<string.h>

int main(int argc, char *argv[]){
    int rank,size;
    char str1[100];
    char str2[100];
    char temp1[100];
    char temp2[100];
    int lens;
    int chunk_size;
    char merged[100];
    char final[100];

    MPI_Init(&argc,&argv);
    MPI_Comm_rank(MPI_COMM_WORLD,&rank);
    MPI_Comm_size(MPI_COMM_WORLD,&size);
     
    if(rank==0){
        fprintf(stdout,"enter string1:");
        fflush(stdout);
        fgets(str1, sizeof(str1), stdin);
        str1[strcspn(str1,"\n")]='\0';

        fprintf(stdout,"enter string2:");
        fflush(stdout);
        fgets(str2, sizeof(str2), stdin);
        str2[strcspn(str2,"\n")]='\0';

        if(strlen(str1) % size != 0 || strlen(str2) % size != 0 || strlen(str1) != strlen(str2)) {
            fprintf(stdout, "Strings don't follow the rules.\n");
            fflush(stdout);
            MPI_Finalize();
            return 0;
        }

        lens = strlen(str1);
    }

    MPI_Bcast(&lens,1,MPI_INT,0,MPI_COMM_WORLD);
    
    chunk_size = lens/size;
    if(rank==size-1){
        chunk_size+=lens%size;
    }

    MPI_Scatter(str1,chunk_size,MPI_CHAR,temp1,chunk_size,MPI_CHAR,0,MPI_COMM_WORLD);
    MPI_Scatter(str2,chunk_size,MPI_CHAR,temp2,chunk_size,MPI_CHAR,0,MPI_COMM_WORLD);
    
    for(int i =0;i<chunk_size;i++){
        merged[2*i]=temp1[i];
        merged[2*i+1]=temp2[i];
    }

    MPI_Gather(merged,2*chunk_size,MPI_CHAR,final,2*chunk_size,MPI_CHAR,0,MPI_COMM_WORLD);
    if (rank == 0) {
        final[strlen(str1) + strlen(str2)] = '\0';
        printf("Merged string: %s\n", final);
    }

    MPI_Finalize();
    return 0;

    


}