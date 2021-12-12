import React, {Component} from 'react';
import "./GameCard.css"

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

interface GameCardProps{
    key: string;
    game: GameObj;
}

class GameCard extends Component<GameCardProps, { }>{

    render() {
        console.log(this.props.game)
        return (
            <div>
                <div className={"flex-container"}>
                    <div className={"flex-card"}>
                        <div className={"card-left"}>
                            <h1 className={"gameTitle"}>{this.props.game.name}</h1>
                            <img className="coverArt" src={this.props.game.coverArt} alt={this.props.game.name}/>

                        </div>
                        <div className={"card-top-right"}>
                            <h1> hi </h1>
                        </div>
                    </div>
                    <div className={"flex-card"}>
                        <h1 className={"gameTitle"}>Overcooked 2</h1>
                    </div>
                </div>
                <br/>
                <div className={"flex-container"}>
                    <div className={"flex-card"}>
                        <h1 className={"gameTitle"}>Minecraft</h1>
                    </div>
                </div>
            </div>
        );
    }
}

export default GameCard;