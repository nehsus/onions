import logo from './logo.svg';
import './App.css';
import Autocomplete from './Complete'
import AutoComplete from './Completee'

import React, { Component, Suspense, Loading } from "react";
import ReactSearchBox from "react-search-box";


class App extends Component {

  constructor(props) {
    super(props)

    this.state = {
      s1data: [],
      s2data: [],
      s3data: [],
      s1: true,
      s2: false,
      s3: false
    }

    this.hideComponent = this.hideComponent.bind(this);
  }

  hideComponent(name, item) {
    console.log("Getting professor from uni: "+item)
    switch (name) {
      case "s1":
        this.setState({ 
          s1: !this.state.s1,
          s2: !this.state.s2 
        });
        fetch('/api/get/professors/'+item).then(res => res.json().then(
          data => {
            console.log(data.data)
            this.setState({
            s2data: data.data
            }); //() => {  console.log(this.state.s1data);});
          }
          
        ));
        break;
      case "s2":
        this.setState({ 
          s2: !this.state.s2,
          s3: !this.state.s3,
         });
        fetch('/api/get/comments/'+item.pid).then(res => res.json().then(
          data => {
            console.log(data.data)
            this.setState({
            s3obj: item,
            s3data: data.data
            }); //() => {  console.log(this.state.s1data);});
          }
        ));
          
        break;
      default:
        break;
    };
  };

  componentDidMount() {
    const requestOptions = {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    };

    console.log("getting data")
    fetch('/api/get/universities/all', requestOptions).then(res => res.json().then(
      data => {
        console.log(data.data)
        this.setState({
        s1data: data.data
        }); //() => {  console.log(this.state.s1data);});
      }
      
    ));
      
    
    
    // this.setState({items: data});
   
  }

  loadComponents() {
    const {s1data, s1, s2, s2data} = this.state
    console.log(s1data.length)
    return (
      
        <div className="main-area">
          {s1 && <div>
            <h1>Search for University</h1>
            <Autocomplete suggestions={s1data} onClicked={(name, item) => this.hideComponent(name, item)}/>
          </div>}

          {s2&& <div>
            <h1>Search for Professor</h1>
            <AutoComplete suggestions={s2data} onClicked={(name, item) => this.hideComponent(name, item)} />
          </div>}
                 
        </div>
     
    )
  };

  render() {
    return (
      <div className="App">
        <header className="App-header">
          
          
          <div className="search-area">
          <Suspense fallback={<Loading />}>
            {this.loadComponents()}
          </Suspense>
            
          </div>
          
  
        </header>
      </div>
    );
  }
  
}

export default App;
