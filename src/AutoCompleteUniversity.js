import React, { Fragment, useState } from "react";

/**
 * Non-Component version of:
 * https://www.digitalocean.com/community/tutorials/react-react-autocomplete
 * @param {*} props 
 * @returns AutoCompleteUniversity
 */
const AutoCompleteUniversity = (props) => {

  const [activeSuggestion, updateActiveSuggestion] = useState(0);
  const [filteredSuggestion, updateFilteredSuggestion] = useState([]);
  const [showSuggestion, updateShowSuggestion] = useState(false);
  const [userInput, updateUserInput] = useState("");

  const onChange = (e) => {
    updateUserInput(e.currentTarget.value);
    const suggestion = props.suggestion;
    // Filter our suggestions that don't contain the user's input
    const filteredSuggestion = suggestion.filter(
      suggestion =>
        suggestion.title.toLowerCase().indexOf(userInput.toLowerCase()) > -1
    );
    
    updateActiveSuggestion(0);
    updateFilteredSuggestion(filteredSuggestion);
    updateShowSuggestion(true);
    updateUserInput(e.currentTarget.value);
  };

  const onClick = (item) => {
    updateActiveSuggestion(0);
    updateFilteredSuggestion();
    updateShowSuggestion(false);
    updateUserInput(item.title);
    props.onClicked("s1", item);
  };

    let suggestionsListComponent;

    if (showSuggestion && userInput) {
      if (filteredSuggestion.length) {
        suggestionsListComponent = (
          <ul class="suggestions">
            {filteredSuggestion.map((suggestion, index) => {
              let className;

              // Flag the active suggestion with a class
              if (index === activeSuggestion) {
                className = "suggestion-active";
              }

              return (
                <li className={className} key={suggestion.uid} onClick={()=>onClick(suggestion)}>
                  {suggestion.title}
                </li>
              );
            })}
          </ul>
        );
      } else {
        suggestionsListComponent = (
          <div class="no-suggestions">
            <em>no suggestions</em>
          </div>
        );
      }
    }

    return (
      <div className="suggestions-d">
        <Fragment>
        <input
          type="text"
          onChange={onChange}
          value={userInput}
        />
        {suggestionsListComponent}
      </Fragment>
      </div>
      
    );
}

export default AutoCompleteUniversity;
