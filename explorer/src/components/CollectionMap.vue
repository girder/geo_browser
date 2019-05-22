<template>
  <v-card>
    <div />
  </v-card>
</template>

<script>
import Map from 'ol/Map';
import View from 'ol/View';
import { Tile as TileLayer, Vector as VectorLayer } from 'ol/layer';
import GeoJSON from 'ol/format/GeoJSON';
import { OSM } from 'ol/source';
import VectorSource from 'ol/source/Vector';
import Text from 'ol/style/Text';
import { Style, Fill } from 'ol/style';
import Stroke from 'ol/style/Stroke';
import { Select, MouseWheelZoom, DragPan } from 'ol/interaction';
import { click } from 'ol/events/condition';
import { capitalize } from 'lodash';
import Cities from '@/assets/cities.json';
import { mapGetters } from 'vuex';


export default {
  name: 'CollectionMap',
  static() {
    return {
      ol: {},
    };
  },
  computed: {
    ...mapGetters([
      'user',
    ]),
  },
  inject: ['girderRest'],
  watch: {
    user() {
      this.loadFeaturesRemote();
    },
  },
  mounted() {
    this.createMap();
    this.loadFeaturesRemote();
  },
  methods: {
    featureStyle(feature) {
      return new Style({
        stroke: new Stroke({
          color: 'blue',
          width: 1,
        }),
        fill: new Fill({
          color: 'rgba(0, 0, 255, 0.1)',
        }),
        text: new Text({
          text: feature.get('name').split('_').map(x => capitalize(x)).join(', '),
          fill: new Fill({
            color: 'rgb(255, 255, 255)',
          }),
          backgroundFill: new Fill({
            color: 'rgb(0, 0, 0)',
          }),
          scale: 1,
        }),
      });
    },
    createMap() {
      this.ol.vectorSource = new VectorSource();
      this.ol.map = new Map({
        layers: [
          new TileLayer({
            source: new OSM(),
          }),
          new VectorLayer({
            source: this.ol.vectorSource,
            style: this.featureStyle,
          }),
        ],
        target: this.$el,
        view: new View({
          center: [0, 0],
          zoom: 2.5,
        }),
        interactions: [
          new Select({
            condition: click,
          }),
          new MouseWheelZoom(),
          new DragPan(),
        ],
      });
    },
    loadFeaturesLocal() {
      this.ol.features = new GeoJSON({
        featureProjection: 'EPSG:3857',
      }).readFeatures(Cities);

      this.ol.vectorSource.clear();
      this.ol.vectorSource.addFeatures(this.ol.features);
    },
    async loadFeaturesRemote() {
      console.log('LOAD');
      const collectionFeatures = (await this.girderRest.get(
        'collection/geobrowser',
        { params: {} },
      )).data.map(x => ({
        type: 'Feature',
        properties: {
          name: x.name,
        },
        geometry: x.geometa_bounds,
      }));

      this.ol.features = new GeoJSON({
        featureProjection: 'EPSG:3857',
      }).readFeatures({
        type: 'FeatureCollection',
        features: collectionFeatures,
      });

      this.ol.vectorSource.clear();
      this.ol.vectorSource.addFeatures(this.ol.features);
    },
  },
};
</script>
