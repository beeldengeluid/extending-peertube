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

	// Upload videos

	$auth_header = 'Authorization: '.$array_token['token_type'].' '.$array_token['access_token'];

	$ch = curl_init();
	curl_setopt($ch, CURLOPT_URL, $api_url.'/videos/imports');
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
	curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
	curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'POST');

	// Loop through CSV records

	$i = 1;

	if (($handle = fopen('natuurbeelden.csv', 'r')) !== FALSE) {
		while (($data = fgetcsv($handle, 4096, '|')) !== FALSE) {

			if ($i > 0 && $i <= 12) {

				$title = trim($data[1]);
				$alternative = trim($data[2]);
				$tags = explode(";", $data[3]);
				$description = trim($data[4]);
				$abstract = trim($data[5]);
				$creator = $data[6];
				$date = $data[7];
				$licence_link = $data[9];

				switch ($licence_link) {
					case 'https://creativecommons.org/licenses/by/3.0/nl/':
						$licence = '1';
						break;
					case 'https://creativecommons.org/licenses/by-sa/3.0/nl/':
						$licence = '2';
						break;
					case 'https://creativecommons.org/licenses/by-nd/3.0/nl/':
						$licence = '3';
						break;
					case 'https://creativecommons.org/licenses/by-nc/3.0/nl/':
						$licence = '4';
						break;
					case 'https://creativecommons.org/licenses/by-nc-sa/3.0/nl/':
						$licence = '5';
						break;
					case 'https://creativecommons.org/licenses/by-nc-nd/3.0/nl/':
						$licence = '6';
						break;
					case 'https://creativecommons.org/publicdomain/zero/1.0/':
						$licence = '7';
						break;
					case 'https://creativecommons.org/publicdomain/mark/1.0/':
						$licence = '7';
						break;
					default:
						$licence = '0';
						break;
				}

				$video = $data[10];

				// Print data

				// echo '<h1>'.$title.'</h1>';
				// echo '<h3>'.$alternative.'</h3>';
				// echo nl2br($description);
				// echo '<br>';
				// echo '<br>';
				// echo $creator;
				// echo '<br>';
				// echo '<br>';
				// echo $date;
				// echo '<br>';
				// echo '<br>';
				// echo implode(', ', $tags);
				// echo '<br>';
				// echo '<br>';
				// echo $video;
				// echo '<br>';
				// echo '<br>';
				// echo $licence_link;

				$array_video = array();

				$array_video['name'] = $title;
				$array_video['channelId'] = 3;
				$array_video['targetUrl'] = $video;
				$array_video['language'] = 'nl';
				if ($licence != '0') {
					$array_video['licence'] = $licence;
				}
				$array_video['privacy'] = '1';

				$j = 0;
				foreach ($tags as $tag) {
					$tag = trim($tag);
					if ($tag != '' || strlen($tag) > 32) {
						continue;
					}
					$array_video['tags['.$j.']'] = $tag;
					$j++;
					if ($j == 5) {
						break;
					}
				}

				$array_video['commentsEnabled'] = '1';

				$description_ext = '';

				if ($alternative != '') {
					$description_ext.= $alternative."\n\n";
				}

				if ($description != '') {
					$description_ext.= $description."\n\n";
				}

				if ($abstract != '') {
					$description_ext.= $abstract."\n\n";
				}

				if ($creator != '') {
					$description_ext.= $creator;
				}

				$array_video['description'] = $description_ext;
				//$array_video['originallyPublishedAt'] = $date;

				curl_setopt($ch, CURLOPT_POSTFIELDS, $array_video);
				curl_setopt($ch, CURLOPT_HTTPHEADER, array($auth_header));
				$json = curl_exec($ch);
				
				$array = json_decode($json, TRUE);
				print_r($array);

			}

			$i++;

		}
	}

	fclose($handle);

	curl_close($ch);

?>