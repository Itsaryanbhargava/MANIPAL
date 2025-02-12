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
    char word[100];

    if(rank==0){
        fprintf(stdout,"enter a word: ");
        fflush(stdout);
        
        fgets(word, sizeof(word), stdin);
        

        word[strcspn(word,"\n")]='\0';

        MPI_Ssend(word,strlen(word)+1,MPI_CHAR,1,0,MPI_COMM_WORLD);
        MPI_Recv(word,100,MPI_CHAR,1,0,MPI_COMM_WORLD,&status);

        printf("Process 0 received toggled word: ");
        fputs(word,stdout);
        printf("\n");
    }else if(rank==1){
        MPI_Recv(word,100,MPI_CHAR,0,0,MPI_COMM_WORLD,&status);
        toggle(word);
        MPI_Ssend(word,strlen(word)+1,MPI_CHAR,0,0,MPI_COMM_WORLD);
    }


    MPI_Finalize();
    return 0;
}