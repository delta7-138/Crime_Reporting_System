function openwin(className, element , color){
	var i , tab_cont; 
	tab_cont = document.getElementsByClassName("when_click");
	for(i = 0; i<tab_cont.length; i++)
		tab_cont[i].style.display = "none";

	document.getElementById(className).style.display = "block";

}