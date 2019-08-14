<?php

	// API endpoint

	$api_url = 'https://peertube.beeldengeluid.nl/api/v1';

	// Get client 

	$ch = curl_init();
	curl_setopt($ch, CURLOPT_URL, $api_url.'/oauth-clients/local');
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
	curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
	$json = curl_exec($ch);
	curl_close($ch);

	$array_result = json_decode($json, TRUE);

	$client_id = $array_result['client_id'];
	$client_secret = $array_result['client_secret'];

	// Get user token

	$array_user['client_id'] = $client_id;
	$array_user['client_secret'] = $client_secret;
	$array_user['grant_type'] = 'password';
	$array_user['response_type'] = 'code';

	$array_user['username'] = 'nisv';
	$array_user['password'] = 'openbeelden';

	$ch = curl_init();
	curl_setopt($ch, CURLOPT_URL, $api_url.'/users/token');
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
	curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
	curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'POST');
	curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($array_user));
	$json = curl_exec($ch);
	curl_close($ch);

	$array_token = json_decode($json, TRUE);

	// PUT videos

	$auth_header = 'Authorization: '.$array_token['token_type'].' '.$array_token['access_token'];

	$data['originallyPublishedAt'] = '2015-11-29';

	$ch = curl_init();
	curl_setopt($ch, CURLOPT_URL, $api_url.'/videos/a2df9503-5575-44d2-8423-dc578228100b');
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
	curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
	curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'PUT');
	curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($data));
	curl_setopt($ch, CURLOPT_HTTPHEADER, array($auth_header));
	$json = curl_exec($ch);
	
	$array = json_decode($json, TRUE);
	print_r($array);

?>