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
interface GameObj {
    genre: string[];
    developer: string[];
    publisher: string[];
    series: string;
    seriesGames: string[];
    related: string[];
    prices: Map<string, number>;
    platforms: Map<string, string>[];
    timeToBeat: number;
    url: string;
    coverArt: string;
    opencritic: number;
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
            alert("There was an error getting autocomplete suggestions from the server");
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
        } catch (e) {
            alert("There was an error adding game to the server")
        }
    }


  render() {
      let locations: [string,string][] = [["A", "a"], ["B","b"],["C", 'c']]
    return (
        <div className="App">
            <header>Pretend this is a nice logo/header :)</header>
                <label>
                    Add a new game to the watch list:
                    <GameSelector suggestions={this.state.suggestions} onUpdateSearchTerm={this.getSuggestion} onUpdateGame={this.addGame}/>
                </label>
                <br/>
                <GameCard dummy={"dummy"}/>
        </div>
    );
  }
}

export default App;
