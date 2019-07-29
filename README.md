# Girder GeoBrowser

## Requirements
* The Girder [Geospatial](https://github.com/OpenGeoscience/girder_geospatial) Plugin

## Plugin Installation
```
pip install girder-geobrowser
```

## Custom Python Commands
`setup.py` includes 2 custom commands:

* `build_ui`: This command builds the frontend from the `gui` folder, and places the build into `geobrowser_plugin/external_web_client`.
* `clean_build`: This command cleans the project of the files generated by the previous command.

**WARNING**

The standalone frontend will be served at `/geobrowser` if the built front-end path exists (i.e. `python setup.py build_ui` has been run), or if the mode is not `development`. So, if running `girder serve` in `development` mode, you should see no errors if the frontend is not built. However, if running `girder serve` in `production` mode, it will attempt to serve the files, regardless of if they've been built or not, throwing an error through cherrypy if they don't exist.

## Custom Girder CLI Commands
This plugin adds custom Girder CLI commands:

### `extract-geospatial`
This command manually runs the [Geospatial](https://github.com/OpenGeoscience/girder_geospatial) plugin on any Girder paths specified (defaults to '/'). To specify one or more path, use the `-p` argument. For example, to run this command on the collections `collection1` and `collection2`, you would run:
```
girder extract-geospatial -p collection/collection1 -p collection/collection2
```

### `populate-collection-meta`
This command populates the specified collection(s) with the provided metadata. The provided metadata must be in JSON format. The rules for setting metadata follow that of the [setMetadata](https://girder.readthedocs.io/en/stable/api-docs.html?highlight=setMetadata#girder.models.folder.Folder.setMetadata) function. This script requires that you specify 1 metadata JSON file and one or more collection IDs. For example, to populate the meta field of collections `5d3201b4dbdd758d55819007` and `5d3201c54731b3d3a1350823`, with the file `metadata.json`, you would run:
```
girder populate-collection-meta -i 5d3201b4dbdd758d55819007 -i 5d3201c54731b3d3a1350823 -d metadata.json
```
To use a Girder path instead of a collection ID, use the -p/--path option (also works with multiple):
```
girder populate-collection-meta -p /collection/foo -d metadata.json
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
