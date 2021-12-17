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
        public prices: any,
        public platforms: string [],
        public timeToBeat: number,
        public urls: any,
        public coverArt: string,
        public opencritic: number,){}
}

interface CardProps{
    game: GameObj;
}

class Card extends Component<CardProps, {}>{

    render() {
                // Combine data into string for output
        let devs: string = this.props.game.developer.length === 0 ? "N/A" : this.props.game.developer.join(", ");
        let publishers: string = this.props.game.publisher.length === 0 ? "N/A" : this.props.game.publisher.join(", ");
        let genres: string = this.props.game.genre.length === 0 ? "N/A" : this.props.game.genre.join(", ")
        // Display the game series if available
        let series;
        if (this.props.game.series !== ""){
            series = (<div className={"left-desc"}> <b>Game series:</b>&#9; <a href={this.props.game.urls['series']}>{this.props.game.series}</a></div>);
        }

        // The data for some fields on the right may not be available
        // Skip those fields if the data is unavailable
        let rightSideOptional = [];

        // Show price data
        if(this.props.game.prices !== null && this.props.game.prices.current_low != null){
            let relative_price = 100-this.props.game.prices.percent_off;
            const styles = {
                width: relative_price +'%',
                backgroundColor: "#F9D291"
            }
            rightSideOptional.push(
                <div>
                    <div className={"right-side-desc"}> <b>Current best price:</b></div>
                    <div className={"large-num"}> ${this.props.game.prices.current_low}</div>
                    {this.props.game.prices.percent_off}% off at {this.props.game.prices.current_low_stores.join(", ")}
                    <div className="price-bar-right">
                        <div className="price-bar-left" style={styles}> Current: ${this.props.game.prices.current_low}</div>
                    </div>
                    <div className="price-bar-labels-container">
                        <div className={"price-bar-label"} style = {{textAlign: "left"}}> Historical low: ${this.props.game.prices.lowest} </div>
                        <div className={"price-bar-label"} style = {{textAlign: "right"}}> Regular: ${this.props.game.prices.normal} </div>
                    </div>
                    <div className={"right-link"}> <a href={this.props.game.urls['ITAD']}>IsThereAnyDeal ↗</a></div>
                </div>
            );
        }
        // Display the playtime data
        if (this.props.game.timeToBeat === 0){
            rightSideOptional.push(
              <div>
                  <div className={"right-side-desc"}> <b>How long it takes to beat the game (Avg):</b></div>
                  <div className={"missing-playtime"}><a href={this.props.game.urls['HLTB']}> Available on HowLongToBeat ↗</a></div>
                </div>);
        } else if (this.props.game.timeToBeat !== -1){
            rightSideOptional.push(
              <div>
                  <div className={"right-side-desc"}> <b>How long it takes to beat the game (Avg):</b></div>
                  <div className={"large-num"}> {this.props.game.timeToBeat} hrs </div>
                  <div className={"right-link"}> <a href={this.props.game.urls['HLTB']}>HowLongToBeat ↗</a></div>
                </div>);
        } 
        // Color code the bar representing OpenCritic score
        if (this.props.game.opencritic !== -1){
            const styles = {
                width: this.props.game.opencritic+'%',
                backgroundColor: this.props.game.opencritic < 80 ?  "#F9D291" : "#9DCC89"
            }
            rightSideOptional.push(
                <div>
                    <div className={"right-side-desc"}> <b>OpenCritic (Top critic score):</b></div>
                    <div className="bar-container">
                        <div className="bar" style={styles}> <b>{this.props.game.opencritic} </b></div>
                    </div>
                    <div className='right-link'><a href={this.props.game.urls['OpenCritic']}>OpenCritic ↗</a></div>
                </div>);
        }


        if (this.props.game.platforms.length > 0){
            rightSideOptional.push(
              <div>
                  <div className={"right-side-desc"}> <b>Available on:</b></div>
                  <div className={"platform-container"}> {this.props.game.platforms.join(", ")} </div>
              </div>);
        }

        if (this.props.game.series !== ""){
            let seriesGamesList: any[] = [];
            for(let game of this.props.game.seriesGames){
                seriesGamesList.push(
                    <div>
                        {game}
                    </div>
                )
            }
            rightSideOptional.push(
                <div>
                  <div className={"right-side-desc"}> <b>Other games in this series:</b></div>
                  <div className={"series-games-container"}> {seriesGamesList} </div>
              </div>);
        }

        return (
            <div className={"flex-card"}>
                <div className={"card-left"}>
                    <h1 className={"gameTitle"}>{this.props.game.name}</h1>
                    <img className="coverArt" src={this.props.game.coverArt} alt={this.props.game.name}/>
                    <div className={"left-desc"}> <b>Developer:</b>&#9; {devs} </div>
                    <div className={"left-desc"}> <b>Publisher: </b>&#9; {publishers} </div>
                    <div className={"left-desc"}> <b>Genres: </b>&#9; {genres} </div>
                    {series}
                    <br/>
                    <div className={"right-link"}><a href={this.props.game.urls['IGDB']}>More info on IGDB ↗</a></div>
                </div>
                <div className={"card-right"}>
                    {rightSideOptional}
                </div>
            </div>
        );
    }
}

export default Card;