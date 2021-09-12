# Running the code

First Run

### `npm install`

in the base directory to install all the node_modules. Then open VS Code and run it in debug mode after configuring launch.json for Flask and then choosing flask app directory as api/app.py.\
Then run

### `npm start`

To launch the server in development mode.

To add the data in the database, see the code in data.py and run it independently.\
But make sure that the Neo4j database is already running and set the password in data.py accordingly.\
It is advisable to run data.py in debug mode and let each of the functions run independently, so that if something fails each commit can be rolled back.
