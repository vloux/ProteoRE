var cy; // cytoscape network object
var json_input; 
var hidden_nodes = []; // array of hidden nodes

// pathway parameters
var all_pathways = []; // array containing all pathways if the nodes have a pathway attribute
var edges_pathway = []; // edges belonging to the current selected pathway
var nodes_pathway = []; // nodes belonging to the current selected pathway


// shows/hides nodes if the score is above/under a certain threshold 
function scoreImpact(){
  
  var score = document.getElementById('myScore').value;

  cy.edges().filter('[weight>='+score+']').css({'opacity': 0.8});
  cy.edges().filter('[weight<'+score+']').css({'opacity': 0});

}



function createNetwork(data,datatype){
 

  if (datatype == "json"){
  
    json_input = data.elements;
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
          'background-color': 'data(colour)'
        }
      },
      {
        selector: 'node:selected',
        style: {
          'background-color': 'data(colour)',
          'border-width': '6px',
          'border-color': '#000000',
          'border-opacity': '0.5'
        }
      },
      {
        selector: '.pathway-edge',
        style: {
          'line-color': '#ff0000'
        }
      },
      {
        selector: '.pathway-node',
        style: {
          'background-color': '#ff0000'
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
  // set minimal and maximal scores for the edge interaction 
  setMinMaxScore();
  scoreImpact();
  // add pathway to the select bar in the config div
  addPathways();
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

// color nodes and edges belonging to selected pathway 
function selectPathway(){

  if (edges_pathway.length!=0){ 
   for (var e=0; e < edges_pathway.length ; e++){ 
      edges_pathway[e].removeClass('pathway-edge');
   }
    edges_pathway = [];
  }
  if (nodes_pathway.length!=0){
    nodes_pathway.removeClass('pathway-node');
    nodes_pathway = [];
  }
  

  var e = document.getElementById("selectPathway");
  var pathway = e.options[e.selectedIndex].value;
  if (pathway!="all"){
	  nodes_pathway = cy.nodes().filter(function(ele){ return ele.data('pathway').indexOf(pathway) >=0;});
    nodes_pathway.addClass('pathway-node');
    var edges_nodes_pathway = nodes_pathway.connectedEdges();

    for (var e=0; e < edges_nodes_pathway.length; e++){
      if (edges_nodes_pathway[e].source().data('pathway').indexOf(pathway)>=0 && edges_nodes_pathway[e].target().data('pathway').indexOf(pathway)>=0){
        edges_nodes_pathway[e].addClass('pathway-edge');
        edges_pathway.push(edges_nodes_pathway[e]);  
      }
    }

  }
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
	


// if there is a pathway attribute to the nodes, a pathway select input will be
// dynamically added to the menu
function addPathways(){

 var nodes_elements = [];
 for (var n=0; n < json_input.nodes.length; n++){
 
   for (var e=0; e < Object.keys(json_input.nodes[n]['data']).length; e++){
      nodes_elements.push(Object.keys(json_input.nodes[n]['data'])[e]);
   }

 } 

  nodes_elements = uniqueArray(nodes_elements);

  if ($.inArray('pathway', nodes_elements) > -1){
    getPathwayValues();
  
	  var html = "";

	  for (var p=0; p < all_pathways.length; p++){
	    html += "<option value=\""+all_pathways[p]+"\" >"+all_pathways[p]+"</option>";
	  }
	  document.getElementById("selectPathway").innerHTML += html;
  }
} 

// get the different pathway values from the json input

function getPathwayValues(){
  
  var pathway = "";

 for (var n=0; n < json_input.nodes.length; n++){
   
    pathway = json_input.nodes[n]['data']['pathway'];
    if (pathway!="None"){
      for (var p=0; p < pathway.length; p++){
        all_pathways.push(pathway[p]);
      }    
    }
 } 
  all_pathways = uniqueArray(all_pathways);

}
