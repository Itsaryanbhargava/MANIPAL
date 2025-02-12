#include<stdio.h>
#include<mpi.h>
#include<ctype.h>
#include<string.h>

int isvowel(char s){
    if(s=='a'||s=='e'||s=='i'||s=='o'||s=='u'||s=='A'||s=='E'||s=='I'||s=='O'||s=='U'){
        return 1;
    }
    return 0;
}

int main(int argc,char *argv[]){
    int rank,size;
    int final_count;
    int lens;

    MPI_Init(&argc,&argv);
    MPI_Comm_rank(MPI_COMM_WORLD,&rank);
    MPI_Comm_size(MPI_COMM_WORLD,&size);

    char str[100];
    char tstr[100];

    if(rank==0){
        fprintf(stdout,"enter a string:");
        fflush(stdout);
        fgets(str,sizeof(str),stdin);
        str[strcspn(str,"\n")]='\0';

        lens = strlen(str);

    }
    MPI_Bcast(&lens,1,MPI_INT,0,MPI_COMM_WORLD);
    int chunk_size = lens/size;

    if(rank ==size-1){
        chunk_size+=lens%size;
    }

    MPI_Scatter(str,chunk_size,MPI_CHAR,tstr,chunk_size,MPI_CHAR,0,MPI_COMM_WORLD);
    
    int count =0;
    for(int i =0;i<chunk_size;i++){
        if(isvowel(tstr[i])){
            count+=1;
        }
    }
    MPI_Reduce(&count,&final_count,1,MPI_INT,MPI_SUM,0,MPI_COMM_WORLD);

    

    if(rank==0){
        fprintf(stdout,"The number of vowels in the string is %d",final_count);
        fflush(stdout);
    }
    MPI_Finalize();
    return 0;

}