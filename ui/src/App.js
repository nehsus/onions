import logo from './logo.svg';
import './App.css';
import Autocomplete from './Complete'
import AutoComplete from './Completee'

import React, { Component, Suspense, Loading } from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';
const { faker } = require('@faker-js/faker');

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);



class App extends Component {

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
    

     const options = {
      responsive: true,
      plugins: {
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: 'Chart.js Bar Chart',
        },
      },
    };
    
    const labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July'];
    
     const data = {
      labels,
      datasets: [
        {
          label: 'Dataset 1',
          data: labels.map(() => faker.datatype.number({ min: 0, max: 1000 })),
          backgroundColor: 'rgba(255, 99, 132, 0.5)',
        },
        {
          label: 'Dataset 2',
          data: labels.map(() => faker.datatype.number({ min: 0, max: 1000 })),
          backgroundColor: 'rgba(53, 162, 235, 0.5)',
        },
      ],
    };

    // const options = {
		// 	animationEnabled: true,
		// 	theme: "light2",
		// 	title:{
		// 		text: "Opinions for everyone!"
		// 	},
		// 	axisX: {
		// 		title: "Frameworks",
		// 		reversed: false,
		// 	},
		// 	axisY: {
		// 		title: "Score (<=5.0)",
		// 		includeZero: true,
		// 		labelFormatter: this.addSymbols
		// 	},
		// 	data: [{
		// 		type: "bar",
		// 		dataPoints: [
		// 			{ y:  1, label: "Opinion" },
		// 			{ y:  2, label: "Flair" },
		// 			{ y:  3, label: "RateMyProfessor" },
		// 		]
		// 	}]
		// }

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
          <Bar options={options} data={data} />;
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

    const options = {
      title: {
        text: "Basic Column Chart in React"
      },
      data: [{				
                type: "column",
                dataPoints: [
                    { label: "Apple",  y: 10  },
                    { label: "Orange", y: 15  },
                    { label: "Banana", y: 25  },
                    { label: "Mango",  y: 30  },
                    { label: "Grape",  y: 28  }
                ]
       }]
   };

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

export default App;
