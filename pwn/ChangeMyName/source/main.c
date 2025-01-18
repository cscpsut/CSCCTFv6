#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>



void setup(){
    setvbuf(stdout,(char *)0x0,2,0);
    setvbuf(stderr,(char *)0x0,2,0);
    setvbuf(stdin,(char *)0x0,2,0);
  
        

}


void menu(){
    printf("Welcome to Fawaz's Machine!\n");
    printf("Menu:\n");
    printf("1. Register\n");
    printf("2. Enter as Guest\n");
    printf("3. Exit\n");
    printf("Enter your choice > ");
}
void main(){
    setup();
    menu();

    char new_user[100];
    long user = 0x75736572;
    int choice;
    char inp[16];
    char password_input[64];

    

    fgets(inp, sizeof(inp), stdin);
    choice = atoi(inp);
    memset(inp, 0, 16);

    if (choice == 1){
        printf("Enter your name: ");
        scanf("%s",&new_user);
        printf("Welcome, ");
        printf(new_user);
        printf("\n");

    }
    else if (choice == 2){
        printf("Hello, guest!\n" );
    }
    else if (choice == 3){
        exit(0);
    }
    else{
        printf("Invalid choice\n");
        exit(0);
    }
    printf("%p",user);
    
    if (user == 0x466177617a){
            FILE *file = fopen("password.txt", "r");
    
    if (file == NULL) {
        printf("password.txt is missing!\n");
        exit(0);
        }
    char password[64];
    char *pass = password;
    fgets(password, sizeof(password), file);
        printf("Enter Admin password: \n");
        scanf("%7s",password_input);

        if (strcmp(password, password_input) == 0){
        printf("Hello, Fawaz!\n");
        printf("poppin shell..\n");
        system("/bin/sh");}
        else{
            printf("Wrong password\n");
            exit(0);
    }
    }
    
    else{
        printf("U aint admin lol\n");
        exit(1337);
    }
    return 0;
    }