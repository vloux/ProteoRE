var cy; // cytoscape network object
var json_input; 
var hidden_nodes = []; // array of hidden nodes

// pathway parameters
var all_pathways = []; // array containing all pathways if the nodes have a pathway attribute
var edges_pathway = []; // edges belonging to the current selected pathway
var nodes_pathway = []; // nodes belonging to the current selected pathway



// All values associated to nodes and edges parameters
var nodes_parameters_values = {};
var edges_parameters_values = {};

// Dictionnaries associating nodes/edges parameters to boolean values : true if
// the parameter is a numeric parameter false if it is not 
var nodes_parameters_is_numeric = {};
var edges_parameters_is_numeric = {};

// Header from the edges and nodes attributes files 
var headerEdges = [];
var headerNodes = [];

// boolean value, true if a node/edge parameter menu/range slider has been
// added to the config div 
var param_node_has_been_added = false;
var param_edge_has_been_added = false;

// name of the node/edge parameter added (if a parameter has been added), by
// default all
var param_node_added = "all";
var param_edge_added = "all";

// Array of highlighted nodes/edges
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

// return the json format for edges'data
function getEdges(data,idBaitnb,idPreynb,idEdgesParams,headerNetworkFile){

    var edges = [];
    // decrease the column's number of -1 so that first index is 0 and not 1 
    var idBait = idBaitnb-1; 
	  var idPrey = idPreynb-1;
    
    var headerEdges = [];
    

    var edge_data;
    var node_data;

    var all_nodes = [];

    // the Json object usable by Cytoscape JS is as follows : 
    // { elements : {
    //    "nodes" : [
    //        { "data": {"id" : "1", "something": "somethingelse"}},
    //        ...
    //        ],
    //    "edges" : [ 
    //        { "data": {"id" : "1to2","source":"1","target":"2"}},
    //        ...
    //        ]
    //    }
    //  }
    //  Here we want to get the edges array.
    // NB : for unknown reasons, papaparse adds an empty array at the end of the
    // parsed data from the csv. In order to avoir this empty array, the loops
    // stops at data["data"].length-1
    if (headerNetworkFile=="true"){
      var headerEdges = data["data"][0]; // contains the header of the file     

      // prepare a dictonnary with edge's parameters as keys and arrays of values
      // associated to each parameter as key values 
      for (var i=0; i < idEdgesParams.length; i++){
      
        edges_parameters_values[headerEdges[idEdgesParams[i]-1]] = [];
      }
       
      for (var i=1; i < data["data"].length -1; i++){
	      
	      // add the basic information for each edge : id, source and target. 
	      edge_data = {"data":{"id":String(data["data"][i][idBait]+"_"+data["data"][i][idPrey]),"source":String(data["data"][i][idBait]),"target":String(data["data"][i][idPrey])}};
	     
	        // add additional information if the user entered edges's parameters  
	        if (idEdgesParams!="none"){
	          for (var j=0; j < idEdgesParams.length; j++){
	
	            edge_data["data"][headerEdges[idEdgesParams[j]-1]] = data["data"][i][idEdgesParams[j]-1];
	
	            edges_parameters_values[headerEdges[idEdgesParams[j]-1]].push(data["data"][i][idEdgesParams[j]-1]);
	          }
	      }
	      // stock edge data in edges
	      edges.push(edge_data)
	      // stock the source and target of each edge in all_nodes
	      all_nodes.push(data["data"][i][idBait]);
	      all_nodes.push(data["data"][i][idPrey]);
	    }
    }else{

      // prepare a dictonnary with edge's parameters as keys and arrays of values
      // associated to each parameter as key values 
      for (var i=0; i < idEdgesParams.length; i++){
      
        edges_parameters_values["Column_"+idEdgesParams[i]] = [];
      }

      for (var i=0; i < data["data"].length -1; i++){

	      // add the basic information for each edge : id, source and target. 
	      edge_data = {"data":{"id":String(data["data"][i][idBait]+"_"+data["data"][i][idPrey]),"source":String(data["data"][i][idBait]),"target":String(data["data"][i][idPrey])}};
      

	    // add additional information if the user entered edges's parameters  
	    if (idEdgesParams!="none"){
	      for (var j=0; j < idEdgesParams.length; j++){
	        edge_data["data"]["Column_"+idEdgesParams[j]] = data["data"][i][idEdgesParams[j]-1];
	        edge_data["data"][headerEdges[idEdgesParams[j]-1]] = data["data"][i][idEdgesParams[j]-1];
	
	        edges_parameters_values["Column_"+idEdgesParams[j]].push(data["data"][i][idEdgesParams[j]-1]);
	        }
	      }
      
	    // stock edge data in edges
	    edges.push(edge_data)
	    // stock the source and target of each edge in all_nodes
	    all_nodes.push(data["data"][i][idBait]);
	    all_nodes.push(data["data"][i][idPrey]);
      }
    }
    // nodes from the network file have been stocked in all_nodes and some are duplicated so we remove the duplicated nodes with the function uniqueArray 
    all_nodes = uniqueArray(all_nodes);
    return [edges,all_nodes];
}

function getNodes(node_attributes,all_nodes,idNode, headerNodeFile){
  
  var nodes = [];
  var nodes_added = [];
  var node_data;
  idNode = idNode -1;
 
  // get the specific elements of an array compared to another array
  // e.g : [1,2,3,4,5,6].diff( [3,4,5] ) => [1, 2, 6]  
  Array.prototype.diff = function(a) {
      return this.filter(function(i) {return a.indexOf(i) < 0;});
  };


  // first if there is a  node attributes file, add all the nodes from the node
  // attributes file to the nodes variable
  if (node_attributes!="none"){
    if (headerNodeFile=="true"){
      var headerNode = node_attributes["data"][0];
        
      // prepare a dictonnary with node's parameters as keys and arrays of values
      // associated to each parameter as key values 
      for (var i=0; i < headerNode.length; i++){
        if (i!=idNode){ 
          nodes_parameters_values[headerNode[i]] = [];
        }
      }
      for (var i=1; i < node_attributes["data"].length -1; i++){
        node_data = {"data":{"id":String(node_attributes["data"][i][idNode])}};
        nodes_added.push(node_attributes["data"][i][idNode]);
            for (var j=0; j < node_attributes["data"][i].length; j++){
              if (j!=idNode){
                node_data["data"][headerNode[j]]= node_attributes["data"][i][j];
                nodes_parameters_values[headerNode[j]].push(node_attributes["data"][i][j]); 
              }
            }
      nodes.push(node_data);
      }
      
    }else{

      // prepare a dictonnary with node's parameters as keys and arrays of values
      // associated to each parameter as key values 
      for (var i=0; i < node_attributes["data"][0].length; i++){
        if (i!=idNode){ 
          var nb = i+1;
          nodes_parameters_values["Column_"+nb] = [];
        }
      }
      
      for (var i=0; i < node_attributes["data"].length -1; i++){
        node_data = {"data":{"id":String(node_attributes["data"][i][idNode])}};
        nodes_added.push(node_attributes["data"][i][idNode]);
        for (var j=0; j < node_attributes["data"][i].length; j++){
              if (j!=idNode){
                var nb = j+1;
                node_data["data"]["Column_"+nb]= node_attributes["data"][i][j];

                nodes_parameters_values["Column_"+nb].push(node_attributes["data"][i][j]);

              }
            }
      nodes.push(node_data);
      }  
    }
    // now check in case there are nodes in the network that are not in the node
    // attributes file (e.g : if the user has only annotated some nodes of his
    // network and not all the nodes)
    var nodes_spec_to_network_file = all_nodes.diff(nodes_added);
    if (nodes_spec_to_network_file.length!=0){

    if (headerNodeFile=="true"){
        
      for (var i=0; i < nodes_spec_to_network_file.length; i++){
        node_data = {"data":{"id":String(nodes_spec_to_network_file[i])}};
            for (var j=0; j < node_attributes["data"][0].length; j++){
              if (j!=idNode){
                node_data["data"][headerNode[j]]= "NA"; 
                nodes_parameters_values[headerNode[j]].push("NA"); 
              }
            }
      nodes.push(node_data);
      }

      
    }else{
      for (var i=0; i < nodes_spec_to_network_file.length; i++){
 
       node_data = {"data":{"id":String(nodes_spec_to_network_file[i])}};
       for (var j=0; j < node_attributes["data"][0].length; j++){
              if (j!=idNode){
                var nb = j+1;
                node_data["data"]["Column_"+nb]= "NA"; 
                nodes_parameters_values["Column_"+nb].push("NA");
              }
            }
      nodes.push(node_data);
        }  
      }
    }
  }

  // If there is no node attributes file, add all the nodes from the all_nodes variable
  if (node_attributes=="none"){
    for (var i=0; i< all_nodes.length; i++){
      node_data = {"data":{"id":String(all_nodes[i])}};
      nodes.push(node_data);  
    }

  }


  return nodes;
}

// convert the text variables for node and edge attributes into a usable json
// variable for cytoscape js
function convertToJSON(data,idBaitnb,idPreynb,node_attributes, idEdgesParams, headerNetworkFile, headerNodeFile,idNode){

    
    // parse the edge attributes file into a text variable
    Papa.parse(data,{header:false,dynamicTyping:true,delimiter:"\t",complete: function(results){data = results;}});

    var network_data = getEdges(data,idBaitnb,idPreynb,idEdgesParams,headerNetworkFile);
    var edges = network_data[0];
    var all_nodes = network_data[1];


    var nodes = getNodes(node_attributes,all_nodes,idNode, headerNodeFile);
    
    // for each node parameter get an array of its unique values
    for (var i = 0; i < Object.keys(nodes_parameters_values).length; i++){
      nodes_parameters_values[Object.keys(nodes_parameters_values)[i]] = uniqueArray(nodes_parameters_values[Object.keys(nodes_parameters_values)[i]]); 
    }

    // for each edge parameter get an array of its unique values
    for (var i = 0; i < Object.keys(edges_parameters_values).length; i++){
      edges_parameters_values[Object.keys(edges_parameters_values)[i]] = uniqueArray(edges_parameters_values[Object.keys(edges_parameters_values)[i]]); 
    }
    // indicate if the nodes/edges parameters are numeric or not
    for (var i=0; i < Object.keys(nodes_parameters_values).length; i++){
      nodes_parameters_is_numeric[Object.keys(nodes_parameters_values)[i]] = checkIfNumeric(nodes_parameters_values[Object.keys(nodes_parameters_values)[i]]);

    }

    for (var i=0; i < Object.keys(edges_parameters_values).length; i++){
      edges_parameters_is_numeric[Object.keys(edges_parameters_values)[i]] = checkIfNumeric(edges_parameters_values[Object.keys(edges_parameters_values)[i]]);

    }
    var final_data = {elements: {nodes: nodes, edges: edges}}
    return(final_data);
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

// add an edge parameter menu/range slider 
function selectEdgeParam(){

  // get the name of the edge parameter selected
  var param = document.getElementById('selectEdgeParams').value;
  var div = document.getElementById('config');
  var html;
  // if an edge parameter menu/range slider is already present, remove it
  if (param_edge_has_been_added == true){
    $('#edgeElementAdded').remove();
    param_edge_has_been_added=false;
  }
  
  // if edges are highlighted due to the last edge parameter selected remove the highlight 
  if (edges_highlighted.length!=0){
    edges_highlighted.removeClass('highlight-edge');
    edges_highlighted = [];
  }
  // if the parameter not the line "Select an edge parameter"
  if (param!="all"){
    // if the selected parameter is numeric, create a range slider
	  if (edges_parameters_is_numeric[param]){
	
	      var min_value = Math.min.apply(null, edges_parameters_values[param]);      
	      var max_value = Math.max.apply(null, edges_parameters_values[param]);
        // let's get an interval of 100 values
        var step = (max_value - min_value)/100;
	      html = "<form id=\"edgeElementAdded\" oninput=\"scoreoutput.value = numScore.value;\">"+param+"<input type=\"range\" name=\"numScore\" id=\"numScore\" onclick=\"hideShowEdges()\" value=\""+min_value+"\" max=\""+max_value+"\" min=\""+min_value+"\" step=\""+step+"\"><output name=\"scoreoutput\"></output></form>"
        div.innerHTML = div.innerHTML + html;
	      $('#selectEdgeParams option:contains('+param+')').prop({selected: true});
	  }else{
	      // else create a menu with all the edge parameter unique values
	      html = '<select name=\"edgeElementAdded\" id=\"edgeElementAdded\" onclick=\"highlightEdges()\"><option value=\"all\" selected>Choose an edge value</option>';
	      for (var i=0; i < edges_parameters_values[param].length;i++){
	        html += '<option value=\"'+edges_parameters_values[param][i]+'\">'+edges_parameters_values[param][i]+'</option>';
	
	      }
	      html += '</select>';
	      div.innerHTML = div.innerHTML + html;
	
	  }
    // force the edge parameter menu to stay on the selected edge parameter
	  $('#selectEdgeParams option:contains('+param+')').prop({selected: true});
	  // same for the nodes
    $('#selectnodeParams option:contains('+param_node_added+')').prop({selected: true});

    param_edge_has_been_added=true;
    param_edge_added = param;
  } 

}
// same as selectEdgeParam() but for node parameter selection
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


}

// shows/hides nodes above nodeElementAdded numericalValue if the node
// attribute selected is numerical 
function hideShowNodes(){
  
  var param = document.getElementById('selectNodeParams').value;
  var value = document.getElementById("numScore").value;
  
  cy.nodes().filter('['+param+'>='+value+']').css({'opacity': 1});
  cy.nodes().filter('['+param+'<'+value+']').css({'opacity': 0});

}

// create the graph visualization
function createNetwork(data,idBaitnb, idPreynb, node_attributes, idEdgesParams, headerNetworkFile, headerNodeFile, idNode){

    // get the json variable representing the network and usable by CytoscapeJS
    // from the tabular input file(s) 
    json_input = convertToJSON(data,idBaitnb,idPreynb,node_attributes, idEdgesParams,headerNetworkFile,headerNodeFile,idNode);
    json_input = json_input.elements;
    
    // create the cytoscape graph in the cy div
    cy = window.cy = cytoscape({
      container: document.getElementById('cy'),
      elements: json_input,
      style: [
      {
        selector: 'node',
        style:
        {
          'content':'data(id)',
        }
      },
      {
        selector: 'node:selected',
        style: {
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
  // NB : this works only if the nodes are Uniprot identifiers -> to be
  // deleted?  
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

  // initialize the view with a default zoom
  cy.panzoom(defaults);
  // put to automatically selected layout (here concentric)
  changeLayout();
  
  // add menus which allow to manipulate the graph with edge's and node's parameters 
  addFilterMenus();
}

// Change Layout of the graph
function changeLayout(){

    var html_layout_part = document.getElementById("selectShape");
    var shape = html_layout_part.options[html_layout_part.selectedIndex].value;

      cy.makeLayout({
        'name': shape
      })
      .run();

}



// create a concentric graph from a selected node with this node and all its
// neighborhood nodes
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

// Reset the graph to initial zoom and nodes
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

// Get a static image of the graph when clicking on the camera icon
function getPNG(){
  var png_image =  cy.png();
  var openWindow = window.open();
  openWindow.document.body.innerHTML = "<img src="+png_image+" />";
}

// Zoom on the node with id entered in the search bar
function searchProt(e){
  if(e.keyCode == 13) {
    var protein_searched = document.getElementById("search").value;
    var protein_found = cy.nodes().filter('node[id = "'+protein_searched+'"]');
    if (protein_found.length!=0){
      cy.fit(protein_found,200);
    }
  }
}

// Shows only nodes with a degree superior or equal to the degree put by the
// user  
function showNodeWithDegree(e){

  if(e.keyCode == 13) {
    var degree = document.getElementById("filterdegree").value;
    
    cy.nodes().filter('[[degree >='+degree+']]').css({'opacity':1}); 
    cy.nodes().filter('[[degree <'+degree+']]').css({'opacity':0.2}); 
    }
}


