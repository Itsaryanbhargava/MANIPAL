#include<stdio.h>
#include<mpi.h>
#include<string.h>
#include<ctype.h>

void reverse_string(char *str) {
    int len = strlen(str);
    for (int i = 0; i < len / 2; i++) {
        char temp = str[i];
        str[i] = str[len - i - 1];
        str[len - i - 1] = temp;
    }
}

int main(int argc, char *argv[]){
    int rank,size;

    MPI_Init(&argc,&argv);

    MPI_Comm_rank(MPI_COMM_WORLD,&rank);
    MPI_Comm_size(MPI_COMM_WORLD,&size);

    char sentence[500];

    char words[100][50];
    char result[100][50];

    char word[100];

    int wlength;
    int num_words=0;
    int wordlength[100];

    if(rank ==0){
        fprintf(stdout,"Enter a sentence:");
        fflush(stdout);
        fgets(sentence,sizeof(sentence),stdin);

        sentence[strcspn(sentence,"\n")]='\0';

        char *token = strtok(sentence," ");

        while(token!=NULL){
            strcpy(words[num_words],token);
            wordlength[num_words]=strlen(token);
            num_words++;
            token = strtok(NULL," ");
        }

        if(num_words<size){
            fprintf(stdout,"the number of words should be equal to the number of processes");
            fflush(stdout);
            MPI_Abort(MPI_COMM_WORLD,1);
        }

    }

    // MPI_Bcast(&num_words,1,MPI_INT,0,MPI_COMM_WORLD);

    
    MPI_Scatter(words,50,MPI_CHAR,word,50,MPI_CHAR,0,MPI_COMM_WORLD);

    if(rank%2==0){
        for(int i =0;i<strlen(word);i++){
            word[i]=toupper(word[i]);
        }
        
    }
    
    reverse_string(word);

    MPI_Gather(word,50,MPI_CHAR,result,50,MPI_CHAR,0,MPI_COMM_WORLD);

    if(rank==0){
        fprintf(stdout,"The reversed sentence is: ");
        fflush(stdout);
        for(int i =0;i<num_words;i++){
            fprintf(stdout,"%s ",result[i]);
            fflush(stdout);
        }
    }

    MPI_Finalize();
    return 0;
}
