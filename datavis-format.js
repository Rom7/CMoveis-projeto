var glob_antena; 
var glob_mesure;
var glob_render_points;
var all_markers = [];

var map = L.map("map").setView([-8.072391,-34.898461],15); // inicializaçao do mapa mais o menos no centro da zona azul

var OpenStreetMap_Mapnik = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
maxZoom: 19,
attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
});

map.addLayer(OpenStreetMap_Mapnik);

var cadre = L.polygon([
		[-8.065,-34.91],
		[-8.065,-34.887],
		[-8.080,-34.887],
		[-8.080,-34.91]], {
			color : "blue",
			fillOpacity : 0.1
		}); // plota a zona onde trabalhamos com um quadro azul

map.addLayer(cadre);


var start = function(choix) // funçao para cargar os dados dos arquivos csv
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

							for (var i = glob_antena.length - 1; i >= 0; i--) {
								var current = L.circleMarker([glob_antena[i].lat,glob_antena[i].lon], {
									radius : 4 ,
									color : '#005824',
									fillOpacity : 0.5,
									fillColor : "#41AE76"
								}).bindPopup("ID : "+glob_antena[i].nr); // plota as erbs com circulos verdes
								map.addLayer(current);
							};

							console.log("Points in test file : "+glob_mesure.length)
							console.log("Points computed : "+glob_render_points.length)

							if(choix == "smart")
							{
								init_smart_rendering();
							}
							else if (choix == "all_points") 
							{
								init_global_rendering();
							}
						}

					});
					
				}
			});
		}
	});
}


var init_smart_rendering = function()
{
	clean_all();

	var drawed_computed_points = [];


	for (var i = glob_render_points.length - 1; i >= 0; i--) {

		var current = L.circleMarker([glob_render_points[i].lat,glob_render_points[i].lon], {
			radius : 1 ,
			color : 'yellow',
			fillOpacity : 0.5,
			fillColor : "yellow",
		}).addTo(map);

		drawed_computed_points.push(current)
		all_markers.push(current);
	};


	for (var i = drawed_computed_points.length - 1; i >= 0; i--) {
		drawed_computed_points[i].on('click', (function(j)
		{
			return function()
				{
				var current = L.circleMarker([glob_mesure[j].lat,glob_mesure[j].lon], 
						{
							radius : 1 ,
							color : 'red',
							fillOpacity : 0.1,
							fillColor : "red"
					    });
				map.addLayer(current);
				all_markers.push(current);
				};
		})(i) // javascript closure

	)};

}


var init_global_rendering = function()
{
	clean_all();
	
	for (var i = glob_antena.length - 1; i >= 0; i--) {
		var current = L.circleMarker([glob_antena[i].lat,glob_antena[i].lon], {
			radius : 4 ,
			color : '#005824',
			fillOpacity : 0.5,
			fillColor : "#41AE76"
		}).bindPopup("ID : "+glob_antena[i].nr); // plota as erbs com circulos verdes

		map.addLayer(current);
		all_markers.push(current);
	};


	for (var i = glob_mesure.length - 1; i >= 0; i--) {
		var current = L.circleMarker([glob_mesure[i].lat,glob_mesure[i].lon], {
			radius : 1 ,
			color : 'red',
			fillOpacity : 0.1,
			fillColor : "red"
		}); // plota os pontos reais em vermelho

		map.addLayer(current);
		all_markers.push(current);

	};


	for (var i = glob_render_points.length - 1; i >= 0; i--) {
		var current = L.circleMarker([glob_render_points[i].lat,glob_render_points[i].lon], {
			radius : 1 ,
			color : 'yellow',
			fillOpacity : 0.5,
			fillColor : "yellow"
		}); // plota os pontos calculados pela soluçao em amarelo

		map.addLayer(current);
		all_markers.push(current);
	};
}


var clean_all = function() // reset the map 
{
	while(all_markers != 0)
	{
		map.removeLayer(all_markers.pop());
	}
}