<?php

	$api_url = 'https://peertube.beeldengeluid.nl/api/v1';

	function get_curl($url) {

		$ch = curl_init();
		curl_setopt($ch, CURLOPT_URL, $url);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
		curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
		$json = curl_exec($ch);
		curl_close($ch);

		$array = json_decode($json, TRUE);

		return $array;

	}

	function post_curl($url, $array_data, $auth_header) {

		$ch = curl_init();
		curl_setopt($ch, CURLOPT_URL, $url);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
		curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
		curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
		curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($array_data));
		$json = curl_exec($ch);
		curl_close($ch);

		$array = json_decode($json, TRUE);

		return $array;

	}

	// Get client 

	$url = $api_url.'/oauth-clients/local';

	$array_client = get_curl($url);
	$client_id = $array_client['client_id'];
	$client_secret = $array_client['client_secret'];

	// Get user token

	$url = $api_url.'/users/token';

	$array_user['client_id'] = $client_id;
	$array_user['client_secret'] = $client_secret;
	$array_user['grant_type'] = 'password';
	$array_user['response_type'] = 'code';

	$array_user['username'] = 'nisv';
	$array_user['password'] = 'openbeelden';

	$array_token = post_curl($url, $array_user, '');

	$auth_header = 'Authorization: '.$array_token['token_type'].' '.$array_token['access_token'];

	// Upload video

	$url = $api_url.'/videos/upload'; 

	$array_video['name'] = 'Een imitatie van Charlie Chaplin';
	$array_video['channelId'] = 2;
	$array_video['videofile'] = curl_file_create('/home/frank/Downloads/WEEKNUMMER340-HRE0000D5AF_579560_634720.mp4');
	$array_video['language'] = 'nl';
	$array_video['licence'] = '7';
	$array_video['privacy'] = '1';
	$array_video['commentsEnabled'] = '1';
	$array_video['description'] = "Weeknummer 34-05\nBioscoopjournaals waarin Nederlandse onderwerpen van een bepaalde week worden gepresenteerd.\n\nVoorbereidingen voor carnaval in de dierenwereld: een paard imiteert Charlie Chaplin. -Div. shots als Charlie Chaplin vermomd paard; -div. titel(s)/tussentitel(s).\n\nPolygoon-Profilti (producent) / Nederlands Instituut voor Beeld en Geluid (beheerder)";

	$array_video['originallyPublishedAt'] = '1934-01-29T12:00:00.000Z';

	$ch = curl_init();
	curl_setopt($ch, CURLOPT_URL, $url);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
	curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
	curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
	curl_setopt($ch, CURLOPT_POSTFIELDS, $array_video);
	curl_setopt($ch, CURLOPT_HTTPHEADER, array($auth_header));
	
	$json = curl_exec($ch);
	curl_close($ch);

	$array = json_decode($json, TRUE);

	print_r($array);

?>