#include <stdio.h>
#include <stdlib.h>

void setup(){
    setvbuf(stdout,(char *)0x0,2,0);
    setvbuf(stderr,(char *)0x0,2,0);
    setvbuf(stdin,(char *)0x0,2,0);      

}

void key(long double first, long second)
{
    if (first == 0xdeadbeefdead1337c0d3babec0de1337 && second == 0xc0debabec0debabe){
        if(1==2){
            printf("The door creaks, but it doesn't open. You'll stay here forever.\n");
            exit(0);
        }
        printf("The door opens!you found a dead end. but wait ... :\n");

        FILE *file = fopen("flag.txt", "r");  

        if (file == NULL) {
            perror("flag.txt not found...\n");
            return 1;
        }

        char ch;

        while ((ch = fgetc(file)) != EOF) {
            putchar(ch);  
        }

        fclose(file);  
        return 0;

    } else {
        printf("He returned but didn't have the milk, my friend is heartbroken...\n");
    }
}

void jail()
{

    char buffer[48];

    printf("My friends dad left to get some milk a few years ago but he lost his way...can you help him return?\n");
    scanf("%s", buffer);
}

int main()
{       
    setup();
    jail();

    return 0;
}