function newElement() {
    var li = document.createElement("li");
    var inputValue = document.getElementById("myInput").value;
    var t = document.createTextNode(inputValue);
    
    
    li.appendChild(t);
    if (inputValue === '') {
      alert("You must write something!");
    } else {
      document.getElementById("myUL").appendChild(li);
      var skills =skills.append(inputValue)
      document.write(skills)
    }
    document.getElementById("myInput").value = "";
  
    var span = document.createElement("SPAN");
   
    
    span.className = "close";
  
    li.appendChild(span);
}