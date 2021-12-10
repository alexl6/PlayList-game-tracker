import React, {Component} from 'react';
import "./GameCard.css"

interface GameCardProps{
    dummy: string;
}

class GameCard extends Component<GameCardProps, { }>{
    constructor(props: GameCardProps) {
        super(props);
    }


    render() {
        return (
            <div className={"gameCard"}>
                <div className={"leftSideBar"}>
                    <img className="coverArt" src="https://images.igdb.com/igdb/image/upload/t_cover_big/co49x5.jpg" alt={"Carlie Anglemire"}/>
                    <h1 className={"gameTitle"}>Minecraft</h1>
                </div>

            </div>
        );
    }
}

export default GameCard;