"""
Lo scopo della prova è creare una classe, che gestisce una collezione di film costituita dal 
file movies.json. 
Il file condiviso è già popolato con una decina di film, da usare come riferimento. 
Ogni film è caratterizzato dai campi title e director che sono stringhe, year che è un numero 
intero e genre che è una lista di stringhe. 
La classe, dovrà chiamarsi MovieLibrary e dovrà essere definita all’interno del file 
movie_library.py. 
La classe dovrà avere due attributi di istanza, inizializzati nel metodo costruttore. 
Il primo va chiamato json_file, e deve essere inizializzato passando, in fase di creazione 
oggetto, 
il percorso assoluto del file movies.json sul vostro pc.  
Il secondo va chiamato movies e rappresenta la collezione di film. 
Deve essere inizializzato col contenuto del file json de-serializzato. 
In pratica sarà una lista di dizionari, dove ogni dizionario rappresenta un film. 
Ogni modifica che viene effettuata a movies, in qualsiasi metodo, deve immediatamente 
riflettersi sul file movies.json. 
Il cuore della prova sono i metodi della classe. 
La prova è infatti suddivisa in 18 esercizi, ciascuno riguardante la creazione di un metodo o 
la modifica di un metodo esistente.
"""
import json
import os
from collections import Counter

class MovieLibrary:

    class MovieNotFoundError(Exception):
        pass

        # Inizializza la classe con il percorso del file JSON.
    def __init__(self, json_file=r"C:\Users\bipbo\Documents\GitHub\Programing_principles-esame\movies (1).json"):
        self.json_file = json_file
        self.movies = []
       

    #ES17
        if not os.path.exists(self.json_file):
            raise FileNotFoundError(f"The file {self.json_file} does not exist.")

        # Carica i film dal file JSON nella variabile di istanza `movies`.
        with open(self.json_file, 'r', encoding='utf-8') as f:
            self.movies = json.load(f)

    def __update_json_file(self):
        # Aggiorna il contenuto del file JSON con i dati aggiornati della collezione `movies`.
        # Questo metodo garantisce la persistenza dei dati dopo ogni modifica.
        with open(self.json_file, 'w', encoding='utf-8') as f:
            json.dump(self.movies, f, indent=4)

    #ES18
    def get_movie_or_raise(self, title: str):
        try:
            return next(movie for movie in self.movies if movie.get('title') == title)
        except StopIteration:
            raise self.MovieNotFoundError("Movie was not found")

    def update_movie(self, title: str, updated_data: dict):
        # Aggiorna un film esistente con i dati forniti e aggiorna il file JSON.
        movie_to_update = self.get_movie_or_raise(title)
        movie_to_update.update(updated_data)
        self.__update_json_file()

    # ES1
    # Crea un metodo chiamato get_movies che restituisce l'intera collezione di film.

    def get_movies(self):
        # Restituisce l'intera collezione di film come lista di dizionari.
        return self.movies

    # ES2
    # Crea un metodo chiamato add_movie che ha i parametri title e director di tipo stringa,
    # year di tipo intero e genres di tipo lista (di stringhe).
    # Il metodo aggiunge il film alla collezione e aggiorna il file json.

    def add_movie(self, title: str, director: str, year: int, genres: list[str]) -> None:
        # Aggiunge un nuovo film alla collezione. 
        # Ogni film è rappresentato come un dizionario con i campi obbligatori.
        new_movie = {
            "title": title,
            "director": director,
            "year": year,
            "genres": genres
        }
        self.movies.append(new_movie)
        self.__update_json_file()  # Aggiorna il file JSON per salvare la modifica.

    # ES3
    # Crea un metodo chiamato remove_movie che ha il parametro title.
    # Il metodo rimuove dalla collezione il film che ha titolo corrispondente (NON case sensitive) a title.
    # Il metodo aggiorna il file json e restituisce il film rimosso.

    def remove_movie(self, title: str):
        for movie in self.movies:
            if movie["title"].lower() == title.lower():
                self.movies.remove(movie)
                self.__update_json_file()
                return movie
        raise self.MovieNotFoundError(f"Movie '{title}' not found.")

    # ES4
    # Crea un metodo chiamato update_movie che ha il parametro title e i parametri opzionali director, year e genres.
    # Il metodo ricerca nella collezione il film che ha titolo corrispondente (NON case sensitive) a title.
    # Quindi modifica il film, applicando il valore di ciascun parametro opzionale non nullo.
    # Il metodo aggiorna il file json e restituisce il film coi valori aggiornati.

    def update_movie(self, title, director=None, year=None, genres=None):
        for movie in self.movies:
            if movie["title"].lower() == title.lower():
                if director is not None:
                    movie["director"] = director
                if year is not None:
                    movie["year"] = year
                if genres is not None:
                    movie["genres"] = genres
                self.__update_json_file()
                return movie
        raise self.MovieNotFoundError(f"Movie '{title}' not found.")

    # ES5
    # Crea un metodo chiamato get_movie_titles che restituisce una lista contenente
    # tutti i titoli dei film nella collezione.

    def get_movies_title(self):
        # Restituisce una lista contenente solo i titoli dei film.
        return [movie["title"] for movie in self.movies]

    # ES6
    # Crea un metodo chiamato count_movies che restituisce il numero totale dei film nella collezione.

    def count_movies(self):
        # Restituisce il numero totale di film nella collezione.
        return len(self.movies)

    # ES7
    # Crea un metodo chiamato get_movie_by_title che ha il parametro title.
    # Il metodo restituisce il film che ha titolo corrispondente (NON case sensitive) a title.

    def get_movie_by_title(self, title: str):
        # Cerca un film con il titolo specificato (non case sensitive).
        for movie in self.movies:
            if movie["title"].lower() == title.lower():
                return movie
        # Solleva un'eccezione se il film non viene trovato.
        raise self.MovieNotFoundError(f"Movie '{title}' not found.")

    # ES8
    # Crea un metodo chiamato get_movies_by_title_substring che ha il parametro substring.
    # Il metodo restituisce una lista di tutti i film che contengono, nel titolo,
    # una sottostringa corrispondente (case sensitive) a substring.

    def get_movies_by_title_substring(self, substring: str):
        # Cerca tutti i film i cui titoli contengono la sottostringa specificata (case sensitive).
        matching_movies = []
        for movie in self.movies:
            if substring in movie["title"]:
                matching_movies.append(movie)

        if not matching_movies:
            # Solleva un'eccezione se nessun film corrisponde
            raise self.MovieNotFoundError(f"No movies found containing '{substring}'.")
        return matching_movies

    # ES9
    # Crea un metodo chiamato get_movies_by_year che ha il parametro year.
    # Il metodo restituisce una lista di tutti i film con anno corrispondente a year.

    def get_movies_by_year(self, year: int):
        # Restituisce una lista di film pubblicati nell'anno specificato.
        result = []
        for movie in self.movies:
            if movie["year"] == year:
                result.append(movie)

        if not result:
            # Solleva un'eccezione se non ci sono film corrispondenti.
            raise self.MovieNotFoundError(f"No movies found for year {year}.")
        return result

    # ES10
    # Crea un metodo chiamato count_movies_by_director che ha il parametro director.
    # Il metodo restituisce un numero intero che rappresenta quanti film del director scelto
    # sono presenti nella collezione. Il director va confrontato in modo NON case sensitive.

    def count_movies_by_director(self, director: str) -> int:
        # Conta il numero di film diretti da un regista specifico (non case sensitive).
        count = 0
        for movie in self.movies:
            if movie["director"].lower() == director.lower():
                count += 1

        if count == 0:
            # Solleva un'eccezione se non ci sono film per il regista specificato.
            raise self.MovieNotFoundError(f"No movies found for director '{director}'.")
        return count

    # ES11
    # Crea un metodo chiamato get_movies_by_genre che ha il parametro stringa genre.
    # Il metodo restituisce una lista di tutti i film che hanno genere corrispondente a genre
    # (NON case sensitive).

    def get_movies_by_genre(self, genre: str) -> list:
        # Restituisce una lista di film appartenenti a un determinato genere (non case sensitive).
        matching_movies = []
        for movie in self.movies:
            if any(g.lower() == genre.lower() for g in movie["genres"]):
                matching_movies.append(movie)

        if not matching_movies:
            raise self.MovieNotFoundError(f"No movies found for genre '{genre}'.")
        return matching_movies

    # ES12
    # Crea un metodo chiamato get_oldest_movie_title che restituisce
    # il titolo del film più antico della collezione.

    def get_oldest_movie_title(self) -> str:
        # Trova e restituisce il titolo del film più antico.
        if not self.movies:
            return None

        oldest_movie = self.movies[0]
        for movie in self.movies[1:]:
            if movie["year"] < oldest_movie["year"]:
                oldest_movie = movie

        return oldest_movie["title"]

    # ES13
    # Crea un metodo chiamato get_average_release_year che restituisce
    # un float rappresentante la media aritmetica degli anni di pubblicazione dei film.

    def get_average_release_year(self) -> float:
        # Calcola la media degli anni di pubblicazione dei film.
        if not self.movies:
            return 0.0
        total_years = sum(movie["year"] for movie in self.movies)
        avg_year = total_years / len(self.movies)
        return float(avg_year)

    # ES14
    # Crea un metodo chiamato get_longest_title che restituisce
    # il titolo più lungo della collezione di film.

    def get_longest_title(self) -> str:
        # Trova il titolo più lungo nella collezione.
        if not self.movies:
            return None

        longest_movie = self.movies[0]
        for movie in self.movies[1:]:
            if len(movie["title"]) > len(longest_movie["title"]):
                longest_movie = movie
        return longest_movie["title"]

    # ES15
    # Crea un metodo chiamato get_titles_between_years che ha due parametri: start_year e end_year.
    # Il metodo restituisce una lista contenente i titoli dei film pubblicati
    # dall’anno start_year fino all’anno end_year (estremi compresi).

    def get_titles_between_years(self, start_year: int, end_year: int) -> list[str]:
        # Restituisce i titoli dei film pubblicati tra due anni specificati (inclusi).
        titles_in_range = []
        for movie in self.movies:
            if start_year <= movie["year"] <= end_year:
                titles_in_range.append(movie["title"])
        return titles_in_range

    # ES16
    # Crea un metodo chiamato get_most_common_year che restituisce l’anno più frequente
    # fra i film della collezione. Non considerare il caso in cui vi siano pari merito.

    def get_most_common_year(self) -> int:
        # Trova l'anno più frequente tra i film.
        if not self.movies:
            raise self.MovieNotFoundError("Collection is empty.")
        years = [movie["year"] for movie in self.movies]
        year_counts = Counter(years)
        most_common = year_counts.most_common(1)
        return most_common[0][0]
    
# MAIN

if __name__ == "__main__":
    # Questo blocco viene eseguito solo se il file viene eseguito direttamente e non importato come modulo.

    # Specifica il percorso del file JSON contenente la collezione di film.
    json_path = r"C:\Users\bipbo\Documents\GitHub\Programing_principles-esame\movies (1).json"

    try:
        # Crea un'istanza della classe MovieLibrary utilizzando il percorso del file JSON.
        # Se il file non esiste, viene sollevata un'eccezione FileNotFoundError.
        library = MovieLibrary(r"C:\Users\bipbo\Documents\GitHub\Programing_principles-esame\movies (1).json")
    except FileNotFoundError as e:
        # Gestisce l'errore se il file JSON non viene trovato, mostrando un messaggio esplicativo.
        print(e)
    else:
        # ES1: get_movies
        # Stampa l'intera collezione di film per verificare che sia stata caricata correttamente dal file JSON.
        print("All movies:", library.get_movies())

        # ES2: add_movie
        # Aggiunge un nuovo film alla collezione e stampa la collezione aggiornata.
        library.add_movie("Back to the future", "Robert Zemeckis", 1985, ["Commedy", "Sci-Fi", "Action"])
        print("After adding Back to the future:", library.get_movies())

        # ES3: remove_movie
        try:
            # Rimuove il film "Forest Gump" dalla collezione e stampa i dettagli del film rimosso.
            removed = library.remove_movie("Forest Gump")
            print("Film removed:", removed)
        except MovieLibrary.MovieNotFoundError as e:
            # Gestisce il caso in cui il film non esiste nella collezione.
            print("Error removing:", e)

        # Aggiunge di nuovo "Forest Gump" per consentire ulteriori test su altri metodi.
        library.add_movie("Forest Gump", "Robert Zemeckis", 1985, ["Action", "Sci-Fi", "Commedy"])

        # ES4: update_movie
        try:
            # Aggiorna i dettagli del film "Matrix" e stampa il film aggiornato.
            updated = library.update_movie("Matrix", director="Wachowski Brothers", year=1999, genres=["Action", "Sci-Fi"])
            print("Film updated:", updated)
        except MovieLibrary.MovieNotFoundError as e:
            # Gestisce il caso in cui il film da aggiornare non esiste.
            print("Error update:", e)

        # ES5: get_movie_titles
        # Stampa tutti i titoli dei film presenti nella collezione.
        print("All titles of movies:", library.get_movies_title())

        # ES6: count_movies
        # Stampa il numero totale di film nella collezione.
        print("Number of movies:", library.count_movies())

        # ES7: get_movie_by_title
        try:
            # Cerca il film con il titolo "matrix" (non case sensitive) e stampa i dettagli del film trovato.
            matrix_film = library.get_movie_by_title("matrix")  # Non case sensitive
            print("Movie found for title 'matrix':", matrix_film)
        except MovieLibrary.MovieNotFoundError as e:
            # Gestisce il caso in cui il film specificato non viene trovato.
            print("Error:", e)

        # ES8: get_movies_by_title_substring
        try:
            # Cerca tutti i film i cui titoli contengono la sottostringa "ump" e stampa i risultati.
            substring_films = library.get_movies_by_title_substring("ump")
            print("Movies containing 'ump':", substring_films)
        except MovieLibrary.MovieNotFoundError as e:
            # Gestisce il caso in cui nessun film corrisponde alla sottostringa specificata.
            print("Error:", e)

        # ES9: get_movies_by_year
        try:
            # Cerca tutti i film pubblicati nel 1999 e stampa i risultati.
            year_1999_movies = library.get_movies_by_year(1999)
            print("Movies from 1999:", year_1999_movies)
        except MovieLibrary.MovieNotFoundError as e:
            # Gestisce il caso in cui non ci sono film per l'anno specificato.
            print("Error:", e)

        # ES10: count_movies_by_director
        try:
            # Conta quanti film sono stati diretti dai "Wachowski Brothers" e stampa il conteggio.
            director_count = library.count_movies_by_director("Wachowski Brothers")
            print("Movies by 'Wachowski Brothers':", director_count)
        except MovieLibrary.MovieNotFoundError as e:
            # Gestisce il caso in cui il regista specificato non ha diretto alcun film nella collezione.
            print("Error:", e)

        # ES11: get_movies_by_genre
        try:
            # Cerca tutti i film del genere "Action" e stampa i risultati.
            action_movies = library.get_movies_by_genre("Action")
            print("Movies of genre 'Action':", action_movies)
        except MovieLibrary.MovieNotFoundError as e:
            # Gestisce il caso in cui non ci sono film per il genere specificato.
            print("Error:", e)

        # ES12: get_oldest_movie_title
        # Trova e stampa il titolo del film più antico nella collezione.
        oldest_title = library.get_oldest_movie_title()
        print("Oldest movie title:", oldest_title)

        # ES13: get_average_release_year
        # Calcola e stampa la media degli anni di pubblicazione dei film nella collezione.
        avg_year = library.get_average_release_year()
        print("Average release year:", avg_year)

        # ES14: get_longest_title
        # Trova e stampa il titolo più lungo tra i film nella collezione.
        longest_title = library.get_longest_title()
        print("Longest movie title:", longest_title)

        # ES15: get_titles_between_years
        # Cerca e stampa i titoli dei film pubblicati tra il 1990 e il 2000 (inclusi).
        between_titles = library.get_titles_between_years(1990, 2000)
        print("Movies between 1990 and 2000:", between_titles)

        # ES16: get_most_common_year
        try:
            # Trova e stampa l'anno più frequente tra i film nella collezione.
            common_year = library.get_most_common_year()
            print("Most common year:", common_year)
        except MovieLibrary.MovieNotFoundError as e:
            # Gestisce il caso in cui la collezione è vuota.
            print("Error:", e)
            