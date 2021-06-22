<?php

	header('Content-Type: text/html; charset=utf-8');

	error_reporting(E_ALL);
	ini_set('display_errors', 1);
	
	$fp = fopen('openbeelden.csv', 'w');
	
	function file_get_url($url) {

		$ch = curl_init(); 
		curl_setopt($ch, CURLOPT_URL, $url); 
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1); 
		curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
		$output = curl_exec($ch); 
		curl_close($ch);
		return $output;

	}

	function harvest($resumption) {

		global $fp;

		// Timestamp minus 24 hours

		$yesterday = time() - (7*60*60*24);

		// Check GET request for resumption or set

		if ($resumption != '') {

			if (!file_exists('cache/'.$resumption.'.xml') || filectime('cache/'.$resumption.'.xml') < $yesterday) {

				// Update cached file

				if ($file = file_get_url('https://www.openbeelden.nl/feeds/oai/?verb=ListRecords&resumptionToken='.$resumption)) {
					file_put_contents('cache/'.$resumption.'.xml', $file);
				}

			}

			$xml = simplexml_load_file('cache/'.$resumption.'.xml');

		} else {

			if (!file_exists('cache/openbeelden.xml') || filectime('cache/openbeelden.xml') < $yesterday) {

				// Update cached file
				
				if ($file = file_get_url('https://www.openbeelden.nl/feeds/oai/?verb=ListRecords&metadataPrefix=oai_oi&set=beeldengeluid')) {
					file_put_contents('cache/openbeelden.xml', $file);
				};
				
			}

			$xml = simplexml_load_file('cache/openbeelden.xml');

		}	

		$namespaces = $xml->getNamespaces(true);
		$records = $xml->ListRecords->record;

		// Check if there is a resumption token in the data set

		$token = '';

		if ($xml->ListRecords->resumptionToken) {
			$token = (string) $xml->ListRecords->resumptionToken;
		}

		// Loop through the dataset

		foreach ($records as $record) {

			$array_film = array();

			$data = $record->metadata->children($namespaces['oai_oi']);
			$rows = $data->children($namespaces['oi']);

			$array_film['identifier'] = $record->header->identifier;
			$array_film['title'] = trim(preg_replace('/\s+/', ' ', $rows->title[0]));
			$array_film['alternative'] = $rows->alternative[0];

			$array_tags = array();

			foreach ($rows->subject as $item) {
				if ($item->attributes($namespaces['xml'])->lang == 'nl') {
					$array_tags[] = $item[0];
				}
			}

			$array_film['tags'] = implode(';', $array_tags);
			$array_film['description'] = $rows->description[0];
			$array_film['abstract'] = $rows->abstract[0];
			$array_film['creator'] = $rows->creator[0];
			$array_film['date'] = $rows->date[0];
			$array_film['attributionURL'] = $rows->attributionURL[0];
			$array_film['license'] = $rows->license[0];

			// There are multiple media, we just pick the second (hd) one by each extension

			$array_medium = array();

			foreach ($rows->medium as $item) {
				if ($item->attributes()->format == 'hd') {
					$array_medium[] = $item[0];
				}
			}
			
			$array_film['file_mp4'] = '';
			$array_film['file_ogv'] = '';
			//$array_film['file_webm'] = '';

			foreach ($array_medium as $item) {
				if (substr($item, -4) == '.mp4') {
					$array_film['file_mp4'] = $item;
				}
				if (substr($item, -4) == '.ogv') {
					$array_film['file_ogv'] = $item;
				}
				// if (substr($item, -5) == '.webm') {
				// 	$array_film['file_webm'] = $item;
				// }
			}

			fputcsv($fp, $array_film, '|');
		}

		// Recursive loop

		if ($token != '') {
			harvest($token);
		}

	}

	// Run harvest

	harvest('');

	fclose($fp);

?>