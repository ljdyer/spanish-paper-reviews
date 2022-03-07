var FONT_MIN = 10;
var FONT_MAX = 80;


function updateProba(inputText) {

    fetch('/get_proba', { method: "POST", body: inputText }).then(response => response.text().then(json_response => {
        response = JSON.parse(json_response);
        $('#raw-score').text(response['raw_score'])
        $('#rounded-score').text(response['rounded_score'])
    }));
}


$(document).ready(function () {
    // Update probability display whenever input area text changes
    $('#input-area').bind('input propertychange', function () {
        updateProba(this.value);
    });
});
