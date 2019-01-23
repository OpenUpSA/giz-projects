/*
 * A class that loads geography boundary information from
 * mapit.code4sa.org.
 */
var MAPIT = {
  level_codes: {
    ward: 'WD',
    municipality: 'MN',
    district: 'DC',
    province: 'PR',
    country: 'CY',
  },
  level_simplify: {
    DC: 0.01,
    PR: 0.005,
    MN: 0.005,
    WD: 0.0001,
  },
};

function ProjectLoader() {
  var self = this;
  self.url = '/api/projects';

  this.loadProjects = function(success) {
      return jQuery.get(this.url, function(js) {
          var projects = js;
          success(projects);
      })
  }
}

function MapItGeometryLoader() {
  var self = this;
  self.mapit_url = 'https://mapit.code4sa.org';

  this.decorateFeature = function(feature) {
    feature.properties.level = feature.properties.type_name.toLowerCase();
    feature.properties.code = feature.properties.codes.MDB;
    feature.properties.geoid = feature.properties.level + '-' + feature.properties.code;
  };

  this.loadGeometryForLevel = function(level, success) {
    var url = '/areas/' + MAPIT.level_codes[level] + '.geojson?generation=2';
    var simplify = MAPIT.level_simplify[MAPIT.level_codes[level]];
    if (simplify) {
      url = url + '&simplify_tolerance=' + simplify;
    }

    return jQuery.get(this.mapit_url + url, function(geojson) {
      var features = _.values(geojson.features);
      _.each(features, self.decorateFeature);
      success({features: features});
    });
  };

  this.loadGeometryForGeo = function(geo_level, geo_code, generation, success) {
    var mapit_type = MAPIT.level_codes[geo_level];
    var mapit_simplify = MAPIT.level_simplify[mapit_type];
    var url = "/area/MDB:" + geo_code + "/feature.geojson?generation=" + generation + "&simplify_tolerance=" + mapit_simplify +
      "&type=" + mapit_type;

    return jQuery.get(this.mapit_url + url, function(feature) {
      self.decorateFeature(feature);
      success(feature);
    });
  };
}
GeometryLoader = new MapItGeometryLoader();


var Maps = function() {
  var self = this;
  this.mapit_url = GeometryLoader.mapit_url;

  this.featureGeoStyle = {
    "fillColor": "#66c2a5",
    "color": "#777",
    "weight": 2,
    "opacity": 0.3,
    "fillOpacity": 0.5,
    "clickable": false
  };

  this.layerStyle = {
    "clickable": true,
    "color": "#00d",
    "fillColor": "#ccc",
    "weight": 1.0,
    "opacity": 0.3,
    "fillOpacity": 0.3,
  };

  this.projectStyle = {
    "clickable": true,
    "color": "red",
    "fillColor": "red",
    "weight": 1.0,
    "opacity": 0.3,
    "fillOpacity": 0.3,
  };

  this.hoverStyle = {
    "fillColor": "#66c2a5",
    "fillOpacity": 0.7,
  };

  this.drawMapsForProfile = function(geo) {
    this.geo = geo;
    this.createMap();
    this.addImagery();

    // for 2011 munis, we load generation 1 maps, otherwise we load 2016 (generation 2) maps
    var generation = 2;

    // draw this geometry
    GeometryLoader.loadGeometryForGeo(this.geo.geo_level, this.geo.geo_code, generation, function(feature) {
      self.drawFocusFeature(feature);
    });

    this.drawMunicipalities()
      .done(function() {
          self.addLegend();
      });
  };

  this.drawMapForHomepage = function(centre, zoom) {
    // draw a homepage map, but only for big displays
    if (browserWidth < 768 || $('#slippy-map').length === 0) return;

    this.createMap();
    this.addImagery();

    if (centre) {
      self.map.setView(centre, zoom);
    }

    this.drawMunicipalities()
      .done(function() {
          self.addLegend();
      });
  };

  this.addLegend = function() {
      var legend = L.control({position: 'bottomright'});

      legend.onAdd = function (map) {
        var div = L.DomUtil.create('div', 'info legend');
        div.innerHTML += 'Municipalities with projects <i style="background:' + 'red' + '"></i>';
        return div
      }

      legend.addTo(self.map);
  }

  this.createMap = function() {
    var allowMapDrag = (browserWidth > 480) ? true : false;

    this.map = L.map('slippy-map', {
      scrollWheelZoom: false,
      zoomControl: false,
      doubleClickZoom: false,
      boxZoom: false,
      keyboard: false,
      dragging: allowMapDrag,
      touchZoom: allowMapDrag
    });

    if (allowMapDrag) {
      this.map.addControl(new L.Control.Zoom({
        position: 'topright'
      }));
    }
  };

  this.addImagery = function() {
    // add imagery
    L.tileLayer('//{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
      subdomains: 'abc',
      maxZoom: 17
    }).addTo(this.map);
  };

  this.drawMunicipalities = function() {
    var geo_code = this.geo ? this.geo.geo_code : null;

    // draw all local munis
    return GeometryLoader.loadGeometryForLevel('municipality', function(data) {
      // don't include this smaller geo, we already have a shape for that
      data.features = _.filter(data.features, function(f) {
        return f.properties.codes.MDB != geo_code;
      })
      self.data = data;
    })
    .done(function() {
        var projectLoader = new ProjectLoader();
        return projectLoader.loadProjects(function(projects) {
            var munis = _.map(projects, function(el) {
                return el.geo_code;
            });

            self.uniq_munis = _.uniq(munis, false);
        })
        .done(function() {
           self.drawFeatures(self.data);
        })
    })
  };

  this.drawFocusFeature = function(feature) {
    var layer = L.geoJson([feature], {
      style: self.featureGeoStyle,
    });
    this.map.addLayer(layer);
    this.map.fitBounds(layer.getBounds());
    if (browserWidth > 768) {
      this.map.panBy([-270, 0], {animate: false});
    }
  };

  this.drawFeatures = function(features) {
    var setMuniStyle = function(layer, properties) {
        if (_.contains(self.uniq_munis, properties.code)) {
            layer.setStyle(self.projectStyle);
        } else {
            layer.setStyle(self.layerStyle)
        }
    }
    // draw all others
    return L.geoJson(features, {
      style: this.layerStyle,
      onEachFeature: function(feature, layer) {
        setMuniStyle(layer, feature.properties);

        layer
          .bindLabel(feature.properties.name, {direction: 'auto'})
          .on('mouseover', function() {
            layer.setStyle(self.hoverStyle);
          })
          .on('mouseout', function() {
            setMuniStyle(layer, feature.properties);
          })
          .on('click', function() {
            window.location = '/profiles/' + feature.properties.level + '-' + feature.properties.code + '/';
          });
      },
    }).addTo(this.map);
  };
};
