
//Button Variables, infringed set, width and heights
var showAdded = 1,
showRemoved = 1,
showUnchanged = 1,
showModified = 1,
showFormer = 0,
showTarget = 0;

Math.seedrandom('random');

var sizeMod = 3,
	maxSize = 200,
	padding = 6;

var width = 8000,
    height = 8000;

var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);


var force = d3.layout.force()
    .size([width, height]);

  var psv = d3.dsv(";", "text/plain");
  psv(currentData, function(error, links) {
  if (error) throw error;
  var nodesByName = {};


  // Create nodes for each unique source and target.
  links.forEach(function(link) {
      link.source = nodeByName(link.source);
      link.target = nodeByName(link.target);

      // Provide types for source and target
      link.target.type = link.type;
      if (link.type == "Directory") {
        link.source.type = "Directory";}
      else {
      //target is based on whether it is added, removed, etc.
      //Directories are not touched
      if (link.type == "M" || link.type == "U" || link.type == "D"){
      link.target.oldVersion = 1; link.oldVersion = 1 }
      else {link.target.oldVersion = 0; link.oldVersion = 0}

      if (link.type == "M" || link.type == "U" || link.type == "A"){
      link.target.newVersion = 1; link.newVersion = 1}
      else {link.target.newVersion = 0; link.newVersion = 0}
      }
      //source is always a directory. It's a 0 by default, turns into 1.
      //if any of its targets are 1.
      if (link.target.newVersion == 1) {
        link.source.newVersion = 1;
        link.newVersion = 1;
      }
      if (link.target.oldVersion == 1) {
        link.source.oldVersion = 1;
        link.oldVersion = 1;
      }

      //size Tweaks for size sanity
      if (link.newSize > 0) {link.target.size = link.newSize/100}
      else {link.target.size = link.origSize/100}
      link.target.size = Math.min(maxSize,link.target.size)
      link.target.shade = Math.abs(link.newSize - link.origSize)/link.origSize;

      if (link.target.size) {link.target.radius = sizeMod * Math.sqrt(link.target.size/Math.PI) }
      link.target.charge = -60 -link.target.radius*10;
    
  });

  // Extract the array of nodes from the map by name.
  var nodes = d3.values(nodesByName);

  var dirNodes = nodes.filter(function(d) {return d.type == "Directory"});

  // Create the link lines.
  var link = svg.selectAll(".link")
      .data(links)
    .enter().append("g")
      .attr("class", "link")
      .append("line");

  //create the dirNode circles
  var dirNode = svg.selectAll(".dirNode")
      .data(dirNodes)
    .enter().append("g")
    .attr("class", "dirNode").call(force.drag);

    dirNode.append("rect")
      .attr("class","dirNode")
      .attr("width", 14)
      .attr("height",20)
      .style("fill", function(d) {
		return "gold" //directory
    })

  var labels = svg.selectAll('.folder-label')
  	.data(dirNodes)
  	.enter().append("g")
/*
  	labels.append("text").attr("x", function(d) {return d.x;}).attr("y", function(d) {return d.y;})
  	.attr("class","shadow") .style("font", "20px Georgia, serif").text(function(d) {return d.label.toUpperCase()} );
  	labels.append("text").attr("x", function(d) {return d.x;}).attr("y", function(d) {return d.y;})
  	.style("font", "20px Georgia, serif") .text(function(d) {return d.label.toUpperCase()} );
*/
    dirNode.on("mouseover",function(d) {
      d3.select(this).moveToFront();
        d3.select(this).append("text")
      .attr("dx",16)
      .attr("dy",".35em")
        .attr("class","shadow")
      .text(d.label.toUpperCase())
      d3.select(this).append("text")
      .attr("dx",16)
      .attr("dy",".35em")
      .text(d.label.toUpperCase())
      }).on("mouseout",function(d) {
        d3.select(this).select("text").remove();
        d3.select(this).select("text").remove();
      }) 


   // Create the node circles.
  var node = svg.selectAll(".node")
      .data(nodes)
    .enter().append("g")
    .attr("class", "node").call(force.drag);
   

    node.on("mouseover",function(d) {
    	d3.select(this).moveToFront();
        d3.select(this).append("text")
      .attr("dx",16)
      .attr("dy",".35em")
        .attr("class","shadow")
      .text(d.label.toUpperCase())
      d3.select(this).append("text")
      .attr("dx",16)
      .attr("dy",".35em")
      .text(d.label.toUpperCase())
      }).on("mouseout",function(d) {
        d3.select(this).select("text").remove();
        d3.select(this).select("text").remove();
      }) 

    node.append("circle")
      .attr("class", "node")
      .attr("r", function(d) {
        if (d.radius) {return d.radius}
        else {return 0};
      })
      .style("fill", function(d) {
        if (d.type == "A") { return "green"}
        else if (d.type == "D") {return "pink"}
        else if (d.type == "M") { return 'hsl(240,100%,'+ Math.max(50,90 - d.shade*100) +'%)'}
        else if (d.type == "U") {return "grey"}
      })

  // Start the force layout.
  force
      .nodes(nodes)
      .links(links)
      .linkDistance(60) //default 
      .gravity(0)
      .charge(function(d) { //default -60
        if (d.charge) {return d.charge*2}
        else return -60*2;
      })
      .on("tick", tick)
      .start();

  function tick(e) {
    link.attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node.each(gravity(0.1*e.alpha))
        .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

    dirNode.each(gravity(0.1*e.alpha))
    	.attr("transform", function(d) { return "translate(" + (d.x-7) + "," + (d.y-10) + ")"; });

    labels.each(function(d) {d3.select(this).moveToFront()})
    .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
  }

  function nodeByName(name) {
  	nameArray = name.split("/");
    return nodesByName[name] || (nodesByName[name] = {name: name, label: nameArray[nameArray.length-1]});
  }
});

// Reorients gravity causing like nodes to be bunched in different locations
// Slightly messy there's probably a smarter algorithm
function gravity(alpha) {
  return function(d) {
  	switch(d.type) {
  		case "D":
  			xgrav = 0.1;
  			ygrav = 0;
  			break;
  		case "A":
  			xgrav = -0.1;
  			ygrav = 0;
  			break;
  		case "M":
  			xgrav = 0;
  			ygrav = 0.1;
  			break;
  		default:
  			xgrav = 0;
  			ygrav = 0;
  	}
	  d.y += (height/2 + height*ygrav - d.y) * alpha;
	  d.x += (width/2 + width*xgrav - d.x) * alpha;
  };
}

//Moves mouseover nodes to the front for greater visibility
d3.selection.prototype.moveToFront = function() {
  return this.each(function(){
   this.parentNode.appendChild(this);
  });
};  