from Crypto.Util.number import *
from secret import FLAG

e = 65537
m = bytes_to_long(FLAG)

class Court:
    def __init__(self):
        self.jury = [getPrime(16) for _ in range(10)]
        for i, juror in enumerate(self.jury):
            print(f"Juror {i + 1} has been seated, known as {juror}")
        
    def verdict(self, defendant):
        if len(bin(defendant)) <= len(bin(m)) or defendant <= 0:
            return "Guilty"
        
        for juror in self.jury:
            if pow(juror, defendant - 1, defendant) != 1:
                return "Guilty"
            
        return "Innocent"
    
    

welcome = r"""
                                                              
                                                              
              @@@            @@%%                       ==    
             @@@@@      =    @@@@                             
             @@@@#*%@@%#**   @@@@@                            
              @@@@@%@@@@@@@@@@@@@@@                           
               @@@@@@@@@@@@@@@@@@@@@@@                        
               %@@      @@@@@@@@@@@@@@@@@@                    
              =%%#           @@@@@@@@@@@@@@@@=*%@             
              ##@%            @@@@ @@@@@@@@@@@@@@             
           =  %@@@#          @@@@@        @@@@@@@@            
             @ @@@%%          @@@            @@@              
            @@  @@ %         @@@@@    =      @@@%             
           @@   @@  @        @@@@@          %%@@@#            
           @@  @@@  @@       @@@@@          %%@@ %%           
          @%   @@@  @@        @@@          @@ @@ %%%          
          @    @@@   @@       @@@          @  @@  %%          
         %@     @%    @@      @@@         @   @@   %%         
        %@     @@@    @@      @@@        @@   @@    %@        
       @@       @@     @@     @@@       #%    @@     @@  =    
      @@%######@@@@@@@@@@@@  @@@@@     %%%    @@     @@@#     
     @@@@@@@@@@@@@@@@@@@@@@  @@@@@    @@@@@@@@@@@@@@@@@@@     
       @@@@@@@@@@@@@@@@@@  @@@@@@@@@   @@@@@@@@@@@@@@@@       
          %%%@@@@@@@@@     @@@@@@@@@      %@@@@@@@%%          
                             @@@@@                            
              ===       @@@@@@@@@@@@@@@      = =              
               =    @@@@@@@@@@@@@@@@@@@@@@    =               
           =       @@@@@@@@@@@@@@@%%%%@%@@@%                  
                @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                
               @@@@@@@@@@@@@@@@@@@@@%%##%%%@@@@               
               @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@               
                       @@@@@@@@@@@@@@@@@@                     
                                                              
                                                              
"""
    
def main():
    print(welcome)
    print("All rise!!!!")
    print(f"This court is now in session. We are here to hear the case of CBL, M0tH3r5h1P, and G2 versus Luigi, Case Number {len(bin(m)) - 2}.")
    print("This is a civil matter regarding a dispute over unpaid prizes from a competition")
    print("The jury will now be seated.")
    court = Court()
    print("The defendant will now be brought in.")
    print("Defendant, please state your name.")
    name = int(input("My name is (hex): "), 16)
    print("What is your plea?")
    plea = int(input("My plea is (hex): "), 16)
    print("What is your defense?")
    defense = int(input("My defense is (hex): "), 16)
    num = name * plea * defense
    print("The jury will now deliberate.")
    verdict = court.verdict(num)
    if verdict == "Guilty":
        print("The jury finds the defendant guilty.")
        print("The defendant is hereby sentenced to answering CSC tickets for the rest of their life.")
        return
    else:
        print("The jury finds the defendant innocent.")
        print(f"Here is your flag: {pow(m, e, num)}")
        return
    

if __name__ == "__main__":
    main()


