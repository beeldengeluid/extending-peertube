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

	// Upload videos

	$url = $api_url.'/videos/imports'; 

	$ch = curl_init();
	curl_setopt($ch, CURLOPT_URL, $url);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
	curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
	curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");

	// Loop through CSV records

	function get_str($str) {
		$str_array = explode(";", $str);
		return trim($str_array[0]);
	}

	$i = 0;

	if (($handle = fopen("openbeelden_beng.tsv", "r")) !== FALSE) {
		while (($data = fgetcsv($handle, 4096, "\t")) !== FALSE) {

			if ($i > 200 && $i <= 300) {

				$title = get_str($data[1]);
				$header = get_str($data[2]);
				$creator = get_str($data[3]);

				$tags = explode(";", $data[4]);

				$description = str_replace("; Newsreels in which Dutch subjects of a certain week are presented.","",$data[5]);

				$date = $data[9];

				$video = $data[12];
				$video_array = explode(";", $video);

				foreach ($video_array as $item) {
					$item = trim($item);
					if (substr($item, -3) == 'mp4') {
						$video_link = $item;
					}
				}

				$licence_link = get_str($data[20]);

				$licence = "0";

				if ($licence_link == 'https://creativecommons.org/licenses/by/3.0/nl/') {
					$licence = "1";
				}

				if ($licence_link == 'https://creativecommons.org/licenses/by-sa/3.0/nl/') {
					$licence = "2";
				}

				if ($licence_link == 'https://creativecommons.org/licenses/by-nd/3.0/nl/') {
					$licence = "3";
				}

				if ($licence_link == 'https://creativecommons.org/licenses/by-nc/3.0/nl/') {
					$licence = "4";
				}

				if ($licence_link == 'https://creativecommons.org/licenses/by-nc-sa/3.0/nl/') {
					$licence = "5";
				}

				if ($licence_link == 'https://creativecommons.org/publicdomain/mark/1.0/') {
					$licence = "7";
				}

				if ($licence_link == 'https://creativecommons.org/publicdomain/zero/1.0/') {
					$licence = "7";
				}

				/*

				// Print data

				echo '<h1>'.$title.'</h1>';
				echo '<h3>'.$header.'</h3>';
				echo nl2br($description);
				echo '<br>';
				echo '<br>';
				echo $creator;
				echo '<br>';
				echo '<br>';
				echo $date;
				echo '<br>';
				echo '<br>';
				echo $tags;
				echo '<br>';
				echo '<br>';
				echo $video_link;
				echo '<br>';
				echo '<br>';
				echo $licence_link;

				*/

				$array_video = array();

				$array_video['name'] = $title;
				$array_video['channelId'] = 2;
				$array_video['targetUrl'] = $video_link;
				$array_video['language'] = 'nl';
				if ($licence != "0") {
					$array_video['licence'] = $licence;
				}
				$array_video['privacy'] = '1';

				/*
				TAGS: { min: 0, max: 5 }, // Number of total tags
    		TAG: { min: 2, max: 30 }, // Length
    		*/

				$j = 0;
				foreach ($tags as $tag) {
					$tag = trim($tag);
					if ($tag != "" && strlen($tag) > 32) {
						continue;
					}
					$array_video['tags['.$j.']'] = $tag;
					$j++;
					if ($j == 5) {
						break;
					}
				}

				$array_video['commentsEnabled'] = '1';
				$array_video['description'] = $header."\n\n".$description."\n\n".$creator;
				$array_video['originallyPublishedAt'] = $date;

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