# Girder GeoBrowser

## Requirements
* The Girder [Geospatial](https://github.com/OpenGeoscience/girder_geospatial) Plugin

## Plugin Installation
```
pip install .
```


## Standalone Frontend Setup

### Install Yarn
```
npm install -g yarn
```

### Install Frontend packages
```
cd gui
yarn install
```

### Compiles and hot-reloads for development
```
yarn run serve
```

### Compiles and minifies for production
```
yarn run build
```

If you've cloned the repo and are developing for the plugin, there is a custom command in `setup.py` that will automate installing yarn packages, building the frontend for production, and copying the dist folder to the proper location. To use this, run: `python setup.py build_ui`. To clean the directory of the files generated from running this command, run `python setup.py clean_build`

**WARNING**

If you run `girder serve` in development mode, the standalone frontend will not be served at `/geobrowser`. This is because it is expected that the frontend will be served on its own (E.g. `yarn run serve`) in order to see the changes being made. If for some reason you need to serve the frontend at `/geobrowser`, you will need to run girder serve in production mode. However be aware that in this case it is serving the pre-built files, and thus no changes will take affect until you rebuild the frontend (E.g. by running `python setup.py build_ui`).

### Run your tests
```
yarn run test
```

### Lints and fixes files
```
yarn run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).
