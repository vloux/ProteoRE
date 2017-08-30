var cy; // cytoscape network object
var json_input; 
var hidden_nodes = []; // array of hidden nodes

// All values associated to nodes and edges parameters
var nodes_parameters_values = {};
var edges_parameters_values = {};

// Dictionnaries associating nodes/edges parameters to boolean values : true if
// the parameter is a numeric parameter false if it is not 
var nodes_parameters_is_numeric = {};
var edges_parameters_is_numeric = {};


var param_node_has_been_added = false;
var param_edge_has_been_added = false;

// which parameters have been added (by default "all")
var param_node_added = "all";
var param_edge_added = "all";

var nodes_highlighted = []; 
var edges_highlighted = [];

// Returns unique elements in an array 
uniqueArray = function(my_array) {
  var n = {},r=[];
  for(var i = 0; i < my_array.length; i++) 
  {
    if (!n[my_array[i]]) 
    {
      n[my_array[i]] = true; 
      r.push(my_array[i]); 
    }
  }
  return r;
}


// returns false if at least one element of the input array is not numeric
function checkIfNumeric(a){
  console.log(a);
  for (var e=0; e < a.length; e++){
    console.log(a[e]);
    if ($.isNumeric(a[e])==false && a[e]!="None" && a[e]!="NA" && a[e]!=NaN && a[e]!=null && a[e]!=undefined && a[e]!="No interactants found"){
        return(false)
    }
  }
  return(true); 

}
// get edges parameters : 

function getEdgesParameters(data){

    edges_parameters_values = {};
    
    var edges = data.elements.edges;

    // initialize the dictionnary edges_values_parameters with edge
    // parameters as keys  
    for (var j=0; j < Object.keys(edges[0]["data"]).length; j++){
      if (Object.keys(edges[0]["data"])[j]!="id" && Object.keys(edges[0]["data"])[j]!="source" && Object.keys(edges[0]["data"])[j]!="target"){
        // for each edge parameter which is not "id","source",or "target" an
        // empty list is attributed
        edges_parameters_values[Object.keys(edges[0]["data"])[j]] = []
      }
    }
    var edges = data.elements.edges;

    if (Object.keys(edges_parameters_values).length === 0){
      return(edges_parameters_values);
    }else{
      for (var i=0;i < edges.length; i++){
        for (var j=0; j < Object.keys(edges[i]["data"]).length; j++){
            if (Object.keys(edges[i]["data"])[j]!="id" && Object.keys(edges[i]["data"])[j]!="source" && Object.keys(edges[i]["data"])[j]!="target"){
            
              edges_parameters_values[Object.keys(edges[i]["data"])[j]].push(edges[i]["data"][Object.keys(edges[i]["data"])[j]]);
            }
          }
        
      }
    
      return(edges_parameters_values);
    }

}


// get nodes parameters : 

function getNodesParameters(data){

    nodes_parameters_values = {};
    
    var nodes = data.elements.nodes;

    // initialize the dictionnary nodes_values_parameters with node
    // parameters as keys  
    for (var j=0; j < Object.keys(nodes[0]["data"]).length; j++){
      if (Object.keys(nodes[0]["data"])[j]!="id"){
        // for each node parameter which is not "id","source",or "target" an
        // empty list is attributed
        nodes_parameters_values[Object.keys(nodes[0]["data"])[j]] = []
      }
    }
    var nodes = data.elements.nodes;

    if (Object.keys(nodes_parameters_values).length === 0){
      return(nodes_parameters_values);
    }else{
      for (var i=0;i < nodes.length; i++){
        for (var j=0; j < Object.keys(nodes[i]["data"]).length; j++){
            if (Object.keys(nodes[i]["data"])[j]!="id"){
            
              nodes_parameters_values[Object.keys(nodes[i]["data"])[j]].push(nodes[i]["data"][Object.keys(nodes[i]["data"])[j]]);
            }
          }
        
      }
    
      return(nodes_parameters_values);
    }

}


// Add menu bar for "filter by node/edge parameters"
function addFilterMenus(){
  
  var div = document.getElementById('config');
  
  // add edge filter menu
  var html = '<select name=\"selectEdgeParams\" id=\"selectEdgeParams\" onclick=\"selectEdgeParam()\">';

  html = html + '<option value=\"all\" selected> Filter edge parameters</option>';
  
  for (var i=0; i < Object.keys(edges_parameters_values).length; i++){
      html = html + '<option value=\"';
      html = html + Object.keys(edges_parameters_values)[i];
      html = html + '\">';
      html = html + Object.keys(edges_parameters_values)[i];
      html = html + '</option>';
  } 
  html = html + '</select>';
  div.innerHTML = div.innerHTML + html;


  // same for nodes
  html = '<select name=\"selectNodeParams\" id=\"selectNodeParams\" onclick=\"selectNodeParam()\">';

  html = html + '<option value=\"all\" selected> Filter node parameters</option>';
  for (var i=0; i < Object.keys(nodes_parameters_values).length; i++){
      html = html + '<option value=\"';
      html = html + Object.keys(nodes_parameters_values)[i];
      html = html + '\">';
      html = html + Object.keys(nodes_parameters_values)[i];
      html = html + '</option>';
  } 
  html = html + '</select>';
  div.innerHTML = div.innerHTML + html;

}

// when the user select an edge parameter, a new menu bar or range slidder is added
function selectEdgeParam(){

  var param = document.getElementById('selectEdgeParams').value;
  var div = document.getElementById('config');
  var html;
  if (param_edge_has_been_added == true){
    $('#edgeElementAdded').remove();
    param_edge_has_been_added=false;
  }
   
  if (edges_highlighted.length!=0){
    edges_highlighted.removeClass('highlight-edge');
    edges_highlighted = [];
  }
  if (param!="all"){
	  if (edges_parameters_is_numeric[param]){
	
	      var min_value = Math.min.apply(null, edges_parameters_values[param]);      
	      var max_value = Math.max.apply(null, edges_parameters_values[param]);
              // let's get an interval of 100 values
              var step = (max_value - min_value)/100;

	      html = "<form id=\"edgeElementAdded\" oninput=\"scoreoutput.value = numScore.value;\">"+param+"<input type=\"range\" name=\"numScore\" id=\"numScore\" onclick=\"hideShowEdges()\" value=\""+min_value+"\" max=\""+max_value+"\" min=\""+min_value+"\" step=\""+step+"\"><output name=\"scoreoutput\"></output></form>"
	      console.log("html");
        console.log(html);
        div.innerHTML = div.innerHTML + html;
	      $('#selectEdgeParams option:contains('+param+')').prop({selected: true});
	  }else{
	      
	      html = '<select name=\"edgeElementAdded\" id=\"edgeElementAdded\" onclick=\"highlightEdges()\"><option value=\"all\" selected>Choose an edge value</option>';
	      for (var i=0; i < edges_parameters_values[param].length;i++){
	        html += '<option value=\"'+edges_parameters_values[param][i]+'\">'+edges_parameters_values[param][i]+'</option>';
	
	      }
	      html += '</select>';
	      div.innerHTML = div.innerHTML + html;
	
	  }
	  $('#selectEdgeParams option:contains('+param+')').prop({selected: true});
	  $('#selectnodeParams option:contains('+param_node_added+')').prop({selected: true});

    param_edge_has_been_added=true;
    param_edge_added = param;
  } 

}

// when the user select a node parameter, a new menu bar or range slidder is added
function selectNodeParam(){

  var param = document.getElementById('selectNodeParams').value;
  var div = document.getElementById('config');
  var html;

  if (param_node_has_been_added == true){
    $('#nodeElementAdded').remove();
    param_node_has_been_added=false;
  }

  if (nodes_highlighted.length!=0){
    nodes_highlighted.removeClass('highlight-node');
    nodes_highlighted = [];
  }

  cy.nodes().css({'opacity': 1});
  

  if (param!="all"){
	  if (nodes_parameters_is_numeric[param]){
	
	      var min_value = Math.min.apply(null, nodes_parameters_values[param]);      
	      var max_value = Math.max.apply(null, nodes_parameters_values[param]);
        
        // let's get an interval of 100 values
        var step = (max_value - min_value)/100;
	      html = "<form id=\"nodeElementAdded\" oninput=\"scoreoutput.value = numScore.value;\">"+param+"<input type=\"range\" name=\"numScore\" id=\"numScore\" onclick=\"hideShowNodes()\" value=\""+min_value+"\" max=\""+max_value+"\" min=\""+min_value+"\" step=\""+step+"\"><output name=\"scoreoutput\"></output></form>"
	      div.innerHTML = div.innerHTML + html;
	      $('#selectnodeParams option:contains('+param+')').prop({selected: true});
	  }else{
	      
	      html = '<select name=\"nodeElementAdded\" id=\"nodeElementAdded\" onclick=\"highlightNodes()\"><option value=\"all\" selected>Choose a node value</option>';
	      for (var i=0; i < nodes_parameters_values[param].length;i++){
	        html += '<option value=\"'+nodes_parameters_values[param][i]+'\">'+nodes_parameters_values[param][i]+'</option>';
	
	      }
	      html += '</select>';
	      div.innerHTML = div.innerHTML + html;
	
	  }
	  $('#selectNodeParams option:contains('+param+')').prop({selected: true});
	  $('#selectEdgeParams option:contains('+param_edge_added+')').prop({selected: true});

    param_node_has_been_added = true;
    param_node_added = param;
  }
}

// Highlight nodes corresponding to the value of nodeElementAdded 
function highlightNodes(){

  if (nodes_highlighted.length!=0){
    nodes_highlighted.removeClass('highlight-node');
    nodes_highlighted = [];
  }
  
  var param = document.getElementById('selectNodeParams').value;
  var value = document.getElementById("nodeElementAdded").value;
 
   
  if (value!="all"){
	  nodes_highlighted = cy.nodes().filter(function(ele){ return ele.data(param).indexOf(value) >=0;});
    nodes_highlighted.addClass('highlight-node');
  }
  
}

// Highlight edges corresponding to the value of edgeElementAdded 
function highlightEdges(){

  if (edges_highlighted.length!=0){
    edges_highlighted.removeClass('highlight-edge');
    edges_highlighted = [];
  }
  

  cy.edges().css({'opacity': 0.8});
  var param = document.getElementById('selectEdgeParams').value;
  var value = document.getElementById("edgeElementAdded").value;
  if (value!="all"){
	  edges_highlighted = cy.edges().filter(function(ele){ return ele.data(param).indexOf(value) >=0;});
    edges_highlighted.addClass('highlight-edge');
  }
}
// shows/hides edges above edgeElementAdded numericalValue if the edge
// attribute selected is numerical 
function hideShowEdges(){
  
  var param = document.getElementById('selectEdgeParams').value;
  var value = document.getElementById("numScore").value;
  
	cy.edges().filter(function(ele){ return ele.data(param) >= value;}).css({'opacity':0.8});
	cy.edges().filter(function(ele){ return ele.data(param) < value;}).css({'opacity':0});

  //cy.edges().filter('[\"'+param+'\">='+value+']').css({'opacity': 0.8});
  //cy.edges().filter('[\"'+param+'\"<'+value+']').css({'opacity': 0});

}

// shows/hides nodes above nodeElementAdded numericalValue if the node
// attribute selected is numerical 
function hideShowNodes(){
  
  var param = document.getElementById('selectNodeParams').value;
  var value = document.getElementById("numScore").value;
  
  cy.nodes().filter('['+param+'>='+value+']').css({'opacity': 1});
  cy.nodes().filter('['+param+'<'+value+']').css({'opacity': 0});

}


// create cytoscape network
function createNetwork(data){

    json_input = data.elements;

    // for each edge and node parameter, get all its associated values
    edges_parameters_values = getEdgesParameters(data);
    nodes_parameters_values = getNodesParameters(data);


    // for each edge and node parameter, get all its unique associated values
    for (var i=0; i < Object.keys(edges_parameters_values).length; i++){
      edges_parameters_values[Object.keys(edges_parameters_values)[i]] = uniqueArray(edges_parameters_values[Object.keys(edges_parameters_values)[i]]);
    }
     
    for (var i=0; i < Object.keys(nodes_parameters_values).length; i++){
      nodes_parameters_values[Object.keys(nodes_parameters_values)[i]] = uniqueArray(nodes_parameters_values[Object.keys(nodes_parameters_values)[i]]);
    }
   
    // for each edge and node parameter, assert if its associated values are
    // numeric or not 
    for (var i=0; i < Object.keys(edges_parameters_values).length; i++){
      edges_parameters_is_numeric[Object.keys(edges_parameters_values)[i]] = checkIfNumeric(edges_parameters_values[Object.keys(edges_parameters_values)[i]]);
    }

    for (var i=0; i < Object.keys(nodes_parameters_values).length; i++){
      nodes_parameters_is_numeric[Object.keys(nodes_parameters_values)[i]] = checkIfNumeric(nodes_parameters_values[Object.keys(nodes_parameters_values)[i]]);
    }


    cy = window.cy = cytoscape({
       container: document.getElementById('cy'),
       elements: json_input,
       style: [
       {
         selector: 'node',
         style:
         {
           'content':'data(id)',
           //'background-color': 'data(colour)'
         }
       },
       {
         selector: 'node:selected',
         style: {
           //'background-color': 'data(colour)',
           'border-width': '6px',
           'border-color': '#000000',
           'border-opacity': '0.5'
         }
       },
       {
         selector: '.highlight-edge',
         style: {
           'line-color': '#000000',
           'width': '10px'
         }
       },
       {
         selector: '.highlight-node',
         style: {
           'background-color': '#ff0000',
           'width':'100px',
           'height':'100px'
         }
       }
  
       ]
     });
 
   // add qtip boxes with links to Nextprot and Uniprot
   cy.nodes().qtip({
     content: function(){
 
       var all_links = '<a target="_blank" href="http://www.uniprot.org/uniprot/'+this.id()+'">Uniprot external link</a><br><a href="http://www.uniprot.org/uniprot/'+this.id()+'">Uniprot internal link</a> <br> <a target="_blank" href="https://www.nextprot.org/entry/NX_'+this.id()+'/"> Nextprot external link</a>';
 
 
       return all_links; 
     },
     position: {
       target: 'mouse',
       adjust: {
         mouse: false
       }
     },
     show: {
       event: 'cxttap'
     },
     style: {
       classes: 'qtip-bootstrap',
       tip: {
         width: 16,
         height: 8
       }
     }
   });
   var defaults = {
     zoomFactor: 0.05, // zoom factor per zoom tick
     zoomDelay: 45, // how many ms between zoom ticks
     minZoom: 0.1, // min zoom level
     maxZoom: 10, // max zoom level
     fitPadding: 50, // padding when fitting
     panSpeed: 10, // how many ms in between pan ticks
     panDistance: 10, // max pan distance per tick
     panDragAreaSize: 75, // the length of the pan drag box in which the vector for panning is calculated (bigger = finer control of pan speed and direction)
     panMinPercentSpeed: 0.25, // the slowest speed we can pan by (as a percent of panSpeed)
     panInactiveArea: 8, // radius of inactive area in pan drag box
     panIndicatorMinOpacity: 0.5, // min opacity of pan indicator (the draggable nib); scales from this to 1.0
     zoomOnly: false, // a minimal version of the ui only with zooming (useful on systems with bad mousewheel resolution)
     fitSelector: undefined, // selector of elements to fit
     animateOnFit: function(){ // whether to animate on fit
       return false;
     },
     fitAnimationDuration: 1000, // duration of animation on fit
 
     // icon class names
     sliderHandleIcon: 'fa fa-minus',
     zoomInIcon: 'fa fa-plus',
     zoomOutIcon: 'fa fa-minus',
     resetIcon: 'fa fa-expand'
   };
   cy.panzoom(defaults);
   // put to automatically selected layout (here concentric)
   changeLayout();
   
 
   addFilterMenus();
  // set minimal and maximal scores for the edge interaction 
  //setMinMaxScore();
  //scoreImpact();
  // add pathway to the select bar in the config div
  //addPathways();
}


function changeLayout(){

    var html_layout_part = document.getElementById("selectShape");
    var shape = html_layout_part.options[html_layout_part.selectedIndex].value;

      cy.makeLayout({
        'name': shape
      })
      .run();

}




function viewSelectedNode(){
  var selected_node = cy.$(':selected');
  if (hidden_nodes.length!=0){ 
    hidden_nodes.restore();
  }
  if (selected_node.length==0){
    alert("Please select a node");
  }
  else{

    var selected_node_neighbors = cy.$(':selected').neighborhood(); 
    hidden_nodes = cy.elements().not(selected_node);
    hidden_nodes = hidden_nodes.not(selected_node_neighbors);
    hidden_nodes = cy.remove(hidden_nodes.union(hidden_nodes.connectedEdges()));
    cy.elements().layout({name: 'concentric', concentric: function(node){ return node.degree();}});

	  cy.makeLayout({'name': 'concentric'}).run();
	
	  

  }
}

// reset the graph to initial zoom and nodes
function getGeneralView(){

  if (edges_pathway.length!=0){
   for (var e=0; e < edges_pathway.length ; e++){ 
      edges_pathway[e].removeClass('pathway-edge');
   }
    edges_pathway = [];
    nodes_pathway.removeClass('pathway-node');
    nodes_pathway = [];
  }

  hidden_nodes.restore();
  cy.reset();
  cy.zoom(0.5);
}

function getPNG(){
  var png_image =  cy.png();
  var openWindow = window.open();
  openWindow.document.body.innerHTML = "<img src="+png_image+" />";
}

function searchProt(e){
  if(e.keyCode == 13) {
    var protein_searched = document.getElementById("search").value;
    var protein_found = cy.nodes().filter('node[id = "'+protein_searched+'"]');
    if (protein_found.length!=0){
      cy.fit(protein_found,200);
    }
  }
}

// shows only nodes with a degree superior or equal to the degree put by the
// user  
function showNodeWithDegree(e){

  if(e.keyCode == 13) {
    var degree = document.getElementById("filterdegree").value;
    
    cy.nodes().filter('[[degree >='+degree+']]').css({'opacity':1}); 
    cy.nodes().filter('[[degree <'+degree+']]').css({'opacity':0.2}); 
    }
}

// set the min and max values of the score slider
function setMinMaxScore(){
 
  var scores = [];

  for (var e=0; e < json_input.edges.length; e++){
    scores.push(json_input.edges[e]['data']['weight']);

  }

	var min_score = Math.min.apply(null,scores);
	var max_score = Math.max.apply(null,scores);

	$('#myScore').prop('min', min_score);
	$('#myScore').prop('max', max_score);
	$('#myScore').prop('value', min_score);
	$('#myScore').prop('step', ((max_score-min_score)/100));
}

// Returns unique elements in an array 
function uniqueArray(my_array) {
  var n = {},r=[];
  for(var i = 0; i < my_array.length; i++) 
  {
    if (!n[my_array[i]]) 
    {
      n[my_array[i]] = true; 
      r.push(my_array[i]); 
    }
  }
  return r;
}
	



