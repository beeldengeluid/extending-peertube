<?php

error_reporting(-1);

// Get password protected video from PeerTube

include('video_config.php');

// video_config.php

// $api_url = 'https://peertube.beeldengeluid.nl/api/v1';
// $api_user = 'ihc';
// $api_pass = 'xxx';
// $video_passwd = 'xxx';

/*

// Get video through REST API

$api_url = 'https://peertube.beeldengeluid.nl/api/v1/videos/pt34fjVBax5dzF5z5fcGvz';

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $api_url);
curl_setopt($ch, CURLOPT_HTTPHEADER, ['x-peertube-video-password: '.$video_passwd]);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
$output_json = curl_exec($ch);
curl_close($ch);

header('Content-Type: application/json; charset=utf-8');
echo $output_json;
exit;

*/

// Return user client GET

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $api_url.'/oauth-clients/local');
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
$output_json = curl_exec($ch);
curl_close($ch);

$data = json_decode($output_json, TRUE);

$client_id = $data['client_id'];
$client_secret = $data['client_secret'];

// Return user token POST

$post_data = [
  'client_id' => $client_id,
  'client_secret' => $client_secret,
  'grant_type' => 'password',
  'response_type' => 'code',
  'username' => $api_user,
  'password' => $api_pass
];

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $api_url.'/users/token');
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($post_data));
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
$output_json = curl_exec($ch);
curl_close($ch);

$data = json_decode($output_json, TRUE);

$token_type = $data['token_type'];
$access_token = $data['access_token'];

$post_data = [
    'Authorization' => $token_type.' '.$access_token
];

$headers = [
  'x-peertube-video-password: '.$video_passwd
];

// Return video token for https://peertube.beeldengeluid.nl/w/pt34fjVBax5dzF5z5fcGvz

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $api_url.'/videos/pt34fjVBax5dzF5z5fcGvz/token');
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($post_data));
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
$output_json = curl_exec($ch);
curl_close($ch);

$data = json_decode($output_json, TRUE);

$video_token = $data['files']['token'];

// Static video URL

$static_video_url = 'https://peertube.beeldengeluid.nl/static/streaming-playlists/hls/private/be0889bb-4c50-4b9f-9c9b-20bed1481aab/dbae6561-7bbd-4ba2-be71-0f10ca5f6160-master.m3u8?videoFileToken='.$video_token.'&reinjectVideoFileToken=1';

?>
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>PeerTube embed test</title>
  </head>
  <body>
    <h1>Interview met de heer G.A. Kieft door Leo Kaan</h1>

  	<!-- <div style="position: relative; padding-top: 56.25%;"><iframe title="Interview met de heer G.A. Kieft door Leo Kaan" width="100%" height="100%" src="https://peertube.beeldengeluid.nl/videos/embed/pt34fjVBax5dzF5z5fcGvz?title=0&amp;warningTitle=0&amp;peertubeLink=0" frameborder="0" allowfullscreen="" sandbox="allow-same-origin allow-scripts allow-popups allow-forms" style="position: absolute; inset: 0px;"></iframe></div> -->

    <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
    <video id="video" width="850" height="480" controls></video>
    <script>
    if(Hls.isSupported())
    {
        var video = document.getElementById('video');
        var hls = new Hls();
        hls.loadSource('<?php echo $static_video_url; ?>');
        hls.attachMedia(video);
        hls.on(Hls.Events.MANIFEST_PARSED,function()
        {
            video.play();
        });
    }
    else if (video.canPlayType('application/vnd.apple.mpegurl'))
    {
        video.src = '<?php echo $static_video_url; ?>';
        video.addEventListener('canplay',function()
        {
            video.play();
        });
    }
    </script>

  </body>
</html>