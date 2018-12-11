var geoSelect = $('#geography-select, #geography-select-home');

function resultTemplate(info) {
    return '<p class="result-name"><span class="result-type">' + info.geo_level + '</span>' + info.name + '</p>';
}

var textMatchEngine = new Bloodhound({
    datumTokenizer: function(d) {
        return Bloodhound.tokenizers.whitespace(d.name);
    },
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    limit: 300,
    prefetch: {
        url: '/api/municipalities',
        cache: false,
    },
});
textMatchEngine.initialize();

function makeGeoSelectWidget(element, selected) {
    element.typeahead({
        autoselect: true,
        highlight: false,
        hint: false,
        minLength: 2
    }, {
        // get textual matches from host
        name: 'textmatch',
        displayKey: 'name',
        source: textMatchEngine.ttAdapter(),
        limit: 20,
        templates: {
            suggestion: resultTemplate,
        },
    });

    element.on('typeahead:selected', selected || function(event, datum) {
        event.stopPropagation();
        window.location = datum.url;
    });
}

makeGeoSelectWidget(geoSelect);
