highlightOptions = [];


function customInputHandler(){

}


function generateOptions(){
    fetch('/get_features', { method: "POST" }).then(response => response.text().then(json_response => {
        response = JSON.parse(json_response);
        for (const [colorClass, words] of Object.entries(response)) {
            highlightOptions.push({
                highlight: RegExp(`\\b(${words.join('|')})\\b`, "gm"),
                className: colorClass
            })
        }
    }));
}

function getScores(inputText) {
    fetch('/get_scores', { method: "POST", body: inputText }).then(response => response.text().then(json_response => {
        response = JSON.parse(json_response);
        $('#raw-score').text(response['raw_score'])
        $('#recommended-score').text(response['recommended_score'])
        updateScoreColor()
    }));
}

function updateScoreColor() {
    recommendedScoreSpan = $('#recommended-score')
    let rScore = parseInt(recommendedScoreSpan.text())
    recommendedScoreSpan.removeClass('red light-red light-green green')
    switch (rScore) {
        case -2:
            recommendedScoreSpan.addClass('red')
            break;
        case -1:
            recommendedScoreSpan.addClass('light-red')
            break;
        case 1:
            recommendedScoreSpan.addClass('light-green')
            break;
        case 2:
            recommendedScoreSpan.addClass('green')
            break;
    }
}

$(document).ready(function () {
    // Configure textarea highlights
    generateOptions();
    console.log(highlightOptions)
    $('#input-area').highlightWithinTextarea({
        highlight: highlightOptions
    });
    $('#input-area').focus()
    // Update score display whenever input area text changes
    $('#input-area').bind('input propertychange', function () {
        getScores(this.value);
    });
});