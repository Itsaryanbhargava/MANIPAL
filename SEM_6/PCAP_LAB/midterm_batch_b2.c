#include<stdio.h>
#include<mpi.h>
#include<string.h>
#include<ctype.h>
int isVowel(char s){
    if(s=='a'||s=='e'||s=='i'||s=='o'||s=='u'||s=='A'||s=='E'||s=='I'||s=='O'||s=='U'){
        return 1;
    }
    return 0;
}


int main(int argc, char *argv[]){
    int rank,size;

    char word[100],chunk[100],final_word[100];
    int n,chunk_size;

    MPI_Init(&argc,&argv);
    MPI_Comm_rank(MPI_COMM_WORLD,&rank);
    MPI_Comm_size(MPI_COMM_WORLD,&size);
    MPI_Status status;

    if(rank ==0){
        fprintf(stdout,"enter a word:");
        fflush(stdout);

        fgets(word,sizeof(word),stdin);
        word[strcspn(word,"\n")]='\0';

        n = strlen(word);

        if(n%size!=0){
            fprintf(stdout,"Error: The length of the word should be divisible by the number of processes.\n");
            fflush(stdout);
            MPI_Abort(MPI_COMM_WORLD,1);
        }

        chunk_size = n/size;

        for(int i =0;i<size;i++){
            MPI_Send(&word[i*chunk_size],chunk_size,MPI_CHAR,i,0,MPI_COMM_WORLD);
        }


    }
    MPI_Bcast(&chunk_size, 1, MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Recv(chunk,chunk_size,MPI_CHAR,0,0,MPI_COMM_WORLD,&status);


    for(int i =0;i<chunk_size;i++){
        if(isVowel(chunk[i])){
            if(rank%2==0){
                chunk[i]='$';

            }else{
                chunk[i]='#';
            }
        }else{
            if(rank%2==0){
                chunk[i]='#';
            }else{
                chunk[i]='$';
            }
        }
    }

    MPI_Gather(chunk,chunk_size,MPI_CHAR,final_word,chunk_size,MPI_CHAR,0,MPI_COMM_WORLD);

    if(rank==0){
        final_word[n]='\0';
        fprintf(stdout,"The final word is: ");
        fflush(stdout);
        fputs(final_word,stdout);
        fprintf(stdout,"\n");
        fflush(stdout);
    }

    MPI_Finalize();
    return 0;
}
