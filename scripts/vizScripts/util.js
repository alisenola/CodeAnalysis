//toggles the visibility of non infringed nodes
function showRemovedF() {
  if (showRemoved == 0) {  showRemoved = 1}
  else {  showRemoved = 0  }
  updateVisibility();
}

//toggles the visibility of non infringed nodes
function showUnchangedF() {
  if (showUnchanged == 0) {  showUnchanged = 1}
  else {  showUnchanged = 0  }
  updateVisibility();
}

//toggles the visibility of non infringed nodes
function showModifiedF() {
  if (showModified == 0) {  showModified = 1}
  else {  showModified = 0  }
  updateVisibility();
}

//toggles the visibility of non infringed nodes
function showAddedF() {
  if (showAdded == 0) { showAdded  = 1}
  else {  showAdded = 0  }
  updateVisibility();
}
//toggles the visibility of non infringed nodes
function showFormerF() {
  if (showFormer == 0) { showFormer = 1}
  else {  showFormer = 0  }
  showTarget = 0
  updateVisibility();
}
//toggles the visibility of non infringed nodes
function showTargetF() {
  if (showTarget == 0) { showTarget  = 1}
  else {  showTarget = 0  }
  showFormer = 0
  updateVisibility();
}

//toggles the visibility of non io and nio nodes
function updateVisibility() {
  var link = d3.select("body").selectAll("svg").selectAll(".link")
  var node = d3.select("body").selectAll("svg").selectAll(".node")
  var dirNode = d3.select("body").selectAll("svg").selectAll(".dirNode")


  link.select("line")
  .attr("visibility", function(d) {
    return vis(d)})
  
  node.selectAll("circle")
  .attr("visibility", function(d) {
    return vis(d)})

  node.selectAll("text")
  .attr("visibility", function(d) {
    return vis(d)})

  dirNode.selectAll("rect")
  .attr("visibility", function(d) {
   return vis(d)})
}

//toggles the visibility of non infringed nodes
function vis(d) {
  if (showTarget) {
    if (d.newVersion == 0 || !d.newVersion)
      {return "hidden"}
    else {return "visible"}
  }
  else if (showFormer) {
    if (d.oldVersion == 0 || !d.oldVersion)
      {return "hidden"}
    else {return "visible"}
  }
  if (d.type == "A" && !showAdded) {return "hidden"}
  else if (d.type == "M" && !showModified) {return "hidden"}
  else if (d.type == "D" && !showRemoved) {return "hidden"}
  else if (d.type == "U" && !showUnchanged) {return "hidden"}
  else {return "visible"}
}