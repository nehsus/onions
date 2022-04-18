## Opinions for everyone
#### For CS521 at the University of Illinois, Chicago

# Opinions
## _For Everyone!_

Opinions shows you the happiness/satisfaction index on scale of 1 - 10 for top 500 US universities based on their professors' rating. 
In addition to the universities, you can also find the individual professor rating for any of those universities.

Python with MongoDB for database and React for frontend

## Features
- Select a university from the dropdown
- See its happiness/satisfaction index
- Select a professor from that university
- See his/her rating
- Make your decision

## Tech

Opinions uses many open source technologies to show you what you asked for:

- [ReactJS] - HTML enhanced for web apps!
- [Python] - makes the magic happen
- [mongoDB] - NoSQL db to make our lives easier

And of course Opinions itself is open source for future research.

## Installation

Opinions requires [React.js](https://reactjs.org/) v10+ to run.

Install the dependencies and devDependencies and start the server.

```sh
cd dillinger
npm i
node app
```

For production environments...

```sh
npm install --production
NODE_ENV=production node app
```

## Development

Want to contribute? Great!

Dillinger uses Gulp + Webpack for fast developing.
Make a change in your file and instantaneously see your updates!

Open your favorite Terminal and run these commands.

First Tab:

```sh
node app
```

Second Tab:

```sh
gulp watch
```

(optional) Third:

```sh
karma test
```

#### Building for source

For production release:

```sh
gulp build --prod
```

Generating pre-built zip archives for distribution:

```sh
gulp build dist --prod
```
