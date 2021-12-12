import React, {Component} from 'react';
import "./GameCard.css"
import Card from "./Card";

class GameObj {
    constructor(
        public name: string,
        public genre: string[],
        public developer: string[],
        public publisher: string[],
        public series: string,
        public seriesGames: string[],
        public related: string[],
        public prices: any,
        public platforms: string [],
        public timeToBeat: number,
        public url: string,
        public coverArt: string,
        public opencritic: number,){}
}

interface GameCardsProps{
    games: GameObj[];
}

class GameCards extends Component<GameCardsProps, { }>{

    render() {
        let gamecards:  any[] = [];
        // Add game cards in pairs (so they collapse into a column of entries when the window gets small)
        // Generate cards independently to increase code reuse
        console.log(this.props.games.length);
        if (this.props.games.length >=2) {
            for (let i = 0; i < this.props.games.length-1; i += 2) {
                gamecards.push(
                    <div className={"flex-container"}>
                        <Card game={this.props.games[i]}/>
                        <Card game={this.props.games[i + 1]}/>
                    </div>);
            }
        }
        // Manually add the last game if there are odd number of games
        if (gamecards.length * 2 < this.props.games.length){
            console.log(this.props.games.length - gamecards.length * 2);
            console.log(this.props.games[this.props.games.length-1]);
            gamecards.push(
                <div className={"flex-container"} id={"single-card"}>
                    <Card game={this.props.games[this.props.games.length-1]}/>
                </div>);
        }

        // Render
        return (
            <div>
                {gamecards}
            </div>
        );
    }
}

export default GameCards;