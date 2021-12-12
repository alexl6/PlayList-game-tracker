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

interface CardProps{
    game: GameObj;
}

class Card extends Component<CardProps, {}>{

    render() {
        console.log(this.props.game);
        let devs: string = this.props.game.developer.length == 0 ? "N/A" : this.props.game.developer.join(",");
        let publishers: string = this.props.game.publisher.length == 0 ? "N/A" : this.props.game.publisher.join(",");
        let series = [];
        if (this.props.game.series != ""){
            series.push(<div className={"company-name"}> <b>Game series:</b>&#9; {this.props.game.series} </div>);
        }

        // Since data might not be available for all properties on the right side,
        // we dynamically build the page
        let rightSideOptional = [];
        if (this.props.game.opencritic != -1){
            const styles = {
                width: this.props.game.opencritic+'%',
                backgroundColor: this.props.game.opencritic < 80 ?  "#F9D291" : "#9DCC89"
            }
            rightSideOptional.push(
                <div>
                    <div className={"right-side"}> <b>OpenCritic (Top critic score):</b></div>
                    <div className="bar-container">
                        <div className="bar" style={styles}> <b>{this.props.game.opencritic} </b></div>
                    </div>
                </div>);
        }

        if (this.props.game.timeToBeat != -1){

        }

        return (
            <div className={"flex-card"}>
                <div className={"card-left"}>
                    <h1 className={"gameTitle"}>{this.props.game.name}</h1>
                    <img className="coverArt" src={this.props.game.coverArt} alt={this.props.game.name}/>
                    <div className={"company-name"}> <b>Developer:</b>&#9; {devs} </div>
                    <div className={"company-name"}> <b>Publisher: </b>&#9; {publishers} </div>
                    {series}
                </div>
                <div className={"card-right"}>
                    <h1> hi </h1>
                    {rightSideOptional}
                </div>
            </div>
        );
    }
}

export default Card;