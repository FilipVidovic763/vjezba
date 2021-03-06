import sys
import random

from hut import Hut
from knight import Knight
from orcrider import OrcRider
from gameutils import print_bold

class AttackOfTheOrcs:
    """Glavna klasa za igru napad orkova"""
    def __init__(self):
        self.huts = []
        self.player = None

    def get_occupants(self):
        """Vraca listu okupanata za sve kucice
        """
        return [x.get_occupant_type() for x in self.huts]

    def show_game_mission(self):
        """Ispis misije igre"""
        print_bold("Misija:")
        print("  1. Bori se s neprijateljem.")
        print("  2. Stavi sve kucice pod svoju kontrolu")
        print("---------------------------------------------------------\n")

    def _process_user_choice(self):  # zasticena metoda
        """metoda za obradu korisnickog unosa broja kucice"""
        verifying_choice = True
        idx = 0
        print("Trenutni okupanti: {}". format(self.get_occupants()))
        while verifying_choice:
            user_choice = input("Odaberite broj kucice (1-5): ")
            # hvataj iznimku ako se ne unese broj            
            try:
                idx = int(user_choice)    
            except ValueError:
                raise NijeBroj
            
            if idx > 5:
                raise PrevelikBroj()
            if idx == 0:
                raise BrojNula()
            if idx < 0:
                raise NegativanBroj()
            # hvataj iznimku ako se unese neodgovarajuci indeks
            try:
                if self.huts[idx-1].is_acquired:
                    print("Ova kucica je vec pod vasom kontrolom. Pokusajte ponovno."
                        "<INFO: Ne možete ozdraviti u kucici koja je vec pod vasom kontrolom.>")
                else:
                    verifying_choice = False
            except IndexError:
                print('Krivi unos: ',idx)
                print('Broj mora biti u rasponu 1-5. Pokušaj ponovno!')

        return idx


    def _occupy_huts(self):
        """Metoda koja koristi random funkciju za nastambu kucica s prijatelj, neprijatelj ili 'None'"""
        for i in range(5):
            choice_lst = ['neprijatelj', 'prijatelj', None]
            computer_choice = random.choice(choice_lst)
            if computer_choice == 'neprijatelj':
                name = 'neprijatelj-' + str(i+1)
                self.huts.append(Hut(i+1, OrcRider(name)))
            elif computer_choice == 'prijatelj':
                name = 'vitez-' + str(i+1)
                self.huts.append(Hut(i+1, Knight(name)))
            else:
                self.huts.append(Hut(i+1, computer_choice))

    def play(self):
        """Metoda za pokretanje igre
        """
        self.player = Knight()
        self._occupy_huts()
        acquired_hut_counter = 0

        self.show_game_mission()
        self.player.show_health(bold=True)

        while acquired_hut_counter < 5:
            try:
                idx = self._process_user_choice()
                self.player.acquire_hut(self.huts[idx-1])

                if self.player.health_meter <= 0:
                    print_bold("Izgubili ste  :(")
                    break

                if self.huts[idx-1].is_acquired:
                    acquired_hut_counter += 1
            except KeyboardInterrupt:
                print('nKorisnik je izašao iz igre.')
                # izadji iz programa
                sys.exit(1)

        if acquired_hut_counter == 5:
            print_bold("Cestitke! Pobijedili ste!!!")


if __name__ == '__main__':
    game = AttackOfTheOrcs()
    game.play()