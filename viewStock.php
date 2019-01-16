<html>
<body onresize="resizeCanvas()">
<title id="title">S&P 500 Stock Overview</title>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<link href="https://fonts.googleapis.com/css?family=Roboto" rel="stylesheet">
<div id="overview" onclick="window.location.href='table.php'">Back to Overview</div>
<h1 id="header"></h1>
<canvas id="canvas1" width= height=200></canvas>
<h3 id="desc">{Description Placeholder}</h3>
<h2 id="similarHeader">Similar Stocks</h2>
<table id="simTable">


</table>
</body>
</html>

<script>
var resolution = 50; 
var historical;
var ticker = getQueryVariable('ticker');
var similarities;

init();


function getFinalOutput () {
    $.ajax({
        type: "GET",
        url: "stockDescriptions.txt",
        dataType: "text",
        success: function(data) {processDesc(data);}
     });
}

function getSimilarities () {
    $.ajax({
        type: "GET",
        url: "sim/"+ticker+"_Sim.txt",
        dataType: "text",
        success: function(data) {processSim(data);}
     });
}

$(document).ready(function() {
    $.ajax({
        type: "GET",
        url: "finalStockHistorical.txt",
        dataType: "text",
        success: function(data) {processDataHist(data);}
     });
});

function processDataHist(allText) {
    var allTextLines = allText.split(/\r\n|\n/);
    var headers = allTextLines[0].split(',');
    var lines = [];

    for (var i=1; i<allTextLines.length; i++) {
        var data = allTextLines[i].split(',');
        if (data.length == headers.length) {

            var tarr = [];
            for (var j=0; j<headers.length; j++) {
                tarr.push(data[j]);
            }
            lines.push(tarr);
        }
    }
    historical = lines.filter(function(line) {
	       return line[0] == ticker;
    });
    resizeCanvas();
    getFinalOutput();
}

function processSim(allText) {
    var allTextLines = allText.split(/\r\n|\n/);
    var headers = allTextLines[0].split(',');
    var lines = [];

    for (var i=1; i<allTextLines.length; i++) {
        var data = allTextLines[i].split(',');
        if (data.length == headers.length) {

            var tarr = [];
            for (var j=0; j<headers.length; j++) {
                tarr.push(data[j]);
            }
            lines.push(tarr);
        }
    }
    lines.sort(function(a,b){
        return b[1] - a[1];
    });
    console.log(lines);
    similarities = lines;
    populateTable();
}

function processDesc(allText) {
    var allTextLines = allText.split(/\r\n|\n/);
    var headers = allTextLines[0].split(',');
    var lines = [];

    for (var i=1; i<allTextLines.length; i++) {
        var data = allTextLines[i].split(',');
            if (data[0] == ticker) {
                desc = allTextLines[i].slice(4);   
            }
        }
    desc = desc.replace(/"/g,"");
    console.log(desc);
    document.getElementById('desc').innerHTML = desc;
    
    getSimilarities();
}

function resizeCanvas () {
var c = document.getElementById("canvas1");
c.width = window.innerWidth*0.99;
c.height = window.innerWidth*0.3;
populateCanvas("canvas1", historical);
}

function init () {
    document.getElementById('title').innerHTML = "ASX:"+ticker+" Details";
    document.getElementById('header').innerHTML = "ASX:"+ticker;
}

function populateTable () {
    var htmlSTR = "<tr><th>Ticker</th><th>Similarity</th></tr>";
    
    for (var i = 0; i < similarities.length; i++) {
        onclickTxt = 'gotoPage("'+similarities[i][0]+'")';
        htmlSTR += "<tr onclick='"+onclickTxt+"'><td>"+similarities[i][0]+"</td><td>"+parseFloat(similarities[i][1]).toFixed(5)+"</td></tr>"
    }

    document.getElementById('simTable').innerHTML = htmlSTR;
}

function populateCanvas (canvasName, data) {

var c = document.getElementById(canvasName);
var ctx = c.getContext("2d");

var mapped = data.map(function(v) {
  return v[2];
})

var max = 1.05*Math.max.apply(Math, mapped);
var min = 0.95*Math.min.apply(Math, mapped);

data.sort(function(a,b){
    return a[1] - b[1];
});

ctx.strokeStyle = '#42f4b9';

for (var i = 0; i <= resolution; i++) {
    var val1 = data[(i-1).clamp(0, resolution)][2];
    var val2 = data[i][2];
    
    var x1 = (i-1).clamp(0, resolution)/50*c.width;
    var y1 = c.height - (((val1 - min)/(max - min)) * c.height);
    
    var x2 = i/50*c.width;
    var y2 = c.height - (((val2 - min)/(max - min)) * c.height);
    
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.stroke();
    ctx.closePath();   
    
}
}

String.prototype.replaceAll = function(search, replacement) {
    var target = this;
    return target.replace(new RegExp(search, 'g'), replacement);
};
function round(value, decimals) {
  return Number(Math.round(value+'e'+decimals)+'e-'+decimals);
}

Number.prototype.clamp = function(min, max) {
  return Math.min(Math.max(this, min), max);
};

function getQueryVariable(variable)
{
       var query = window.location.search.substring(1);
       var vars = query.split("&");
       for (var i=0;i<vars.length;i++) {
               var pair = vars[i].split("=");
               if(pair[0] == variable){return pair[1];}
       }
       return(false);
}

function gotoPage (str) {
window.location.href = "viewStock.php?ticker="+str;
}
</script>


<style>
body {
background-color: #202020;
font-family: 'Roboto', sans-serif;
color:white;
}
#header {
text-align: center;
position: absolute;
margin-left: auto;
margin-right: auto;
left: 0;
right: 0;
margin-top: 10px;
}
#canvas1 {
border-bottom: 1px solid #bbb;
padding-bottom:5px;
}
#desc {
text-align: center;
color: #f4f4f4;
font-weight: 100;
}
#similarHeader {
text-align: center;
margin-bottom: 10px;
}
#simTable {
margin: auto;
width: 20%;
}
th {
padding: 5px;
text-align: center;
background-color: #202035;
}
tr {
cursor: hand;
}
td {
text-align: center;
padding: 5px;
}
tr:nth-child(even) {background-color: #303030;}
tr:hover {
    background-color: #202035;
}
#overview {
    position: absolute;
    padding: 10px;
    background-color: #303030;
    z-index: 10;
    transition: background-color 0.5s;
}
#overview:hover {
    background-color: #202035;
}
</style>















