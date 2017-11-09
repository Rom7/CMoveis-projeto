var glob_antena; 
var glob_mesure;
var glob_render_points;

var start = function() // funçao para cargar os dados dos arquivos csv
{
	d3.csv("erbs.csv", function(error, antena) {

		if (error) {
			console.log(error);
		}
		else
		{
			glob_antena = antena;

			d3.csv("testLoc.csv", function(error, mesure) {
				if(error)
					{console.log(error);}
				else
				{
					glob_mesure = mesure;
					d3.csv("fichier-test.csv", function(error, render_points){ // aqui se carrega o arquivo onde estao os pontos
															//calculados pela soluçao
						if(error){console.log(error);}
						else
						{
							glob_render_points = render_points;
							init_rendering();
						}

					});
					
				}
			});
		}
	});
}


var init_rendering = function()
{
	var map = L.map("map").setView([-8.072391,-34.898461],15); // inicializaçao do mapa mais o menos no centro da zona azul

	var OpenStreetMap_Mapnik = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
	maxZoom: 19,
	attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
	}).addTo(map);

	var cadre = L.polygon([
		[-8.065,-34.91],
		[-8.065,-34.887],
		[-8.080,-34.887],
		[-8.080,-34.91]], {
			color : "blue",
			fillOpacity : 0.1
		}).addTo(map); // plota a zona onde trabalhamos com um quadro azul

	for (var i = glob_antena.length - 1; i >= 0; i--) {
		L.circleMarker([glob_antena[i].lat,glob_antena[i].lon], {
			radius : 4 ,
			color : '#005824',
			fillOpacity : 0.5,
			fillColor : "#41AE76"
		}).addTo(map).bindPopup("ID : "+glob_antena[i].nr); // plota as erbs com circulos verdes
	};


	for (var i = glob_mesure.length - 1; i >= 0; i--) {
		L.circleMarker([glob_mesure[i].lat,glob_mesure[i].lon], {
			radius : 1 ,
			color : 'red',
			fillOpacity : 0.1,
			fillColor : "red"
		}).addTo(map); // plota as mediçoes com pontos vermelhos
	};

	for (var i = glob_render_points.length - 1; i >= 0; i--) {
		L.circleMarker([glob_render_points[i].lat,glob_render_points[i].lon], {
			radius : 1 ,
			color : 'yellow',
			fillOpacity : 0.5,
			fillColor : "red"
		}).addTo(map); // plota os pontos calculados pela soluçao em amarelho
	};


}