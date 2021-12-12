import React, {Component} from 'react';
import logo from './logo.svg';
import './App.css';
import GameSelector from "./GameSelector";
import GameCard from "./GameCard";

interface AppState {
  games: GameObj[];
  suggestions: string[]
}

// Holds the game object: Equivalent to gameobj on the serverside
class GameObj {
    constructor(
        public name: string,
        public genre: string[],
        public developer: string[],
        public publisher: string[],
        public series: string,
        public seriesGames: string[],
        public related: string[],
        public prices: Map<string, number>,
        public platforms: Map<string, string>[],
        public timeToBeat: number,
        public url: string,
        public coverArt: string,
        public opencritic: number,){}
}

class App extends Component<{}, AppState> {
    constructor(props: any) {
        super(props);
        this.state = {
            games: [],
            suggestions: []
        };

        this.requestGame = this.requestGame.bind(this);
        this.getSuggestion = this.getSuggestion.bind(this);
        this.addGame = this.addGame.bind(this);
    }

    //TODO: Remove placeholder code
  requestGame = async() =>{
        try{
            console.log("Nothing")
        } catch (e) {
            alert("Error while attempting to contact the server.");
        }
    }

    getSuggestion = async (keyword: string) => {
        console.log(keyword)
        try {
            let url =  "http://localhost:4567/autocomplete?key=" + keyword;
            let responsePromise = fetch(url);
            let response = await responsePromise;
            if (!response.ok) {
                alert("Error " + response.status);
                return;
            }
            let parsedObject = await response.json();
            console.log(parsedObject)
            this.setState({suggestions: parsedObject});
        } catch (e) {
            alert("There was an error getting autocomplete suggestions from the server.\nIs the server running right now?");
            console.log(e);
        }
    }


    addGame = async(name: string) => {
        console.log(name)
        try{
            let url = "http://localhost:4567/addgame?name=" + name;
            let responsePromise = fetch(url);
            let response = await responsePromise;
            if(!response.ok){
                alert("Error " + response.status)
            }
            let parsedObject = await response.json();
            console.log(parsedObject)
            // Construct a new game object from the returned data
            let newGame:GameObj = new GameObj(
                parsedObject['name'],
                parsedObject['genre'],
                parsedObject['developer'],
                parsedObject['publisher'],
                parsedObject['series'],
                parsedObject['series_games'],
                parsedObject['related'],
                parsedObject['prices'],
                parsedObject['platforms'],
                parsedObject['time_to_beat'],
                parsedObject['url'],
                parsedObject['cover_art'],
                parsedObject['opencritic']
            )
            this.setState({
                games: [...this.state.games, newGame],
                suggestions: [],
            })
        } catch (e) {
            alert("There was an error adding game to the server. .\nIs the server running right now?")
        }
    }


  render() {
    let gamecards:  any[] = [];
      for (let gameEntry of this.state.games) {
          gamecards.push(<GameCard key={gameEntry.name} game={gameEntry}/>)
      }

    return (
        <div className="App">
            <header>Pretend this is a nice logo/header :)</header>
                <label>
                    Add a new game to the watch list:
                    <GameSelector suggestions={this.state.suggestions} onUpdateSearchTerm={this.getSuggestion} onUpdateGame={this.addGame}/>
                </label>
                <br/>
            <br/>
            {gamecards}
        </div>
        );
    }
}

export default App;
