// This script will request the json file for each protein nextprot identifier and parse it to get information. 
// This script takes as input a Nextprot ID
var request = require("request");


// Parse arguments given as inputs
var inputs = process.argv // NB : first input will be node location on the machine, and second will be the script

var id = inputs[2];
var url ="https://api.nextprot.org/entry/"+id+".json";

request({
      url: url,
      json: true
}, function (error, response, body) {
      if (!error && response.statusCode === 200) {
                var ent = body.entry;
		var mass_mol = ent.isoforms[0].massAsString;
		var seqLength = ent.isoforms[0].sequenceLength;
		var isoElec = ent.isoforms[0].isoelectricPointAsString;
		var chromosomalLocation = ent.chromosomalLocations[0].chromosome;
		var subcellLocs = ent.annotationsByCategory["subcellular-location"];
		var all_subcellLocs = "NA";
		var cpt=0;
		var subcellLocs_found = [];
		if (subcellLocs!=null){	
			for (var i=0; i < subcellLocs.length; i++){
				if (cpt==0 && subcellLocs[i].cvTermName!=null){
					if (!(subcellLocs[i].cvTermName in subcellLocs_found)){
						all_subcellLocs = subcellLocs[i].cvTermName;
						cpt = cpt +1;
						subcellLocs_found.push(subcellLocs[i].cvTermName);
						}
					}
			else{
				if (subcellLocs[i].cvTermName!=null){
					if (!(subcellLocs[i].cvTermName in subcellLocs_found)){
						all_subcellLocs = all_subcellLocs+";"+subcellLocs[i].cvTermName;
						subcellLocs_found.push(subcellLocs[i].cvTermName);
						}
					}
				}
			}
		}

		cpt = 0;
		var diseases = ent.annotationsByCategory["disease"];	
		var all_diseases = "NA";	
		var diseases_found = [];
		if (diseases!=null){	
			for (var i=0; i < diseases.length; i++){
				if (cpt==0 && diseases[i].cvTermName!=null){
					if (!(diseases[i].cvTermName in diseases_found)){
						all_diseases = diseases[i].cvTermName;
						cpt = cpt +1;
						diseases_found.push(diseases[i].cvTermName);
			
					}
				}
				else{
					if (diseases[i].cvTermName!=null){
						if (!(diseases[i].cvTermName in diseases_found)){
							all_diseases = all_diseases+";"+diseases[i].cvTermName;
							diseases_found.push(diseases[i].cvTermName);
						}
					}
				}
			}
		}
		
		var tm_domains = ent.annotationsByCategory["transmembrane-region"];
		var nb_domains = 0;
		if (tm_domains!=null){
			for (var i=0; i < tm_domains.length; i++){
				if (tm_domains[i]["properties"]!=null){
					var domains = tm_domains[i]["properties"];
					for (var j=0; j < domains.length; j++){
						if (domains[j]["name"]=="region structure" && domains[j]["value"]=="Helical"){
							nb_domains = nb_domains +1;
						}
					}
				}
			}

		}
		console.log(id+"\t"+mass_mol+"\t"+seqLength+"\t"+isoElec+"\t"+chromosomalLocation+"\t"+all_subcellLocs+"\t"+all_diseases+"\t"+nb_domains+"\t"+"PE"+ent["overview"]["proteinExistences"]["proteinExistenceInferred"]["proteinExistence"]["level"]);
                }
      });

