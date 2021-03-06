<html>
<body>
<title>S&P 500 Stock Overview</title>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<link href="https://fonts.googleapis.com/css?family=Roboto" rel="stylesheet">
<select style="float:right"><option>5 Days</option><option>1 Month</option><option>6 Months</option><option>1 Year</option><option>5 Years</option><option>All</option></select>
<table class="formTable"><tr>
<td><div class="inputDiv">Column: <select id="columnSelect"></select><br>Green/Red Colouring:<input type="checkbox" id="colouringCheckbox"><br>Show %:<input type="checkbox" id="percentCheckbox"><br><button class="colButton" onclick="addColumn()">Add Column</button></div></td>
<td><table id="canvasTable" style="float:right"><tr><td id="graphedContainer" style="overflow: auto;vertical-align:top; max-height:200px "></td><td><canvas id="focusCanvas" width="400" height="200" style="border: 1px solid white; float: right"></td></tr></canvas></table></td>
</tr></table>
<table id="table1" class="stockTable"></table>
</body>
</html>

<script>
// Name, Colouring, Percent
var propertiesArray = [["Ticker", false, false], ["Recent_Close_Value", false, false]];
var historical;
var graphsDisplayed = 50;
var graphedTickers = [];
var colours = ["#ff0000", "#00ff00", '#0000ff', '#ffffff', '#00ffff', '#ff00ff'];

populateFocusCanvas();

function getFinalOutput () {
    $.ajax({
        type: "GET",
        url: "finalOutput.txt",
        dataType: "text",
        success: function(data) {processData(data);}
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
    historical = lines;
    getFinalOutput();
    // alert(lines);
}

function processData(allText) {
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
    for (var m = 0; m < lines.length; m++) {
        stocks.push(new Stock(lines[m][0], lines[m][1], lines[m][2], lines[m][3], lines[m][4], lines[m][5]));
    }
    populateSelect();
    sortTable(stocks, "Ticker")
    // alert(lines);
}

var stocks = [];
var sortedArray = [];
var sortedCol = "";
var sortedAscending = false;

function Stock (Ticker, LstdDev, pChange10d, Gradient30, Gradient90, close) {
this.Ticker = Ticker;
this.Lifetime_Standard_Deviation = Number(LstdDev);
this.Percent_Change_Past_10_Days = Number(pChange10d);
this.x30_Day_Gradient = Number(Gradient30);
this.x90_Day_Gradient = Number(Gradient90);
this.Recent_Close_Value = Number(close);
this.Ben_Variable = Number(close);
}

function SortByCol (colNum) {
sortTable(stocks, propertiesArray[colNum][0]);
}

function addColumn () {
columnName = document.getElementById('columnSelect').value;
colouredText = document.getElementById('colouringCheckbox').checked;
percentText = document.getElementById('percentCheckbox').checked;
if (columnName != "") {
propertiesArray.push([columnName, colouredText, percentText]);
populateTable(stocks, "table1");
populateSelect();
}
}

function removeColumn (id) {
console.log(id);
propertiesArray.splice(id, 1);
populateTable(stocks, "table1");
populateSelect();
}

function populateSelect () {
    var properties = Object.getOwnPropertyNames(stocks[0]);
    var activeProperties = getActiveProperties();
    htmlStr = "";
    for (var i = 0; i < properties.length; i++) {
    if (!activeProperties.includes(properties[i])) {
        prettyString = properties[i].replaceAll("_", " ").replace("x", "");
        htmlStr += "<option value='"+properties[i]+"'>"+prettyString+"</option>"
    }
    }
    document.getElementById('columnSelect').innerHTML = htmlStr;
    if (document.getElementById('columnSelect').innerHTML == "") {
        document.getElementById('columnSelect').innerHTML = "<option value=''>No more columns</option>"; 
    }
}

function populateTable (objArray, tableID) {
if (objArray.length > 0) {
document.getElementById(tableID).innerHTML = "";
var properties = Object.getOwnPropertyNames(objArray[0]);
var containingText = "";
containingText += "<tr>";

for (var i = 0; i < propertiesArray.length; i++) {
var onclickText = "sortTable(stocks, "+propertiesArray[i][0].toString()+")";
var sortedRow = (propertiesArray[i][0] == sortedCol);
if (sortedRow) {
    var typeText = (sortedAscending) ? "Asc" : "Desc";
    containingText += '<th class="sorted'+typeText+' stockElementH" onclick="SortByCol('+i+')">'+propertiesArray[i][0].replaceAll("_", " ").replace("x", "")+' <img src="sort-'+typeText+'.png" width="20px" height="20px" style="vertical-align:top"><div class="deleteColumn" onclick="removeColumn('+i+')">X</div></th>';
} else {
    containingText += '<th onclick="SortByCol('+i+')" class="stockElementH">'+propertiesArray[i][0].replaceAll("_", " ").replace("x", "")+' <img src="sort-Desc.png" width="20px" height="20px" style="vertical-align:top; opacity:0"><div class="deleteColumn" onclick="removeColumn('+i+')">X</div></th>';
}
}

containingText += '<th class="stockElementH">Stock Graph</th>'

containingText += "</tr>";

for (var i = 0; i < objArray.length; i++) {
    onclickTxt = 'gotoPage("'+objArray[i]['Ticker']+'")';
    containingText += "<tr class='stockElementR' onclick='"+onclickTxt+"'>";
    for (var j = 0; j < propertiesArray.length; j++) {
        if (propertiesArray[j][1]) {
            var pos = objArray[i][propertiesArray[j][0]] >= 0;
            containingText += "<td class='stockElementD'><a class='"+((pos) ? "positive": "negative")+"Val'>"+(propertiesArray[j][2] ?  (objArray[i][propertiesArray[j][0]]*100) : (objArray[i][propertiesArray[j][0]]))+"</a>"+(propertiesArray[j][2] ? " %": "")+"</td>";
        } else {
            containingText += "<td class='stockElementD'>"+(propertiesArray[j][2] ?  (objArray[i][propertiesArray[j][0]]*100) : (objArray[i][propertiesArray[j][0]]))+(propertiesArray[j][2] ? " %": "")+"</td>";
        }
    }
    str = "ClickedCanvas(event,'"+objArray[i]['Ticker']+"')";
    containingText += '<td class="stockElementD"><canvas onclick="'+str+'" id="canvas'+objArray[i]['Ticker']+'" width="100" height="50" style=""></td>';
    containingText += "</tr>";
}
document.getElementById(tableID).innerHTML = containingText;

for (var i = 0; i < objArray.length; i++) {
        if (i < graphsDisplayed) {        
        var ticker = objArray[i]['Ticker'];        
        var tickerData = historical.filter(function(historicalLine) {
	       return historicalLine[0] == ticker;
        });
        populateCanvas(ticker, tickerData);
        }
}

}
}

function gotoPage (str) {
window.location.href = "viewStock.php?ticker="+str;
}

function sortTable(objArray, colName) {
if (objArray.length > 0) {
var sortedArrayTemp = [];
/*objArray[0][colName].toString().match(/[a-z]/i)*/
    // String Row
    if (colName == sortedCol) {
        sortedAscending = !sortedAscending;
        sortedArrayTemp = objArray.sort(compareValues(colName, (sortedAscending) ? "asc" : "desc"));
        console.log(sortedAscending);
        populateTable(sortedArrayTemp, "table1");
        console.log(sortedArrayTemp);
        return sortedArrayTemp;
    } else {
        sortedAscending = false;
        sortedCol = colName;
        sortedArrayTemp = objArray.sort(compareValues(colName, (sortedAscending) ? "asc" : "desc"));
        console.log(sortedAscending);
        populateTable(sortedArrayTemp, "table1");
        console.log(sortedArrayTemp);
        return sortedArrayTemp;
    }
}
}

function ClickedCanvas (e, ticker) {
if (!e) var e = window.event;
e.cancelBubble = true;
if (e.stopPropagation) e.stopPropagation();
console.log(graphedTickers.indexOf(ticker) > -1);
if (graphedTickers.indexOf(ticker) == -1) {
    graphedTickers.push(ticker);
    populateFocusCanvas();
}
}

function removeGraphed (element) {
    graphedTickers.splice(element, 1);
    populateFocusCanvas();
}

function getActiveProperties () {
var result = [];
for (var i = 0; i < propertiesArray.length; i++) {
    result.push(propertiesArray[i][0]);
}
return result;
}

function populateCanvas (tickerName, data) {

var c = document.getElementById("canvas"+tickerName);
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

for (var i = 0; i < data.length; i++) {
    var val1 = data[(i-1).clamp(0, data.length)][2];
    var val2 = data[i][2];
    
    var x1 = (i-1).clamp(0, data.length)/50*c.width;
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

function populateFocusCanvas () {

var htmlSTR = '<div id="test1" style="max-height:200px; overflow:auto; padding-right:5px;">';
for (var i = 0; i < graphedTickers.length; i++) {
onclickText = "removeGraphed("+i+")";
colourSelected = colours[i%colours.length];
htmlSTR += '<div id="stockBtnContainer"><div style="vertical-align: top;margin-top:5px;width:29; height:29;display:inline-block; background-color:'+colourSelected+';"></div><div id="stockButton"><a style="padding-right: 7px;">'+graphedTickers[i]+'</a><a style="float:right" onclick="'+onclickText+'">X</a></div></div>';
}
htmlSTR += '</div>';
document.getElementById('graphedContainer').innerHTML = htmlSTR;

document.getElementById('test1').style.height = document.getElementById('test1').offsetHeight;

var c = document.getElementById('focusCanvas');
var ctx = c.getContext("2d");
ctx.clearRect(0, 0, c.width, c.height);
for (var j = 0; j < graphedTickers.length; j++) {
console.log(graphedTickers);
var data = historical.filter(function(historicalLine) {
	       return historicalLine[0] == graphedTickers[j];
});

var mapped = data.map(function(v) {
  return v[2];
})

var max = 1.05*Math.max.apply(Math, mapped);
var min = 0.95*Math.min.apply(Math, mapped);

console.log(min);
colourSelected = colours[j%colours.length];
ctx.strokeStyle = colourSelected;

data.sort(function(a,b){
    return a[1] - b[1];
});

for (var i = 0; i < data.length; i++) {
    var val1 = data[(i-1).clamp(0, data.length)][2];
    var val2 = data[i][2];
    
    var x1 = (i-1).clamp(0, data.length)/50*c.width;
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
if (graphedTickers.length < 1) {
    ctx.fillStyle = "#ffffff";
    ctx.font = "30px Arial";
    ctx.textAlign = "center";
    ctx.fillText("Click on any of the", c.width/2, 85);
    ctx.fillText("Stock Graphs", c.width/2, 115);
    ctx.fillText("to overlay", c.width/2, 145);
}
}

function compareValues(key, order='asc') {
  return function(a, b) {
    if(!a.hasOwnProperty(key) || !b.hasOwnProperty(key)) {
      return 0;
    }

    const varA = (typeof a[key] === 'string') ?
      a[key].toUpperCase() : a[key];
    const varB = (typeof b[key] === 'string') ?
      b[key].toUpperCase() : b[key];

    let comparison = 0;
    if (varA > varB) {
      comparison = 1;
    } else if (varA < varB) {
      comparison = -1;
    }
    if (typeof a[key] === 'string') {
            return (
            (order == 'desc') ? comparison : (comparison * -1)
            );
    } else {
            return (
            (order == 'desc') ? (comparison * -1) : comparison
            );
    }
    
  };
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
</script>


<style>
body {
background-color: #202020;
font-family: 'Roboto', sans-serif;
color:white;
}
th {
background-color: #202035;
-webkit-touch-callout: none;
-webkit-user-select: none;
-khtml-user-select: none;
-moz-user-select: none;
-ms-user-select: none;
user-select: none;
}
.sortedAsc {
color: #eaeaea;
}
.sortedDesc {
color: #eaeaea;
}
.positiveVal {
    color: lime;
}
.negativeVal {
    color: #ff2828;
}
.stockTable {
    color:white;
    border-collapse: collapse;
    width: 100%;
}
.stockElementR, .stockElementD, .stockElementH {
    padding: 8px;
    text-align: left;
    border-bottom: 1px solid #ddd;
}

.deleteColumn {
    display:block;
    padding: 1px;
    text-align:center;
    vertical-align:top; float:right; height:20px; width:20px;
    cursor: pointer;
}

.formTable {
    width:100%; 
}

th:hover .deleteColumn {
    background-color: #991b1b;
}

.deleteColumn:hover {
    background-color: red !important; 
}

.colButton {
    background-color: #505050;
    border: 3px solid #202035;
    color: white;
    padding: 5px 10px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
}

.colButton:hover {
    background-color: #777777;
}

.inputDiv {
    padding-bottom: 10px; 
}

.stockElementH:last-child{
    width:1%;
    white-space:nowrap;
}
.stockElementR {
    cursor: pointer;
}
#stockButton {
padding:5px;background-color:#303030;margin:5px;display:inline-block;margin-left:0px;
}

.stockElementR:nth-child(even) {background-color: #303030;}

.stockElementR:hover {background-color:#202035;}
</style>















