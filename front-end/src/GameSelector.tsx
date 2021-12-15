import React, {Component} from 'react';
import "./GameSelector.css";

interface GameSelectorProps {
    suggestions: string[],            // Array of possible locations
    onUpdateSearchTerm(keyword : string): void,
    onUpdateGame(gameName: string): void,
    onClearSearch():void,
    onClearGames(): void
}

interface GameSelectorState{
    searchBox: string,
    // prevSearchSuggest: number,   // The last time an search suggestion request was sent to server
    timeout: any
}

/**
 * GameSelector is a dropdown menu with a search bar that allows users to quickly
 * select a location from a given list
 */
class GameSelector extends Component<GameSelectorProps, GameSelectorState> {
    constructor(props: GameSelectorProps) {
        super(props);
        this.state = {
            searchBox: "",
            // prevSearchSuggest: new Date().getTime(),
            timeout: 0,
        }
        this.clearSearchBox = this.clearSearchBox.bind(this);
        this.clearAllGames = this.clearAllGames.bind(this);
    }

    /**
     * Clear & collapse the search box
     */
    clearSearchBox(){
        this.setState({
            searchBox: "",
            timeout:0
        });
        this.props.onClearSearch();
    }

    /**
     * Clear all games
     */
         clearAllGames(){
            this.setState({
                searchBox: "",
                timeout: 0
            });
            this.props.onClearGames();
        }

    /**
     * Handle user clicking on a game in the list of suggestions in the dropdown menu
     * @param e Index of the selected element in the list of suggested games
     *        matching user's search query
     */
    onGameSelect(e: number){
        this.setState({
            searchBox: "",
            timeout: 0
        })
        this.props.onUpdateGame(this.props.suggestions[e]);
    }

    /**
     * Handle user input in the search bar. Calls server for search suggestion at reduced rate
      */
    onUserTyped = (event: React.ChangeEvent<HTMLInputElement>) =>{
        this.setState({
            searchBox: event.target.value
        });
        // let currTime = new Date().getTime()
        // if(currTime - this.state.prevSearchSuggest > 100){
        //     this.setState({
        //         prevSearchSuggest: currTime
        //     })
        //     this.props.onUpdateSearchTerm(event.target.value);
        // }

        if(this.state.timeout) clearTimeout(this.state.timeout);
        this.setState({
            timeout: setTimeout(() => {
                this.props.onUpdateSearchTerm(event.target.value)}, 200)
            });
    }


    render() {
        // Construct add game dropdown menu if the button is pressed
        let dropdownItems : any[] = [];
        // Trivial loop: Loops through every game in this.props.suggestions
        for(let i=0; i<this.props.suggestions.length; i++){
            dropdownItems.push(
                <button key={i} value={i} onClick={() => this.onGameSelect(i)}>
                    {this.props.suggestions[i]}
                </button>
            );
        }
        // Add search box and wrap the dropdown menu items in a container
        return (
            <div>
                <div className={"dropdownContainer"}>
                    <div id={"searchDropdownContent"}>
                        <input value={this.state.searchBox} placeholder="Enter the name of a game" onChange={this.onUserTyped}/>
                        {dropdownItems}
                    </div>
                </div>
                <button onClick={this.clearSearchBox} className={"clearBtn"}> Clear search
                </button>
                <button onClick={this.clearAllGames} className={"clearBtn"}> Clear all games
                </button>
            </div>
        )
    }
}

export default GameSelector;
