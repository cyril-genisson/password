#!/usr/bin/env python3
#
# Project: Password Generator
# Filename: main.py
# Created: 12/03/2024
#
# License: GPLv3
#
# Author: Cyril GENISSON
#
import hashlib
import random
import json


class Password:
    def __init__(self):
        self.mini = 8
        self.file = "save_passwd_hash.json" 
        self.car = {
                "Maj": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                "Min": "abcdefghijklmnopqrstuvwxyz",
                "Num": "0123456789",
                "Spe": "!@#$%^&*"
                }
        self.string = self.car["Maj"] + self.car["Min"] + self.car["Num"] + self.car["Spe"]

        try:
            with open(self.file, encoding="utf-8") as f:
                self.data = json.load(f)
        except:
            self.data = []


    def valide(self, s: str) -> bool:
        state = [False, False, False, False, False, True]
        if len(s) >= self.mini:
            state[0] = True
        for k in s:
            if k in self.car["Maj"]:
                state[1] = True
            if k in self.car["Min"]:
                state[2] = True
            if k in self.car["Num"]:
                state[3] = True
            if k in self.car["Spe"]:
                state[4] = True
            if k not in self.string:
                state[5] = False
        if sum(state) == 6:
            return True
        else:
            return False


    def ask_password(self):
        run = True
        while run:
            p = input("Veuillez saisir un mot de passe: ")
            if self.valide(p):
                hash_p = self.hash_password(p)
                if not self.compare(hash_p):
                    print("Mot de passe validé et enregistré")
                    print(f"mot de passe: {p}\nHash: {self.hash_password(p)}\n")
                    self.save_hash(hash_p)
                    run = False
                else:
                    print("Vous avez déjà utilisé ce mot de passe...")
                    continue
            else:
                print("Le mot de passe de répond pas aux critères de sécurités:")
                print("\t-> 8 caractères minimum,")
                print("\t-> au moins 1 majuscule,")
                print("\t-> au moins 1 minuscuke,")
                print("\t-> au moins 1 chiffre,")
                print("\t-> au moins 1 caractère spécial parmis ! @ # $ % ^ & *")


    def hash_password(self, s: str) -> str:
        return hashlib.sha256(s.encode()).hexdigest()

    
    def compare(self, s: str) -> bool:
        if s not in self.data:
            return False
        return True


    def save_hash(self, s: str) -> None:
        self.data.append(s)


    def generate_password(self):
        runner = True
        while runner:
            tmp = ""
            for k in range(self.mini):
                tmp += random.choice(self.string)
            hash_tmp = self.hash_password(tmp)
            if self.valide(tmp) and not self.compare(hash_tmp):
                self.save_hash(hash_tmp)
                runner = False
        return tmp

    def exit(self):
        with open(self.file, 'w', encoding="utf-8") as f:
            json.dump(self.data, f)
        exit(0)


def menu() -> None:
    print("Choix 1: créer un mot de passe")
    print("Choix 2: génération automatique d'un mot de passe")
    print("Choix 3: consulter les mots de passes enregistrés")
    print("Choix 4: sortir du programme\n")


def main():
    p = Password()
    print(f"{'*' * 80}")
    print(f"{'Gestionnaire de mot de passe': ^80}")
    print(f"{'*' * 80}")
    while True:
        menu()
        choix = input("Choisir votre option: ")
        match choix:
            case '1':
                p.ask_password()
            case '2':
                password = p.generate_password()
                print(f"mot de passe: {password}")
                print(f"Hash: {p.hash_password(password)}")
                print()
            case '3':
                for k in p.data:
                    print(f"{k}")
                print()
            case '4':
                print("Bye")
                p.exit()
            case _:
                print("L'option choisie est incorrecte.\n")
    p.exit()
    
if __name__ == "__main__":
    main()
