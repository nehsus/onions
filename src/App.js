import React, { Suspense, Loading, Component } from 'react';
import './App.css';
import Autocomplete from './Complete'
import AutoComplete from './Completee'


export default class App extends Component {

  constructor(props) {
    super(props)

    this.state = {
      s1data: [],
      s2data: [],
      s3data: [],
      s1: true,
      s2: false,
      s3: false,
      c1: 0,
      c2: 0,
      c3: 0, 
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

        fetch('/api/get/scores/'+item.pid).then(res => res.json().then(
          data => {
            console.log(data.data)
            this.setState({
              c1: data.data.vader,
              c2: data.data.flair,
              c3: data.data.rmp,
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

  getRandomInt(max) {
    return Math.floor(Math.random() * max);
  }

  loadComponents() {
    const {s1data, s1, s2, s2data, s3, s3data, s3obj, c1, c2, c3} = this.state


    console.log(s1data.length)
    return (

        <div className="component-area">
          {s1 && <div>
            <h1>Search for University</h1>
            <Autocomplete suggestions={s1data} onClicked={(name, item) => this.hideComponent(name, item)}/>
          </div>}

          {s2&& <div>
            <h1>Search for Professor</h1>
            <AutoComplete suggestions={s2data} onClicked={(name, item) => this.hideComponent(name, item)} />
          </div>}
          
          {s3&& <div className="a-area">
              <div className="score-area">
         <div className="chart-area">

        </div>      
			
              </div>
              
              <div className="comments-area">
              <h4>Top Comments</h4>
                <ul>{s3data !== [] && s3data.map(item => {
                    return (
                <li key = {this.getRandomInt(9999999)}> {item} </li>
                  )
                })}
                </ul>
              </div>
        
          </div>}
                 
        </div>
     
    )
  };

  render() {
    return (
      <div className="App">
        <header className="App-header">
        
        <div className="main-area">
          <Suspense fallback={<Loading />}>
            {this.loadComponents()}
          </Suspense>
          
        </div>
  
        </header>

        

      </div>
    );
  }
  
}
