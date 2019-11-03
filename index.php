<?php 
require_once 'users/init.php'; 
if (!securePage($_SERVER['PHP_SELF'])){die();}

$options = array(
'submit'=>'submit', 
'class'=>'btn btn-lg btn-success',
'value'=>'Send',
);

$ip = $_SERVER['REMOTE_ADDR'];
$details = json_decode(file_get_contents("http://ipinfo.io/{$ip}/json"));

if(!empty($_POST)){
	$response = preProcessForm();
	if($response['form_valid'] == true){
		$message = $response['fields']['message'];
		//echo 'python3 /var/www/html/drpy/app/run.py --query "' + $message + '"';
		// exec python classify
		$results = exec('python3 /var/www/html/drpy/app/run.py --query "' + $message + '"');
		
		$t=time();
		$date = date("Y-m-d h:i:s",$t);

		// update ip and location
		$response['fields']['ip'] = $_SERVER['REMOTE_ADDR'];
		$response['fields']['location'] = $details->loc;
		$response['fields']['messagedate'] = $date;
		$response['fields']['results'] = $results;
		
		// send to db
		postProcessForm($response);
		
		Redirect::to('index.php?err=success!');
	}
}
	
?>
<!doctype html>
<html lang="en">
    <head>    
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <title>Smart mobilization system</title>
        <link rel="shortcut icon" href="{{ url_for('static', filename='favicon.ico') }}">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    </head>

    <body>
		
        <nav class="navbar navbar-inverse navbar-fixed-top">
            <div class="container">
                <div class="navbar-header">
                    <a class="navbar-brand" href="/" target="_blank" style="color:white;">Smart mobilization system</a>
                </div>
                <div class="collapse navbar-collapse ml-auto" id="navbar" >
                    <ul class="nav navbar-nav">
                        <li><a href="/users/login.php" target="_blank" style="color:white;">Login</a></li>
                        <li><a href="#" target="_top" style="color:white;">Contact</a></li>
                    </ul>
                </div>
            </div>
        </nav>


        <div class="jumbotron">
            <div class="container">
                <h1 class="text-center">Smart mobilization system</h1>
                <p class="text-center">Emergency assistance through streamlined responses</p>
                <hr />
				<div class="row">
					<div class="col-lg-12">
						<p class="text-center">Your location: <?=$details->city;?>, <?=$details->region?> (<?=$details->loc?>)</p>
					</div>
				<div>
                <div class="row">
                    <div class="col-lg-12 form-group-lg">
					<?php
						if ($_GET['err'] == 'success!') {
							?>
							<p class="text-center text-success">Success! Emergency services have been notified</p>
							<?php
						} else {
							displayForm('helpform2', $options);
						}
					?>
                    </div>
                </div>
            </div>
        </div>

        <div class="container">

        </div>


    </body>
</html>